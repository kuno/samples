# coding: UTF8

#
# A simple fabric script that
# wrapping the google appengine sdk
# appcfg.py command line tool.
#

import os
import urllib
import httplib
import os.path

from fabric.api import *
from datetime import date

from perference import *

#==============================================================================
# Project profiles
#==============================================================================
# Project souce code repository
CODENAME = ''

# Proejct remote address
REMOTE_HOST = ''

# Project local address
LOCALE_HOST = ''

# Project directory
PROJECT_DIR = os.path.dirname(__file__)

# Setting file
PERFERENCE_FILE = os.path.join(os.path.dirname(__file__), '')

# Template file
BASE_LAYER = os.path.join(os.path.dirname(__file__), '')

# Index script
INDEX_SCRIPT = os.path.join(os.path.dirname(__file__), '')

# Javascript file dir
JS_DIR = os.path.join(os.path.dirname(__file__), '')

# CSS files dir
CSS_DIR = os.path.join(os.path.dirname(__file__), '')

# specified javascript code compressor
JS_COMPILER = 'google'

#==============================================================================
# Inner functions
#==============================================================================
def _list_files(dir):
    """
    Filter directory for lists.
    """
    files = []
    for f in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, f)):
            files.append(f)
        else:
            pass

    return files

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
    for f in js_files:
        if not f.startswith('.') and not f.split('.')[-2] = 'min' and f.split('.')[-1] == 'js':
            if JS_COMPILER == 'yahoo':
                local("yuicompressor %s/%s --type js -o %s/%s" % 
                        (JS_DIR, f, JS_DIR, f.split('.')[0] + '.min.js'))
            else # use google closure
                local("closure --js %s/%s --js_output_file %s/%s" % 
                        (JS_DIR, f, JS_DIR, f.split('.')[0] + '.min.js'))
        else:
            pass

    # Compress css code
    # Warning: MAY demage the code 
    for f in css_files:
        if not f.startswith('.') and not f.split('.')[-2] == 'min' and f.split('.')[-1] == 'css':
            local("yuicompressor %s/%s --type css -o %s/%s" % 
                    (CSS_DIR, f, CSS_DIR, f.split('.')[0] + '.min.css'))
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
