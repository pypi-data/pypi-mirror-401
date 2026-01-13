#Se importan las funciones necesarias 
from setuptools import setup, find_packages

setup(
    #Nombre del paquete
    name="hotel-tatianlara",
    version="1.0.0",
    #Incluye automáticamente los paquetes necesarios
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt5"
    ],
    #Define los puntos de entrada
    entry_points={
        "console_scripts": [
            "hotel=hotel.principal:main"
        ]
    },
    author="Tatiana Lara Redondo",
    description="Aplicación realizada para la Tarea 3"
)
