import numpy
from Cython.Build import cythonize
from Cython.Compiler import Options
from setuptools import Extension, setup

# These are optional
Options.docstrings = True
Options.annotate = False

# Modules to be compiled and include_dirs when necessary
extensions = [
    Extension(
        "xradar.io.backends.nexrad_interpolate",
        sources=["xradar/io/backends/nexrad_interpolate.pyx"],
        include_dirs=[numpy.get_include()],
    ),
]


# This is the function that is executed
setup(
    name="xradar",  # Required
    # external to be compiled
    ext_modules=cythonize(
        extensions, compiler_directives={"language_level": "3", "cpow": True}
    ),
)
