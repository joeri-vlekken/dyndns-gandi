#! /path/to/.virtualenvs/dyndns-gandi/bin/python3

from app import app as application
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/path/to/application/')
application.secret_key = 'oareipgjeroiugheroiughreqoiguehioe'
