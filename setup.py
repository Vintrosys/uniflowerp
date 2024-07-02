from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in uniflowerp/__init__.py
from uniflowerp import __version__ as version

setup(
	name="uniflowerp",
	version=version,
	description="Uniflow ERP",
	author="Swerved Right",
	author_email="kaviyaperiyasamy22@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
