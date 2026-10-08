FUZZING FRAMEWORK - J2

1.Descripción

Este proyecto proporciona un entorno reproducible para la ejecución de las herramientas de fuzzing seleccionadas en la fase J1.
Las herramientas incluidas son: boofuzz, fuzzware.

El objetivo es permitir que una tercera persona pueda preparar el entorno y ejecutar los ejemplos mínimos de cada herramienta siguiendo únicamente las instrucciones de este documento.


2.Entorno

El entorno se ejecuta sobre una máquina virtual con Ubuntu 24.04.5 LTS, Python 3, Docker y Git.
Se utiliza una máquina virtual para aislar el entorno de ejecución y facilitar su reproducción.


3.Estructura

fuzzing-framework/
|--README.md
|--install.sh
|--boofuzz/
   |--requirements.txt
   |--examples/
	|--minimal.py
        |--server.py
   |--results/
   |--venv/
|--fuzzware/
   |--examples/
   |--results/
   |--Dockerfile
   |--build_docker.sh
   |--run_docker.sh

4.Instalación

La instalación de dependencias se realiza mediante :
chmod +x install.sh
./install.sh


5.Ejecución

Las instrucciones específicas para cada herramienta se encuentran en sus correspondientes apartados.


6.Resultados

Los resultados de las ejecuciones se almacenan en las carpetas results/ de cada herramienta.
Cada resultado incluye el nombre de la herramienta y la fecha de ejecución.
