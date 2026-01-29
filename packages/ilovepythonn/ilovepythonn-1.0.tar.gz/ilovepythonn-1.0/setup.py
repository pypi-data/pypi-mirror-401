import setuptools
with open('README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='ilovepythonn',
	version='1.0',
	author='CtrlZett',
	author_email='Ivansharkov2012@gmail.com',
	description='The true love to python :D',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/SuperZombi/Pypi-uploader',
	packages=['ilovepythonn'],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.13',
)