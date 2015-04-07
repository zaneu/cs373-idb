#!/bin/bash
# This script setups a python dev environment for Macs
# @pybae

trap "Terminating" SIGINT SIGTERM

echo "Installing pyenv"
echo "================"
brew install pyenv

echo "Installing pyenv virtualenvwrapper"
echo "=================================="
brew install pyenv-virtualenvwrapper

echo "Installing Python 2.7.8"
echo "======================="
pyenv install 2.7.8

echo "Installing Python 3.4.2"
echo "======================="
pyenv install 3.4.2

echo "==================================================="
echo "All done!"
echo "pyenv is a python management tool"
echo "Here's what it does:"
echo ">>> pyenv"
pyenv

echo
echo "==================================================="
echo "You can install versions with install, change them with local or global and more"
echo "We've installed Python 2.7.8 and 3.4.2 for you already"
echo ">>> pyenv versions"
pyenv versions

echo
echo "==================================================="
echo "pyenv virtualenvwrapper is a pyenv extension that emulates virtualenvwrapper"
echo "running pyenv virtualenv wrapper will enable virtualenvwrapper commands"
echo "read more about virtualenvs here: http://docs.python-guide.org/en/latest/dev/virtualenvs/"
