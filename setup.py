from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in print_permission/__init__.py
from print_permission import __version__ as version

setup(
	name="print_permission",
	version=version,
	description=" Control & limit document printing in ERPNext",
	author="DAS",
	author_email="DAS@digitalasiasolusindo.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
