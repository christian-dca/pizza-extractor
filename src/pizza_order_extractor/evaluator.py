import os
import json
import pandas as pd
from pathlib import Path
import math
import re
from typing import Any, Dict, List, Tuple, Union
from rapidfuzz import fuzz
from scipy.optimize import linear_sum_assignment


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "extraction_results"


def load_and_evaluate(
    gold_file: Union[str, Path, List[Dict[str, Any]]],
    pred_file: Union[str, Path, List[Dict[str, Any]]],
    duration_list = None,
) -> pd.DataFrame:

    gen_path = DATA_DIR / pred_file
    gt_path = DATA_DIR / gold_file

    # Dateiinhalte als Liste laden
    with open(gt_path, "r", encoding="utf-8") as f:
        gt_dataset = json.load(f)
        

    with open(gen_path, "r", encoding="utf-8") as f:
        gen_dataset = json.load(f)
        

    
    csv_path = PROJECT_ROOT / "data" / "evaluation_results" / "extractor_benchmark_results.csv"


    evaluation_path = PROJECT_ROOT / "data" / "evaluation_results"
    evaluation_path.mkdir(parents=True, exist_ok=True)

    evaluator = IDPEvaluator(fuzzy_threshold=70.0)

# 3. Evaluierung ausführen & CSV exportieren
    return evaluator.evaluate_and_export(
        gt_dataset=gt_dataset,
        ext_dataset=gen_dataset,
        dataset_name=pred_file,
        output_path=csv_path,
        duration_list=duration_list,
    )


