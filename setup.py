from setuptools import setup, find_packages

setup(
    name='hink',
    version=None,
    author='hink',
    url='https://github.com/h1nk/',
    packages=find_packages(exclude=['tests', 'docs']),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 2.2',
    ],
)
