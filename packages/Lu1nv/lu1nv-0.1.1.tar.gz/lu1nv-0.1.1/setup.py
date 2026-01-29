from setuptools import setup, find_packages 

# Leer el conteido del arhcivo README.md
with open("README.md", "r", encoding="utf-8") as fh: 
    long_description = fh.read()

setup(
    name="Lu1nv",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    author="Luis E Martinez",
    description="Hola Solecito, prueba #2 para decirte te amoou. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)
