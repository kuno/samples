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
# Project settings
#==============================================================================
# Project souce code repository
PROJECT_CODENAME = ''

#
REMOTE_HOST = ''

#
LOCALE_HOST = ''

# Project directory
PROJECT_DIR = os.path.dirname(__file__)

# Main file
MAIN_FILE = os.path.join(os.path.dirname(__file__), 'main.py')

# Setting file
PERFERENCE_FILE = os.path.join(os.path.dirname(__file__), 'perference.py')

# Javascript file dir
JS_DIR = os.path.join(os.path.dirname(__file__), 'static/js')

# CSS files didr

CSS_DIR = os.path.join(os.path.dirname(__file__), 'static/css')

# Choose javascript code comppler 
JS_COMPILER = '

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
    js_files = os.listdir(JS_DIR)
    css_files = os.listdir(CSS_DIR)

    # Compress javascript code
    for f in js_files:
        if not f.startswith('.') and f.split('.')[-1] == 'js':
            local("cp %s/%s %s/%s" % (JS_DIR, f, JS_DIR, '.'+f))
            local("yuicompressor %s/%s --type js -o %s/%s" % 
                    (JS_DIR, '.'+f, JS_DIR, f))
        else:
            pass

    # Compress css code
    for f in css_files:
        if not f.startswith('.') and f.split('.')[-1] == 'css':
            local("cp %s/%s %s/%s" % (CSS_DIR, f, CSS_DIR, '.'+f))
            local("yuicompressor %s/%s --type css -o %s/%s" % 
                    (CSS_DIR, '.'+f, CSS_DIR, f))
        else:
            pass     


def decompact():
    """
    Reverse of previous task.
    """
    js_files = os.listdir(JS_DIR)
    css_files = os.listdir(CSS_DIR)

    # Recover js files
    for f in js_files:
        if f.startswith('.') and f.split('.')[-1] == 'js':
            local("cp %s/%s %s/%s" % (JS_DIR, f, JS_DIR, f.lstrip('.')))
        else:
            pass
    # Recover css files
    for f in css_files:
        if f.startswith('.') and f.split('.')[-1] == 'css':
            local("cp %s/%s %s/%s" % (CSS_DIR, f, CSS_DIR, f.lstrip('.')))
        else:
            pass


def debugon():
    """
    Turn debug mode on.
    """
    local("sed -i -e 's/debug=.*[^\)]\w/debug=True/'  %s" % (MAIN_FILE))


def debugoff():
    """
    Turn debug mode off.
    """
    local("sed -i -e 's/debug=.*[^\)]/debug=False/' %s" % (MAIN_FILE))


def localize():
    """
    Switch to local development mode.
    """
    host = "\"" + LOCALE_HOST + "\""
    debugon()
    decompact()
    local("sed -i -e 's/ajax\.googleapis\.com/lapi/' %s " % BASE_LAYER)
    local("sed -i -e 's/^HOST = .*/HOST = %s/' %s" %  (host, PERFERENCE_FILE))


def i18nize():
    """
    Change javascript library to google js api.
    """
    host = "\"" + REMOTE_HOST + "\""
    debugoff()
    compact()
    local("sed -i -e 's/lapi/ajax\.googleapis\.com/' %s" % BASE_LAYER)
    local("sed -i -e 's/^HOST = .*/HOST = %s/' %s" % (host, PERFERENCE_FILE))   


def update():
    """
    Upload the application.
    """
    reversion = "\"" + date.today().isoformat() + "\""
    local("sed -i -e 's/REVERSION = .*/REVERSION = %s/' %s" % 
            (reversion, PERFERENCE_FILE))
    i18nize()
    local("appcfg.py --email=neokuno@gmail.com --passin update %s" % PROJECT_DIR)
    localize()

def rollback():
    """
    Rollback the previous update.
    """
    local("appcfg.py rollback %s" % PROJECT_DIR)


def start():
    """Start development server."""


def stop():
    """Stop development server."""


def restart():
    """Restart development server."""
#==============================================================================
# EOF
#==============================================================================
