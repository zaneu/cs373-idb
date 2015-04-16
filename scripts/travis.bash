#!/bin/bash

check_file () {
    if [ -f "$1" ]
    then
        echo "$1 found"
    else
        echo "$1 not found"
        exit -1
    fi
}

echo "Checking for all files"

check_file "UML.pdf"
check_file "apiary.apib"
check_file "IDB.log"
check_file "tests.py"
check_file "tests.out"
check_file "config.py"
check_file "populate.py"
check_file "wsgi.py"

cd data
check_file "drinks.json"
check_file "ingredients.json"
check_file "remove_duplicate_drinks.py"
check_file "remove_duplicate_ingredients.py"
cd ..

cd scripts
check_file "bootstrap.sh"
check_file "setup_dev.sh"
check_file "setup_scraper.sh"
check_file "travis.bash"
cd ..

cd FreeSpirits
check_file "__init__.py"
check_file "models.py"
check_file "views.py"
cd ..

echo "Running tests"

python tests.py > tests.out

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

echo "Making IDB.log"

commit_message=`git log -1 --pretty=%B`
git log > IDB.log
git add -A
git commit -m "Added IDB.log (Travis CI)"
git reset --hard HEAD~1
git commit -m "$commit_message"
git push

echo "Done."
