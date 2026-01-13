from setuptools import setup, find_packages

# Lecture du README pour la description longue sur PyPI
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='surf_scrap_cli',
    version='1.0.1',
    author='Céline ADOUSSINGANDE, Loukmane BOULANKI, Isaac BESSANH',
    author_email='mauriceteadoussinande@yahoo.com',
    description='Extraction des données météo surf depuis surf-report.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/votre-username/surf_scrap',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests>=2.25.0',
        'beautifulsoup4>=4.9.0',
        'pandas>=1.2.0',
        'lxml>=4.6.0'
    ],
    # Permet d'exécuter la bibliothèque directement via le terminal
    entry_points={
        'console_scripts': [
            'surf-scrap=surf_scrap.scraper:extract_surf_data',
        ],
    },
    include_package_data=True,
)