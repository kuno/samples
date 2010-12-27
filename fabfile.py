# coding: UTF8

#
# A simple fabric script that
# wrapping the google appengine sdk
# appcfg.py command line tool.
#


import urllib
import httplib

import os.walk

from os.path import join
from os.path import dirname
from os.path import basename

from fabric.api import *
from datetime import date

from perference import *

#==============================================================================
# Project profiles
#==============================================================================
# Appengine ID
ID = ''

# Project souce code repository
CODENAME = ''

# Proejct remote address
REMOTE_HOST = ''

# Project local address
LOCALE_HOST = ''

# Project directory
PROJECT_DIR = dirname(__file__)

# Setting file
PERFERENCE_FILE = join(dirname(__file__), '')

# Template file
BASE_LAYER = join(dirname(__file__), '')

# Index script
INDEX_SCRIPT = join(dirname(__file__), '')

# Javascript file dir
JS_DIR = join(dirname(__file__), '')

# CSS files dir
CSS_DIR = join(dirname(__file__), '')

# specified javascript code compressor
JS_COMPILER = 'google'

#==============================================================================
# Inner functions
#==============================================================================
def _list_files(root):
    """
    Filter directory for lists.
    """
    file_list = []
    for parent, subdirs, files in os.walk(root):
        for f in files:
            if not f.startswith('.'):
                p = join(parent, f)
                file_list.append(p)
            else:
                pass

    return file_list

#==============================================================================
# Tasks
#==============================================================================
def doctest():
    """
    Do local test.
    """


def compact():
    """
    Compact the javascript code.
    """
    js_files = _list_files(JS_DIR)
    css_files = _list_files(CSS_DIR)

    # Compress javascript code
    for p in js_files:
        f = basename(p)
        n = f.split('.')
        if len(n) >= 2 and n[-1] == 'js' and not n[-2] = 'min':
            if JS_COMPILER == 'yahoo':
                local("yuicompressor %s --type js -o %s" % 
                        (p, join(dirname(f),(n[0] + '.min.js')))
            else # use google closure
                local("closure --js %s --js_output_file %s" % 
                        (p, join(dirname(f),(n[0] + '.min.js')))
        else:
            pass

    # Compress css code
    # Warning: MAY demage the code 
    for p in css_files:
        f = basename(p)
        n = f.split('.')
        if len(n) >= 2 and n[-1] == 'css' and not n[-2] == 'min':
            local("yuicompressor %s --type css -o %s" % 
                    (p, join(dirname(f),(n('.')[0] + '.min.css')))
        else:
            pass     


def replace():
    """
    Replace all file for release.
    """


def debugon():
    """
    Turn debug mode on.
    """
    local("sed -i -e 's/debug=.*[^\)]\w/debug=True/'  %s" % (INDEX_SCRIPT)) 


def debugoff():
    """
    Turn debug mode off.
    """
    compact()
    local("sed -i -e 's/debug=.*[^\)]/debug=False/' %s" % (INDEX_SCRIPT))   


def localize():
    """
    Switch to local development mode.
    """
    host = "\"http:\/\/" + LOCALE_HOST + "\""
    local("sed -i -e 's/ajax\.googleapis\.com/lapi/' %s " % BASE_LAYER)
    local("sed -i -e 's/^HOST = .*/HOST = %s/' %s" %  (host, PERFERENCE_FILE))
    debugon()



def i18nize():
    """
    Prepare for releasing to the wild.
    """
    host = "\"http:\/\/" + REMOTE_HOST + "\""
    local("sed -i -e 's/lapi/ajax\.googleapis\.com/' %s " % BASE_LAYER)
    local("sed -i -e 's/^HOST = .*/HOST = %s' %s" % (host, PERFERENCE_FILE))
    debugoff()


def tag():
    """
    Make git tag and project revresion.
    """
    today = date.today().isoformat().replace('-', '')
    reversion = "\"" + today + "\""
    massage = ("\"reversion " + today + " ready for released.\"")
    local("git tag -a %s -m %s" % (reversion, massage))
    local("sed -i -e 's/REVERSION = .*/REVERSION = %s/' %s" % 
            (reversion, PERFERENCE_FILE))


def update():
    """
    Upload the application.
    """
    i18nize()
    local("appcfg.py --email=neokuno@gmail.com --passin update %s" % PROJECT_DIR)
    localize()


def rollback():
    """
    Rollback the previous update.
    """
    local("appcfg.py rollback %s" % PROJECT_DIR)

def downloadapp():
    """
    Download source code from google appengine.
    """
    local("appcfy.py --email=neokuno@gmail.com --passin update download_app -A %s %s" % (ID, PROJECT_DIR)


def start():
    """
    Start development server.
    """


def stop():
    """
    Stop development server.
    """


def restart():
    """
    Restart development server.
    """
#==============================================================================
# EOF
#==============================================================================
