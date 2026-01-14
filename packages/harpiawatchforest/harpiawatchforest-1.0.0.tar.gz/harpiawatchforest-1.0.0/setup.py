from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="HarpiaWatchForest",
    version="1.0.0",
    author="Elvis Garcia, Yubrany Gonzalez",
    author_email="",  # Agregar email si desean
    description="Sistema de detección de pérdida de cobertura vegetal mediante Google Earth Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",  # Agregar URL del repositorio si tienen
    project_urls={
        "Bug Tracker": "",  # Agregar si tienen
        "Documentation": "",  # Agregar si tienen
        "Source Code": "",  # Agregar si tienen
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Image Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "earthengine-api>=0.1.350",
    ],
    keywords=[
        "google earth engine",
        "remote sensing",
        "deforestation",
        "forest monitoring",
        "vegetation loss",
        "NDVI",
        "satellite imagery",
        "environmental monitoring",
        "Panama",
        "Ministerio de Ambiente"
    ],
)
