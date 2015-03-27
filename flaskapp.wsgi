#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/fs/cs373-idb")

from FreeSpirits import app as application
application.secret_key = 'Add your secret key'
