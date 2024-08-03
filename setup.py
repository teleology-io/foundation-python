import io
from setuptools import find_packages, setup

f = io.open("README.md", mode="r", encoding="utf-8")
long_description = f.read()

setup(
    name='teleology-foundation',
    packages=find_packages(include=['foundation']),
    version='{{VERSION_PLACEHOLDER}}',
    description='Python bindings for the Foundation Api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Foundation',
    author_email='support@teleology.io',
    license='MIT',
    install_requires=[
      'requests >= 2.23.2',
      'websocket-client >= 1.8.0'
    ]
)