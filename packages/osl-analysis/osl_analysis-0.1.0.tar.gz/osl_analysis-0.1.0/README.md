
# OSL_CGCD

Program for the deconvolution of OSL curves using the CGCD method.

## Author
**EDWIN JOEL PILCO QUISPE**  
Email: edwinpilco10@gmail.com

## Description
This package allows you to analyze and deconvolute OSL (Optically Stimulated Luminescence) curves using the CGCD method. It includes tools to process Excel files, fit curves, and save results.

## Installation
You can install the package from PyPI:

```bash
python -m pip install OSL_CGCD
```

Or install it locally from the generated `.whl` file:

```bash
cd dist
python -m pip install osl_cgcd-0.1.1-py3-none-any.whl
```

## Basic Usage
Create a script and use the included module:

```python
from OSL_CGCD import modulo
<<<<<<< HEAD
# Example: run analysis functions
=======
# Ejemplo de uso: ejecutar funciones de análisis
>>>>>>> 5882aa6f15235a4163d5a83757f74e2cb5de888b
```

## Package Structure

<<<<<<< HEAD
- `modulo.py`: Deconvolution of OSL curves from Excel files. Allows you to select the file to process and saves results in the `deconvolution_results` folder. Combines results from several columns into a single continuous file for further analysis.

## Example Execution
1. Run `modulo.py` to process your Excel file:
	```bash
	python src/OSL_CGCD/modulo.py
	```
=======
- `modulo1.py`: Deconvolución de curvas OSL a partir de archivos Excel. Permite seleccionar el archivo a procesar y guarda los resultados en la carpeta `deconvolution_results`. Combina los resultados de varias columnas en un solo archivo continuo para análisis posterior.

>>>>>>> 5882aa6f15235a4163d5a83757f74e2cb5de888b

## Publishing to PyPI
To publish a new version:
1. Update the version in `setup.py`.
2. Build the package:
	```bash
	python -m build
	```
3. Upload the package:
	```bash
	python -m twine upload dist/*
	```

## Requirements
- Python >= 3.6
- Recommended packages: numpy, scipy, matplotlib, pandas, prettytable

## License
This project is free to use for academic and personal purposes.
