# Fuzzing Framework - J2

## 1. Descripción

Este proyecto proporciona un entorno reproducible para la ejecución de las herramientas de fuzzing seleccionadas durante la fase J1 del proyecto.

Las herramientas incluidas inicialmente son:

- **boofuzz**, para fuzzing de protocolos de red.
- **Fuzzware**, para fuzzing de firmware mediante emulación.

El objetivo de este entorno es disponer de las herramientas preparadas para poder realizar las pruebas sin tener que configurar manualmente el entorno en cada ejecución. Además, se incluyen ejemplos mínimos de ejecución y resultados de prueba que permiten comprobar que las herramientas funcionan correctamente.

---

## 2. Arquitectura del entorno

Para el desarrollo del entorno se ha seleccionado una **máquina virtual con Ubuntu 24.04 LTS** como sistema base.

La elección de una máquina virtual permite aislar el entorno de fuzzing del sistema principal y facilita su reproducción en otros equipos.

Fuzzware utiliza adicionalmente **Docker**, ya que requiere un entorno específico debido a sus dependencias y a la versión de las herramientas utilizadas internamente. Por este motivo, Fuzzware se ejecuta mediante su propio entorno Docker, mientras que boofuzz se ejecuta directamente sobre Python en la máquina virtual.

La arquitectura utilizada es, por tanto:

```text
Máquina virtual Ubuntu 24.04
│
├── boofuzz
│   └── Python virtual environment
│
└── Fuzzware
    └── Docker
        └── Fuzzware environment
```

---

## 3. Requisitos

El entorno requiere:

- Ubuntu 24.04 LTS.
- Git.
- Python 3.
- Python virtual environment.
- Docker Engine.
- Conexión a Internet durante la instalación y la primera preparación de Fuzzware.

El repositorio contiene Fuzzware como un **Git submodule**, por lo que debe clonarse incluyendo los submódulos.

---

## 4. Descarga del proyecto

Para obtener el proyecto completo, incluyendo el código de Fuzzware, ejecutar:

```bash
git clone --recurse-submodules https://github.com/junelizarraga/fuzzing-framework.git
cd fuzzing-framework
```

Si el repositorio ya se ha clonado sin utilizar `--recurse-submodules`, se pueden inicializar los submódulos posteriormente mediante:

```bash
git submodule update --init --recursive
```

La versión de Fuzzware utilizada queda fijada mediante el commit almacenado en el submódulo.

---

## 5. Instalación del entorno

El proyecto incluye el script `install.sh`, encargado de instalar las dependencias básicas del sistema.

Desde la raíz del proyecto:

```bash
chmod +x install.sh
./install.sh
```

El script instala las dependencias necesarias para trabajar con Python, Git y las herramientas de compilación utilizadas por el entorno.

Docker debe estar instalado y disponible para el usuario que vaya a ejecutar Fuzzware.

Para comprobar que Docker funciona:

```bash
docker --version
```

También se puede comprobar la ejecución de un contenedor mediante:

```bash
docker run hello-world
```

Si Docker requiere permisos de administrador, se debe añadir el usuario al grupo `docker` y volver a iniciar sesión:

```bash
sudo usermod -aG docker $USER
```

Después de iniciar una nueva sesión, comprobar de nuevo:

```bash
docker run hello-world
```

---

# 6. boofuzz

## 6.1. Descripción

boofuzz es un framework de fuzzing de protocolos que permite definir mediante Python la estructura de los mensajes que se envían al sistema bajo prueba.

En este proyecto se utiliza la versión:

```text
boofuzz 0.4.2
```

La versión se fija mediante el archivo:

```text
boofuzz/requirements.txt
```

cuyo contenido incluye:

```text
boofuzz==0.4.2
```

---

## 6.2. Preparación

Desde la raíz del proyecto se crea un entorno virtual de Python:

```bash
python3 -m venv boofuzz/venv
```

Se activa mediante:

```bash
source boofuzz/venv/bin/activate
```

Y se instalan las dependencias:

```bash
pip install -r boofuzz/requirements.txt
```

Para comprobar la versión instalada:

```bash
pip show boofuzz
```

---

## 6.3. Ejemplo mínimo

El proyecto incluye un ejemplo mínimo de boofuzz formado por:

```text
boofuzz/examples/minimal.py
boofuzz/examples/server.py
```

El servidor de prueba escucha en el puerto TCP 9999 y recibe los mensajes enviados por boofuzz.

Primero se debe iniciar el servidor.

En una terminal:

```bash
cd ~/fuzzing-framework
source boofuzz/venv/bin/activate
python boofuzz/examples/server.py
```

El servidor permanecerá ejecutándose y mostrará los mensajes recibidos.

En una segunda terminal, desde la raíz del proyecto, activar también el entorno virtual:

```bash
cd ~/fuzzing-framework
source boofuzz/venv/bin/activate
```

A continuación ejecutar:

```bash
python boofuzz/examples/minimal.py
```

boofuzz comenzará la campaña de fuzzing contra el servidor local.

Para detener la ejecución:

```text
Ctrl+C
```

---

## 6.4. Guardado de resultados

Para guardar una ejecución del ejemplo mínimo se puede utilizar:

