# 🎓 Guía del Estudiante: Entorno de Trabajo y Flujo con Git/GitHub

Bienvenido a la práctica. En esta asignatura utilizarás **Visual Studio Code, Git y GitHub** como tus herramientas principales de trabajo. Esta guía te explicará la metodología colaborativa que emplearemos y te guiará paso a paso desde la descarga del material base hasta la entrega de tus resultados.


## 🎯 Objetivos de este Entorno de Trabajo

1. **Aprender el flujo de trabajo profesional (Fork & Pull Request):** Trabajarás sobre tu propia copia remota del proyecto, simulando la colaboración real en equipos de desarrollo y ciencia de datos.
2. **Experimentación aislada:** Podrás modificar archivos, ejecutar experimentos y probar soluciones en tu entorno local sin riesgo de alterar o romper el repositorio base de la asignatura.
3. **Revisión y feedback unificado:** Al solicitar ayuda o entregar un ejercicio mediante un *Pull Request*, el profesor podrá auditar directamente las líneas exactas de código que has modificado en cualquier archivo del proyecto y dejarte comentarios precisos.

---

## 🛠️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado y configurado en tu equipo:

* [Visual Studio Code](https://code.visualstudio.com/) junto con las extensiones del lenguaje o entorno que indique la asignatura (ej. Python, Jupyter, Node.js).
* [Git](https://git-scm.com/) instalado en tu sistema operativo.
* Una cuenta personal activa en [GitHub](https://github.com/).

---

## 🚀 Paso a Paso: Flujo de Trabajo con VS Code

1. **Hacer Fork del Repositorio Base:** Crea tu copia personal en la nube.
1. Abre tu navegador e inicia sesión en **GitHub**.
2. Entra en la página del repositorio oficial proporcionada por el profesor.
3. En la esquina superior derecha de la pantalla, haz clic en el botón **Fork**.
4. Deja el nombre por defecto y selecciona **Create fork**. Esto creará una copia idéntica del proyecto dentro de tu cuenta personal (`[https://github.com/TU_USUARIO/nombre-del-proyecto](https://github.com/TU_USUARIO/nombre-del-proyecto)`).


2. **Clonar tu Repositorio en Local:** Descarga el proyecto a tu ordenador con VS Code.
1. Ve a tu repositorio forkeado en GitHub (`[https://github.com/TU_USUARIO/nombre-del-proyecto](https://github.com/TU_USUARIO/nombre-del-proyecto)`).
2. Haz clic en el botón verde **Code** y copia la URL HTTPS.
3. Abre **VS Code**.
4. Abre la paleta de comandos (`Ctrl + Shift + P` en Windows/Linux o `Cmd + Shift + P` en Mac), escribe `Git: Clone` y presiona *Enter*.
5. Pega la URL copiada y selecciona la carpeta de tu ordenador donde deseas guardar el proyecto.
6. Haz clic en **Open / Abrir** cuando VS Code te pregunte si deseas abrir el repositorio clonado.


3. **Configurar el Entorno de Trabajo:** Instala las herramientas del proyecto.
1. Abre la terminal integrada de VS Code (`Ctrl + ~` o `Menú > Terminal > New Terminal`).
2. Ejecuta los comandos de instalación de dependencias requeridos para la práctica.
3. Asegúrate de seleccionar el ejecutable o *kernel* correcto dentro de VS Code si estás trabajando con cuadernos de notas o scripts interactivos.


4. **Desarrollar la Práctica:** Resuelve las tareas asignadas.
1. Modifica los archivos de código o completa los cuadernos siguiendo las instrucciones de la asignatura.
2. Guarda tus cambios localmente en VS Code (`Ctrl + S` / `Cmd + S`).
3. Ejecuta tus pruebas locales para verificar que el código funciona correctamente.


5. **Guardar y Subir tus Cambios (Commit & Push):** Registra tus avances en la nube.
Guarda puntos de control periódicos de tu trabajo desde la terminal integrada de VS Code. La primera vez que ejecutes `push`, VS Code te pedirá autenticarte con tu cuenta de GitHub:

```bash
# 1. Preparar todos los archivos modificados
git add .

# 2. Registrar el punto de control con un mensaje explicativo
git commit -m "solucion: completa la tarea N"

# 3. Subir tus cambios a tu cuenta de GitHub
git push

```


6. **Entregar o Pedir Ayuda mediante Pull Request:** Solicita revisión o entrega la práctica.
Para entregar el trabajo o solicitar revisión sobre un error complejo que afecte a varios archivos:

1. Entra a tu repositorio forkeado en la web de GitHub.
2. Verás una barra que indica si tu repositorio tiene cambios nuevos. Haz clic en **Contribute** y después en **Open Pull Request**.
3. Escribe un título claro (ejemplo: *Entrega Práctica 1 - Nombre y Apellidos*) y describe brevemente los cambios realizados o tus dudas.
4. Haz clic en **Create Pull Request**.
5. El profesor podrá revisar de forma unificada en la pestaña **Files Changed** todos los archivos que has modificado y dejarte retroalimentación directamente sobre las líneas de código afectadas.


---

## 🔄 Cómo Actualizar tu Proyecto si el Profesor Modifica el Repositorio Base

Si el profesor añade nuevas plantillas, ejercicios o correcciones al proyecto original durante el curso, tu *Fork* no se actualizará automáticamente. Para traer las novedades a tu copia sin perder tu trabajo realizado, sigue estos sencillos pasos:

### Método A: Desde la Web de GitHub (Recomendado)

1. Entra en la página principal de tu *Fork* en GitHub (`[https://github.com/TU_USUARIO/nombre-del-proyecto](https://github.com/TU_USUARIO/nombre-del-proyecto)`).
2. Si el profesor ha subido cambios, verás un aviso que dice: *"This branch is X commits behind..."*.
3. Haz clic en el botón **Sync fork** y luego selecciona **Update branch**.
4. Abre la terminal en tu VS Code y descarga las novedades ejecutando:
```bash
git pull

```



### Método B: Desde la Terminal de VS Code

Si prefieres hacerlo mediante comandos:

```bash
# 1. Añadir el repositorio del profesor como fuente remota (solo la primera vez)
git remote add upstream https://github.com/URL-DEL-REPO-DEL-PROFESOR.git

# 2. Descargar e integrar las actualizaciones del profesor
git fetch upstream
git merge upstream/main

# 3. Subir la actualización a tu propio GitHub
git push

```

---

## ❓ Preguntas Frecuentes y Consejos

* **¿Necesito autenticarme en VS Code para descargar el proyecto?**
No. Puedes clonar tu repositorio público sin autenticarte. VS Code solo te solicitará iniciar sesión con GitHub cuando intentes hacer tu primer `git push`.
* **¿Cuándo debo hacer `git push`?**
Hazlo al finalizar cada ejercicio importante o al terminar la sesión de trabajo. De este modo mantendrás una copia de seguridad actualizada en la nube.
* **¿Se borrará o modificará mi trabajo si el profesor revisa mi Pull Request?**
No. Tu *Fork* es un entorno completamente independiente. El *Pull Request* es solo una herramienta de inspección y evaluación para el profesor.