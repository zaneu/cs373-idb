# Free Spirits

Mixed drink database and builder. Built for our Software
Engineering course.

## Group Members
* Paul Bae (@pybae)
* Zane Urbanski (@zaneu)
* Ali Homafar (@alih)
* Jin Dong Tang
* Larry Liu
* Menglin Liu

## Quick Setup

First, install pyenv, pyenv virtualenvwrapper, Python 2.7.8, and Python 3.4.0
The pip packages are found in [requirements.txt](requirements.txt) for the
main project and in [requirements.txt](scraper/requirements.txt). You can
install from the requirements with the following command:
```bash
pip install -r requirements.txt
```

We provide a script for Macs to install the required tools needed to install ([bootstrap.sh](scripts/bootstrap.sh)).

## Running

You can run the code (inside a virtualenv provided by the previous section) with
```bash
export PORT=5000
python wsgi.py
```

wsgi.py relies on the PORT environment variable, by default it is set to 80 (production).
We provide a script to set this up as well ([setup_dev.sh](scripts/setup_dev.sh))

To run the scraper, run the following command:
```bash
scrapy crawl ingredients
```

The tests can be run by the following command:
```bash
python tests.py
```

Or by simply navigating to the following link: (http://freespirits.me/api/tests)

## Outline
![UML Diagram](http://i.imgur.com/h11wLEz.jpg?1)
