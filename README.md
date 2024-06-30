# Trabajo Práctico de MSSCAE 2024 

[Diapositivas online](https://akielbowicz.github.io/tp-msscae-2024/diapositivas)

# Como usar el repo

### En un ambiente local

- Clonar el este repositorio `git clone https://github.com:akielbowicz/tp-msscae-2024.git`
- Crean un ambiente virtual `python -m venv .venv`
- Activar el ambiente virtual `source .venv/bin/activate` (unix), `./.venv/Scripts/Activate.ps1` (Windows Powershell)
- Instalar paquetes `python -m pip install -r requirements.txt`

### En el [Jupyter DC UBA](https://jupyter.dc.uba.ar/)

Para poder instalar paquetes en un ambiente virtual y no tener problemas de permisos

- Seguir los pasos de configuracion de un ambiente local
- Crear un nuevo kernel de jupyter con el ambiente recien creado `python -m ipykernell --user --name TPMSSCAE`
- Refescar el navegador
- Abrir un notebook y seleccionar el kernel `Kernel` -> `Change kernel` -> `TPMSSCAE` (por default usa Python 3)


# Contenidos

[Modelo Conceptual](docs/modelo_conceptual.md)

[Notebook MIP.ipynb](notebooks/MIP.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/akielbowicz/tp-msscae-2024/blob/main/notebooks/MIP.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/akielbowicz/tp-msscae-2024/HEAD?labpath=notebooks%2FMIP.ipynb)

[Notebook exposicion.ipynb](notebooks/exposicion.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/akielbowicz/tp-msscae-2024/blob/main/notebooks/exposicion.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/akielbowicz/tp-msscae-2024/HEAD?labpath=notebooks%2Fexposicion.ipynb)
 
## Cómo generar los documentos estáticos

```shell
jupyter nbconvert ./notebooks/exposicion.ipynb --to html --output-dir docs/diapositivas
jupyter nbconvert ./notebooks/exposicion.ipynb --to slides --output-dir docs/diapositivas
```

Para exportar a PDF es necesario tener un motor de [`TeX`](https://nbconvert.readthedocs.io/en/latest/install.html#installing-tex) (en Windows lo más sencillo es `scoop install main/miktex`)

```shell
jupyter nbconvert ./notebooks/exposicion.ipynb --to pdf --output-dir docs/diapositivas
```

