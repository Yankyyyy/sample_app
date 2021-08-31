from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sample_app/__init__.py
from sample_app import __version__ as version

setup(
	name="sample_app",
	version=version,
	description="1st app",
	author="Yanky",
	author_email="tamocha44@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
