import os
from setuptools import setup, find_packages


base_dir = os.path.dirname(__file__)

about = {}
with open(os.path.join(base_dir, "flake8_import_order", "__about__.py")) as f:
    exec(f.read(), about)


setup(
    name=about["__title__"],
    version=about["__version__"],

    description=about["__summary__"],
    license=about["__license__"],
    url=about["__uri__"],
    author=about["__author__"],
    author_email=about["__email__"],

    packages=find_packages(),
    zip_safe=False,

    install_requires=[
        "flake8"
    ],

    tests_require=[
        "pytest"
    ],

    py_modules=['flake8_import_order'],
    entry_points={
        'flake8.extension': [
            'I10 = flake8_import_order:ImportOrderChecker',
        ]
    },
)
