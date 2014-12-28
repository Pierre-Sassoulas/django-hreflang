# -*- coding: utf-8 -*-

"""
	for installing with pip
"""

from distutils.core import setup
from setuptools import find_packages

setup(
	name='django_hreflang',
	version='0.1.0',
	author='Mark V',
	author_email='noreply.mail.nl',
	packages=find_packages(),
	include_package_data=True,
	url='git+https://bitbucket.org/mverleg/django_hreflang',
	license='Revised BSD License (LICENSE.txt)',
	description='Generate the hreflang html header lines when using i18n urls',
	zip_safe=True,
	install_requires = [
		'django',
	],
)
