# hnt_sap_nf_caixas
## Via transação J1BNFE (Monitor NF-e)
    J1BNFE
## Tipo de imposto - SAP
    (ICMS linha zero NF)
    (COFINS IVA SupNãoDedutImpNorm.)
    (PIS IVA SupNãoDedutImpNormal)
    (IPI NotaFisc Linha 0)

##  NF função parceiro
    AG = Emissor de ordem
    BR = Filial
    LF = Fornecedor
    RG = Pagador
    RE = Recebedor da fatura
    WE = Recebedor mercadoria
    SP = Transportadora

# Requirements
    Pip 24.0
    Python 3.11.5
    VirtualEnv

# Setup the development env unix
```sh
virtualenv venv
. ./venv/bin/activate
```

# Setup the development env win10
```sh
python -m venv venv
. .\venv\Scripts\activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python.exe -m pip install --upgrade pip
pip install pytest
pip install python-dotenv
pip install robotframework-sapguilibrary
copy .\.env.template .\.env
```

# Before publish the packages
```sh
pip install --upgrade pip
pip install --upgrade setuptools wheel
pip install twine
```
python.exe -m pip install --upgrade pip

# How to cleanup generated files to publish
```powershell
Remove-Item .\build\ -Force -Recurse
Remove-Item .\dist\ -Force -Recurse
Remove-Item .\hnt_sap_nf_caixas.egg-info\ -Force -Recurse
```

# How to publish the package to test.pypi.org
```sh
python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

# How to publish the package to pypi.org (username/password see lastpass Pypi)
```sh
python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```