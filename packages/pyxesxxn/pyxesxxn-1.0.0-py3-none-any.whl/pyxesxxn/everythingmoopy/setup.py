import numpy
import setuptools

setuptools.setup(
    name="pymoo",
    packages=setuptools.find_packages(),
    include_dirs=[numpy.get_include()],
)
