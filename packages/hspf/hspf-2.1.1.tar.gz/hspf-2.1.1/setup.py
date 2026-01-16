from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import numpy

# This setup is configured for a 'src' layout
# The full name of the extension module is 'hspf.hbn_cy'
# and its source is located at 'src/hspf/hbn_cy.pyx'
extensions = [
    Extension(
        "hspf.hbn_cy",
        ["src/hspf/hbn_cy.pyx"],
        include_dirs=[numpy.get_include()],
    )
]

setup(
    name="hspf_package", # You can rename this to your project's name
    version="0.1.0",
    # Find packages in the 'src' directory
    packages=find_packages(where="src"),
    # Tell setuptools that the root package is in 'src'
    package_dir={"": "src"},
    ext_modules=cythonize(
        extensions,
        compiler_directives={'language_level': "3"},
        annotate=True # Optional: Creates a report showing C-code interactions
    ),
    # Cython extensions are not zip-safe
    zip_safe=False,
)