from setuptools import setup, find_packages

setup(
    name='polymetre',
    version='1.0',
    packages=find_packages(),
    install_requires=['numpy', 'sounddevice'],
    url='',
    license='',
    author='gyro',
    author_email='',
    description='',
    python_requires='>=3',
    entry_points={
        'gui_scripts': [
            'polymetre=polymetre.__main__:main',
        ],
    },
    include_package_data=True,
)
