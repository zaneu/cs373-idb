#!/bin/bash

echo "Generating Sphinx Documentation"

rm -rf html doc
sphinx-apidoc . --full -o doc -H 'FreeSpirits' -A 'FreeSpirits Team' -V '1.0'
cd doc
rm conf.py index.rst
wget https://gist.githubusercontent.com/pybae/f600f8cdbc1f6a0ffe4e/raw/f1fee5a19962d20f77a30af0e120edca1f9c4b97/conf.py
wget https://gist.githubusercontent.com/pybae/701c26ed77093e825fbd/raw/080ad84dd9af27ee256cf71b854b05098bb46196/index.rst

make html
mv _build/html ../html
cd ..

