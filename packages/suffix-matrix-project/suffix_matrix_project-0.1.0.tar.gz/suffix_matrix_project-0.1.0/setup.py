from setuptools import setup, find_packages

setup(
    name="suffix_matrix_project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Qui puoi elencare le dipendenze necessarie per far girare l'app
        "flask", 
    ],
)