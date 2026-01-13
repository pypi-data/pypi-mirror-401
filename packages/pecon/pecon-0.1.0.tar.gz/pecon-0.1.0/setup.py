from setuptools import setup, Extension, find_packages

extensions = [
    Extension(
        "pecon._core",
        sources=[
            "pecon/_core.c",
            "src/pecon.c",
        ],
        include_dirs=["include"],
    ),
    Extension(
        "pecon.models.correlation",
        sources=[
            "pecon/models/correlation.c",
            "src/pecon.c",
        ],
        include_dirs=["include"],
    ),
]

setup(
    name="pecon",
    version="0.1.0",
    packages=find_packages(),
    ext_modules=extensions,
)
