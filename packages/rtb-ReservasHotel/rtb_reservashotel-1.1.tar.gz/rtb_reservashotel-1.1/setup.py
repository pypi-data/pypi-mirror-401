from setuptools import setup, find_packages

setup(
    name="rtb_ReservasHotel",  # Nombre
    version="1.1",  # Versión de desarrollo
    description="Gestión de reservas Hotel",  # Descripción del funcionamiento
    author="Rubén Trillo",  # Nombre del autor
    author_email="rtbiota@gmail.com",  # Email del autor
    license="GPL",  # Licencia: MIT, GPL, GPL 2.0...
    packages=find_packages(),  # Paquetes a incluir
    install_requires=["PySide6"],  # Dependencias necesarias
    include_package_data=True,  # Incluir archivos de datos del paquete
    package_data={  # Archivos de datos específicos del paquete
        "ReservasHotel.modelo": ["*.db"],
    },
    entry_points={
        'console_scripts': [
            'hotel=ReservasHotel.rtb_principal:main',
        ],
    },
)
