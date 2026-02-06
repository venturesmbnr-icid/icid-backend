ICID - Backend
Creating a conda environment: 
1- make sure you are in the folder of your project 
2- conda create --prefix=.venvICIDBackend python=3.12 
3- conda info --envs #list of environments 
4- if the new environment does not have a name, add a name with: 
conda config --append envs_dirs /Users/mehdis/icid/icid-backend

5- active conda using: conda activate .venvICIDBackend

5.2- create requirement.txt: 
pip freeze > requirements.txt

5.5- to install all dependencies for the environment: conda install -r requirements.txt

6- python -m pytest

7- pytest --cov=src.core --cov-report=term-missing # for coverage or 8- python -m pytest --cov=src.core --cov-report=term-missing #src.core could just src

9- html coverage report: pytest --cov=src.core --cov-report=html open htmlcov/index.html

Updating requirement.txt
you can try: 
- pip install --upgrade --force-reinstall -r requirements.txt 
You can also ignore installed package and install the new one : 
- pip install --ignore-installed -r requirements.txt