class IDPEvaluator:
    def __init__(self, fuzzy_threshold: float = 70.0):
        """
        :param fuzzy_threshold: Threshold for token set ratio in strings (0-100).
        """
        self.fuzzy_threshold = fuzzy_threshold

    def _infer_schema_fields(self, gt_dataset: List[dict]) -> Tuple[List[str], List[str], str]:
        scalar_fields = set()
        nested_list_fields = set()
        item_list_key = None

        # 1. First find item_list_key across all samples
        for order in gt_dataset:
            order_dict = order.model_dump() if hasattr(order, "model_dump") else order
            if isinstance(order_dict, dict) and item_list_key is None:
                for k, v in order_dict.items():
                    if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                        item_list_key = k
                        break

        # 2. Extract schema fields from items
        for order in gt_dataset:
            order_dict = order.model_dump() if hasattr(order, "model_dump") else order
            if not isinstance(order_dict, dict):
                continue

            items = order_dict.get(item_list_key, []) if item_list_key else (
                order_dict if isinstance(order_dict, list) else [order_dict]
            )

            for item in items:
                if isinstance(item, dict):
                    for key, val in item.items():
                        if isinstance(val, dict) or (isinstance(val, list) and any(isinstance(elem, dict) for elem in val)):
                            nested_list_fields.add(key)
                        else:
                            scalar_fields.add(key)

        scalar_fields = scalar_fields - nested_list_fields
        return sorted(list(scalar_fields)), sorted(list(nested_list_fields)), item_list_key

    def match_values(self, val1: Any, val2: Any) -> Union[bool, float]:
        # 1. Numeric check
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            return math.isclose(val1, val2, rel_tol=1e-5)

        if type(val1) != type(val2):
            return False

        if isinstance(val1, bool):
            return val1 == val2

        # 2. String comparison
        if isinstance(val1, str):
            if val1.strip().lower() == val2.strip().lower():
                return True
            return fuzz.token_set_ratio(val1, val2) >= self.fuzzy_threshold

        # 3. List comparison (primitive string/number lists)
        if isinstance(val1, list):
            if not val1 and not val2:
                return 1.0
            if not val1 or not val2:
                return 0.0

            matched_indices = set()
            intersection = 0
            for elem1 in val1:
                for idx2, elem2 in enumerate(val2):
                    if idx2 not in matched_indices and self.match_values(elem1, elem2):
                        matched_indices.add(idx2)
                        intersection += 1
                        break

            union = len(val1) + len(val2) - intersection
            return round(intersection / union, 4)

        return val1 == val2

    def flatten_to_tuples(self, data: Any, prefix: str = "") -> List[Tuple[str, Any]]:
        if hasattr(data, "model_dump"):
            data = data.model_dump()
        elif hasattr(data, "dict"):
            data = data.dict()

        tuples = []
        if isinstance(data, dict):
            for k, v in data.items():
                new_k = f"{prefix}.{k}" if prefix else k
                tuples.extend(self.flatten_to_tuples(v, new_k))
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                new_k = f"{prefix}[{idx}]"
                tuples.extend(self.flatten_to_tuples(item, new_k))
        else:
            if data is not None and data != "":
                tuples.append((prefix, data))
        return tuples

    def compute_jaccard(self, gt_tuples: List[Tuple[str, Any]], ext_tuples: List[Tuple[str, Any]]) -> Dict[str, Any]:
        matched_ext_indices = set()
        intersection = 0

        for gt_k, gt_v in gt_tuples:
            gt_path_norm = re.sub(r'\[\d+\]', '[]', gt_k)
            for idx, (ext_k, ext_v) in enumerate(ext_tuples):
                if idx in matched_ext_indices:
                    continue
                ext_path_norm = re.sub(r'\[\d+\]', '[]', ext_k)
                if gt_path_norm == ext_path_norm and self.match_values(gt_v, ext_v):
                    intersection += 1
                    matched_ext_indices.add(idx)
                    break

        gt_count = len(gt_tuples)
        ext_count = len(ext_tuples)
        union = gt_count + ext_count - intersection
        score = (intersection / union) if union > 0 else 1.0

        return {
            "intersection": intersection,
            "gt_count": gt_count,
            "ext_count": ext_count,
            "union": union,
            "jaccard_score": round(score, 4)
        }

    def align_lists(self, gt_list: List[Any], ext_list: List[Any]) -> List[Tuple[Any, Any]]:
        if not gt_list and not ext_list:
            return []

        # Pad shorter list with empty dicts to account for missing/extra items
        max_len = max(len(gt_list), len(ext_list))
        gt_padded = gt_list + [{}] * (max_len - len(gt_list))
        ext_padded = ext_list + [{}] * (max_len - len(ext_list))

        cost_matrix = []
        for gt_item in gt_padded:
            row = []
            gt_flat = self.flatten_to_tuples(gt_item)
            for ext_item in ext_padded:
                ext_flat = self.flatten_to_tuples(ext_item)
                score = self.compute_jaccard(gt_flat, ext_flat)["jaccard_score"]
                row.append(1.0 - score)
            cost_matrix.append(row)

        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        return [(gt_padded[r], ext_padded[c]) for r, c in zip(row_ind, col_ind)]

    def evaluate_order(self, gt_order: dict, ext_order: dict) -> dict:
        gt_flat = self.flatten_to_tuples(gt_order)
        ext_flat = self.flatten_to_tuples(ext_order)
        return self.compute_jaccard(gt_flat, ext_flat)

    def evaluate_and_export(
        self, 
        gt_dataset: List[dict], 
        ext_dataset: List[dict], 
        dataset_name: str,
        output_path: str,
        sample_label: str = "Sample",
        duration_list: List[float] = None
    ) -> pd.DataFrame:
        scalar_fields, nested_list_fields, item_list_key = self._infer_schema_fields(gt_dataset)

        rows = []
        total_intersection = 0
        total_gt = 0
        total_ext = 0

        for sample_idx, (gt_sample, ext_sample) in enumerate(zip(gt_dataset, ext_dataset), start=1):
            sample_id = f"{sample_label}_{sample_idx}"
            
            current_duration = (
                duration_list[sample_idx - 1] 
                if duration_list and (sample_idx - 1) < len(duration_list) 
                else None
            )

            gt_dict = gt_sample.model_dump() if hasattr(gt_sample, "model_dump") else gt_sample
            ext_dict = ext_sample.model_dump() if hasattr(ext_sample, "model_dump") else ext_sample

            if item_list_key:
                gt_items = gt_dict.get(item_list_key, [])
                ext_items = ext_dict.get(item_list_key, [])
            else:
                gt_items = [gt_dict] if isinstance(gt_dict, dict) else gt_dict
                ext_items = [ext_dict] if isinstance(ext_dict, dict) else ext_dict

            aligned_items = self.align_lists(gt_items, ext_items)

            # 1. ITEM-EBENE
            for item_idx, (gt_item, ext_item) in enumerate(aligned_items, start=1):
                item_label = f"{item_list_key[:-1] if item_list_key and item_list_key.endswith('s') else 'item'}_{item_idx}"
                row = {
                    "dataset_name": dataset_name,
                    "sample_id": sample_id,
                    "level": "item",
                    "item_id": item_label,
                    "duration_sec": None  
                }

                for field in scalar_fields:
                    gt_v = gt_item.get(field)
                    ext_v = ext_item.get(field)
                    if gt_v is None and ext_v is None:
                        row[field] = 1.0
                    elif gt_v is not None and ext_v is not None:
                        match_res = self.match_values(gt_v, ext_v)
                        row[field] = float(match_res) if isinstance(match_res, (bool, int, float)) else (1.0 if match_res else 0.0)
                    else:
                        row[field] = 0.0

                for list_field in nested_list_fields:
                    gt_nested = self.flatten_to_tuples(gt_item.get(list_field, []))
                    ext_nested = self.flatten_to_tuples(ext_item.get(list_field, []))
                    row[f"{list_field}_jaccard"] = self.compute_jaccard(gt_nested, ext_nested)["jaccard_score"]

                item_gt_flat = self.flatten_to_tuples(gt_item)
                item_ext_flat = self.flatten_to_tuples(ext_item)
                row["jaccard_score"] = self.compute_jaccard(item_gt_flat, item_ext_flat)["jaccard_score"]
                rows.append(row)

            # 2. SAMPLE-EBENE
            sample_metrics = self.evaluate_order(gt_dict, ext_dict)
            total_intersection += sample_metrics["intersection"]
            total_gt += sample_metrics["gt_count"]
            total_ext += sample_metrics["ext_count"]

            sample_row = {
                "dataset_name": dataset_name,
                "sample_id": sample_id,
                "level": "sample_summary",
                "item_id": "-",
                "duration_sec": round(current_duration, 4) if current_duration is not None else None,
                "jaccard_score": sample_metrics["jaccard_score"]
            }
            for field in scalar_fields + [f"{lf}_jaccard" for lf in nested_list_fields]:
                sample_row[field] = None
            rows.append(sample_row)

        # 3. DATASET-EBENE
        total_union = total_gt + total_ext - total_intersection
        global_jaccard = (total_intersection / total_union) if total_union > 0 else 1.0
        total_duration = sum(d for d in duration_list if d is not None) if duration_list else None

        ds_row = {
            "dataset_name": dataset_name,
            "sample_id": "DATASET",
            "level": "dataset_summary",
            "item_id": "-",
            "duration_sec": round(total_duration, 4) if total_duration is not None else None,
            "jaccard_score": round(global_jaccard, 4)
        }
        for field in scalar_fields + [f"{lf}_jaccard" for lf in nested_list_fields]:
            ds_row[field] = None
        rows.append(ds_row)     
   
        # Convert to DataFrame & save CSV
        if os.path.exists(output_path):
            df_old = pd.read_csv(output_path, encoding="utf-8-sig")
            df_new = pd.DataFrame(rows)
            df = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df = pd.DataFrame(rows)

        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        
        print(f"✅ Evaluation complete. Results saved in '{output_path}'.")
        print(f"📊 Global Dataset Jaccard Score: {round(global_jaccard * 100, 2)}%")
        
        return df