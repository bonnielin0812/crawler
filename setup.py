# setup.py

from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    # Extension("src.crawlerPath.func.service", ["src/crawlerPath/func/service.py"]),
    # Extension("src.crawlerPath.func.downloadPDF", ["src/crawlerPath/func/downloadPDF.py"]),
    Extension("crawler", ["crawler.py"])

]

setup(
    name='crawler',
    ext_modules=cythonize(extensions),
)