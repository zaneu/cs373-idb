#!/bin/bash
# A setup script for the scraper

cd scraper
mkvirtualenv free_spirits_scraper
pip install -r requirements.txt
echo "All done!"
