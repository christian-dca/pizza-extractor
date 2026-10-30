# The Data & Cloud Academy: AI-Automation Tutorials
# Practice Project 1: Intelligent Order Extraction for Food Service Automation
# Langchain/Pydantic/Ollama

1. [Project Overview](#1-project-overview)
2. [Practical Relevance from an LLM Engineering Perspective](#2-practical-relevance-from-an-llm-engineering-perspective)
3. [Pipeline Overview](#3-pipeline-overview)
4. [Outlook: Productionization & Next Steps](#4-outlook-productionization--next-steps)
5. [Installation & Setup](#5-installation--setup)

---

## 1. Project Overview

Ordering pizza over the phone represents a surprisingly complex real-world application of human speech production. Customers frequently speak in a non-linear fashion, correct themselves mid-sentence, request complex custom modifications, and leave critical details implicit.

This complexity makes food order processing an ideal benchmark for testing LLM-based extraction pipelines. Traditional rule-based Natural Language Processing (NLP) and regular expressions (regex) fail when handling non-standard order variations. Large Language Models (LLMs) provide the semantic reasoning required to map heterogeneous natural language inputs into rigid, programmatically actionable data structures.

This project demonstrates how to configure an **Intelligent Document Processing (IDP)** pipeline step-by-step. The pipeline extracts structured order data from unstructured phone transcriptions into deterministic JSON schemas suitable for downstream kitchen management and Point-of-Sale (POS) systems.

While applied to food service here, this extraction architecture can be adapted to other domains, such as processing invoices or résumés. By leveraging local LLMs, sensitive data remains entirely on-device, satisfying strict compliance and privacy requirements.

This tutorial is part of the **Data & Cloud Academy AI-Automation Curriculum**. It is designed for Python developers looking to build LLM workflows using **LangChain** (the industry-standard orchestration framework) and **Ollama** (for local model deployment). The workflow is divided into four notebooks, which explain architectural decisions and technologies and provide students with step-by-step tasks for configuring and optimizing an IDP extractor. 


---

## 2. Practical Relevance from an LLM Engineering Perspective

From an **LLM Engineering** and **MLOps** perspective, this project mirrors real-world enterprise automation patterns:

1. **Deterministic Output Enforcement (JSON / Pydantic):** Enterprise APIs require strict typing. LLMs are probabilistic by nature; enforcing typed schemas bridges the gap between generative output and deterministic backend applications.
2. **Model Right-Sizing & Cost/Latency Optimization:** In production systems, routing routine extraction tasks to high-parameter cloud models is cost-prohibitive and introduces unnecessary latency. Evaluating smaller open-weights models (e.g., Llama 3.1 8B, Qwen 2.5) locally allows engineering teams to optimize token costs, lower latency, and ensure digital sovereignty.
3. **Vendor-Agnostic Abstraction:** Enterprise architectures require decoupling from single providers. Framework abstractions allow teams to change underlying model infrastructure without rewriting core pipeline code.
4. **Automated Evaluation (LLM-as-a-Judge):** Manual verification does not scale. Implementing automated evaluation loops enables Continuous Integration and Continuous Testing (CI/CD) across prompt and model iterations.

---

## 3. Pipeline Overview

### Notebook 1: Synthetic Test-Order Generation
Generate a comprehensive, edge-case-heavy dataset of test orders to evaluate the pipeline. Introduces LangChain abstractions for interacting with proprietary cloud APIs and local Ollama models, as well as methods for enforcing schema compliance.

### Notebook 2: Extractor Implementation & Optimization (LLM-as-a-Judge)
Build an initial extraction prototype and establish an iterative refinement loop using a high-capability proprietary model (Claude, ChatGPT, or Gemini) as an evaluator. Focuses on catching edge cases, avoiding over-fitting to training data, and analyzing extraction failures.

## Notebook 3: Configurate a schema agnostic evaluator and golden dataset for quantitative evaluation
Evaluate the extraction results against a Golden Dataset (verified ground-truth JSON for our 10 test orders). The notebook provides a step-by-step discussion of the elements and trade-offs involved in setting up an evaluator script.

### Notebook 4: Model Right-Sizing & Cross-Benchmarking
Transition from cloud-based LLMs to smaller, locally deployed models. Compare model performance using both automated rule-based evaluation (against a golden dataset) and LLM-as-a-Judge methodology to establish optimal precision, latency, and cost trade-offs.

---

## 4. Outlook: Productionization & Next Steps

To scale this pipeline into a production-grade telephony automation system, consider implementing the following extensions:

1. **Speech-to-Text (STT) & Phonetic Noise Resilience**
   * Integrate an upstream Automatic Speech Recognition (ASR) engine (e.g., Whisper or Deepgram).
   * Benchmark extraction resilience against phonetic transcription errors (e.g., mapping *"Funghi"* to *"Fungi"* or *"Phonjee"*).

2. **Database Synchronization & Fuzzy Matching**
   * Validate extracted items against active POS menu databases using string-distance metrics (e.g., Levenshtein distance).
   * Map unlisted requests to standard menu options (e.g., normalizing *"Extra Large"* to *"Large"* if XL is unavailable).

3. **Dialogue State Management & Slot-Filling**
   * Track conversation state to handle missing required parameters (e.g., unspecified pizza size).
   * Trigger clarifying prompt loops when confidence scores fall below a defined threshold.

4. **SLA & Latency Optimization**
   * Implement token streaming, speculative decoding, or quantized model formats (e.g., GGUF 4-bit/8-bit) to guarantee sub-second latency required for interactive voice agents.

5. **MLOps Telemetry & Monitoring**
   * Integrate observability platforms (e.g., LangSmith or Phoenix) to monitor schema validation failure rates, latency distributions, and token usage in real time.

---

## 5. Installation & Setup

### Prerequisites & Dependency Management
This project uses [`uv`](https://github.com/astral-sh/uv) for fast, deterministic Python package management. Python **3.13+** is recommended.

1. **Clone the repository and install `uv`:**
   ```bash
   git clone <repository-url>
   cd pizza-order-extractor

(If uv is not installed, follow the installation guide at astral.sh/uv).

    Initialize environment and sync dependencies:
    Bash

    uv sync

    Running the Notebooks:

        Option A: VS Code (Recommended)
        Ensure the Jupyter extension is installed in VS Code. Open any notebook and select the .venv kernel created by uv.

        Option B: Standalone Jupyter Notebook
        Register the virtual environment kernel and launch Jupyter:
        Bash

        uv run python -m ipykernel install --user --name pizza_extractor --display-name "Python (pizza_extractor)"
        uv run jupyter notebook

Environment Configuration

    Obtain an API key from your preferred provider (OpenAI, Anthropic, or Google Gemini).

    Copy .env.example to .env:
    Bash

    cp .env.example .env

    Add your API key to .env:
    Fragmento de código

    OPENAI_API_KEY=your_api_key_here
    ANTHROPIC_API_KEY=your_api_key_here

For support, feature requests, or contributions, please open an issue in the GitHub repository or contact the Data & Cloud Academy team.