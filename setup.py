import os
from setuptools import setup, find_packages


base_dir = os.path.dirname(__file__)

about = {}
with open(os.path.join(base_dir, "flake8_import_order", "__about__.py")) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()


setup(
    name=about["__title__"],
    version=about["__version__"],

    description=about["__summary__"],
    long_description=long_description,
    license=about["__license__"],
    url=about["__uri__"],
    author=about["__author__"],
    author_email=about["__email__"],
    maintainer=about['__maintainer__'],
    maintainer_email=about['__maintainer_email__'],

    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,

    install_requires=[
        "enum34 ;  python_version <= '2.7'",
        "pycodestyle",
        "setuptools",
    ],

    tests_require=[
        "pytest",
        "flake8",
        "pycodestyle",
        "pylama"
    ],

    py_modules=['flake8_import_order'],
    entry_points={
        'flake8_import_order.styles': [
            'cryptography = flake8_import_order.styles:Cryptography',
            'google = flake8_import_order.styles:Google',
            'pep8 = flake8_import_order.styles:PEP8',
            'smarkets = flake8_import_order.styles:Smarkets',
            'appnexus = flake8_import_order.styles:AppNexus',
            'edited = flake8_import_order.styles:Edited',
            'pycharm = flake8_import_order.styles:PyCharm',
        ],
        'flake8.extension': [
            'I = flake8_import_order.flake8_linter:Linter',
        ],
        'pylama.linter': [
            'import_order = flake8_import_order.pylama_linter:Linter'
        ]
    },

    classifiers=[
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        (
            "License :: OSI Approved :: "
            "GNU Lesser General Public License v3 (LGPLv3)"
        ),
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Operating System :: OS Independent"
    ]
)
