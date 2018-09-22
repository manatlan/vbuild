import vbuild
import setuptools

setuptools.setup(
    name='vbuild',
    version=vbuild.__version__,

    author="manatlan",
    author_email="manatlan@gmail.com",
    description="A simple module to extract html/script/style from a vuejs '.vue' file (can minimize/es2015 compliant js) ... just py2 or py3, NO nodejs !",
    long_description=open("README.md","r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/manatlan/vbuild",
    py_modules=["vbuild"], #setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ),
    install_requires=[],
    keywords=['vuejs', 'vue', 'html', 'javascript', 'style', 'minimize', 'es2015'],
)
