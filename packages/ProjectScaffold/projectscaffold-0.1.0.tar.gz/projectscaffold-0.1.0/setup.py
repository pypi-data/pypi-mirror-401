from setuptools import setup, find_packages

setup(
    name='ProjectScaffold',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'project-scaffold=ProjectScaffold.cli:main',
        ],
    },
    python_requires='>=3.9',
    include_package_data=True,  # <-- add this
)
