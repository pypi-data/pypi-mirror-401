from setuptools import setup, find_packages

setup(name='hnt_sap_nf_caixas',
    version='0.0.3',
    license='MIT License',
    author='Pepe',
    keywords='nota_fiscal',
    description=u'Lib to access sap gui to run transactions',
    packages=find_packages(),
    package_data={'hnt_sap_nf': ['common/*']},
    install_requires=[
    'python-dotenv',
    'robotframework-sapguilibrary',
    ])