```bash
timeout 20s python boofuzz/examples/minimal.py > boofuzz/results/boofuzz-minimal-$(date +%F).txt 2>&1
```

El resultado se almacena en:

```text
boofuzz/results/
```

En el repositorio se incluye una ejecución de referencia comprimida:

```text
boofuzz/results/boofuzz-minimal-2026-10-08.txt.gz
```

El archivo se encuentra comprimido debido al gran tamaño que puede alcanzar la salida generada durante una campaña de fuzzing.

---

# 7. Fuzzware

## 7.1. Descripción

Fuzzware es una herramienta orientada al fuzzing de firmware de microcontroladores mediante emulación.

En este proyecto se utiliza el repositorio oficial de Fuzzware como Git submodule.

El submódulo se encuentra en:

```text
fuzzware/
```

La versión utilizada queda fijada mediante el commit almacenado por Git en el repositorio principal.

---

## 7.2. Entorno Docker

Fuzzware proporciona su propio entorno Docker debido a las dependencias específicas necesarias para ejecutar la herramienta.

Desde el directorio del submódulo:

```bash
cd fuzzware
```

Construir la imagen Docker:

```bash
./build_docker.sh
```

Una vez construida la imagen, comprobar que está disponible:

```bash
docker images
```

---

## 7.3. Ejemplo mínimo

Fuzzware incluye ejemplos dentro de su propio repositorio.

Para ejecutar el ejemplo de `pw-recovery`:

```bash
./run_docker.sh examples fuzzware pipeline --skip-afl-cpufreq pw-recovery/ARCH_PRO
```

Durante la ejecución se muestran por pantalla diferentes datos de la campaña de fuzzing, incluyendo información sobre cobertura, bloques básicos, ejecuciones y posibles crashes.

La ejecución puede detenerse mediante:

```text
Ctrl+C
```

---

## 7.4. Ejecución controlada y guardado de resultados

Para realizar una ejecución limitada temporalmente y guardar la salida en el directorio de resultados del proyecto:

Desde:

```text
~/fuzzing-framework/fuzzware
```

ejecutar:

```bash
mkdir -p ../results
timeout 60s ./run_docker.sh examples fuzzware pipeline --skip-afl-cpufreq pw-recovery/ARCH_PRO > ../results/fuzzware-quickstart-$(date +%F).txt 2>&1
```

El resultado queda almacenado en:

```text
~/fuzzing-framework/results/
```

El repositorio contiene una ejecución de referencia:

```text
results/fuzzware-quickstart-2026-10-08.txt
```

---

# 8. Estructura del proyecto

La estructura principal del proyecto es:

```text
fuzzing-framework/
│
├── README.md
├── install.sh
├── .gitignore
│
├── boofuzz/
│   ├── requirements.txt
│   ├── examples/
│   │   ├── minimal.py
│   │   └── server.py
│   ├── results/
│   │   ├── boofuzz-environment-2026-10-08.txt
│   │   └── boofuzz-minimal-2026-10-08.txt.gz
│   └── venv/
│
├── boofuzz-results/
│   └── ...
│
├── fuzzware/
│   └── ...
│
└── results/
    └── fuzzware-quickstart-2026-10-08.txt
```

El directorio `fuzzware/` corresponde al repositorio oficial incorporado como Git submodule.

El entorno virtual de Python de boofuzz (`boofuzz/venv/`) no se incluye en Git, ya que se genera durante la instalación.

---

# 9. Resultados de referencia

El repositorio contiene resultados obtenidos durante la validación del entorno.

Estos resultados permiten comprobar que ambas herramientas han sido instaladas y que sus ejemplos mínimos pueden ejecutarse.

Los resultados incluidos son:

- **boofuzz**: ejecución del ejemplo mínimo contra el servidor local.
- **Fuzzware**: ejecución del ejemplo `pw-recovery/ARCH_PRO` mediante Docker.

Cada resultado incluye la fecha de ejecución en su nombre.

---

# 10. Comprobación del entorno

Para comprobar que el entorno funciona correctamente se deben realizar las siguientes pruebas:

boofuzz
1. Activar el entorno virtual.
2. Ejecutar `server.py`.
3. Ejecutar `minimal.py`.
4. Comprobar que boofuzz inicia la campaña de fuzzing.
5. Comprobar que el servidor recibe las conexiones.

Fuzzware
1. Acceder al directorio `fuzzware`.
2. Construir la imagen Docker.
3. Ejecutar el ejemplo `pw-recovery/ARCH_PRO`.
4. Comprobar que comienza la ejecución del pipeline.
5. Comprobar que se muestran datos de ejecución y cobertura.

La reproducción del entorno se considera correcta cuando ambas herramientas pueden ejecutarse siguiendo únicamente las instrucciones de este documento.

---

# 11. Versiones utilizadas

| Componente | Versión / referencia |
|---|---|
| Sistema operativo | Ubuntu 24.04 LTS |
| boofuzz | 0.4.2 |
| Fuzzware | Commit fijado en el Git submodule |
| Python | Python 3 |
| Docker | Docker Engine |

Las versiones de las herramientas de fuzzing se mantienen fijadas para evitar cambios de comportamiento derivados de actualizaciones posteriores.
