import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="epayco-django",
    version="0.1.0",
    include_package_data=True,
    license="MIT",
    description="A django integration for ePayco's gateway.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/gustav0/epayco_django",
    author="gustav0",
    author_email="tavito.286@gmail.com",
    packages=["epayco_django"],
    install_requires=[
        "requests",
        "epaycosdk>=2.0.0",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.5",
    zip_safe=False,
)
