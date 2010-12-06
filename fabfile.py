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
PROJECT_CODENAME = 

#
REMOTE_HOST = 

#
LOCALE_HOST = 

# Project directory
PROJECT_DIR = os.path.dirname(__file__)

# Setting file
PERFERENCE_FILE = os.path.join(os.path.dirname(__file__), '')

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
        if not f.startswith('.') and f.split('.')[-1] == 'js':
            local("cp %s/%s %s/%s" % (JS_DIR, f, JS_DIR, '.'+f))
            if JS_COMPILER == 'yahoo':
                local("yuicompressor %s/%s --type js -o %s/%s" % 
                        (JS_DIR, '.'+f, JS_DIR, f))
            else # use google closure
            local("closure --js %s/%s --js_output_file %s/%s" % 
                    (JS_DIR, '.'+f, JS_DIR, f))
        else:
            pass

    # Compress css code
    # Warning: MAY demage the code 
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
    js_files = _list_files(JS_DIR)
    css_files = _list_files(CSS_DIR)

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


def localize():
    """
    Switch to local development mode.
    """
    host = "\"" + LOCALE_HOST + "\""
    decompact()
    local("sed -i -e 's/ajax\.googleapis\.com/lapi/' %s " % BASE_LAYER)
    local("sed -i -e 's/^HOST = .*/HOST = %s/' %s" %  (host, PERFERENCE_FILE))


def i18nize():
    """
    Prepare for releasing to the wild.
    """
    host = "\"" + REMOTE_HOST + "\""
    compact()
    local("sed -i -e 's/lapi/ajax\.googleapis\.com/' %s " % BASE_LAYER)
    local("sed -i -e 's/^HOST = .*/HOST = %s' %s" % (host, PERFERENCE_FILE))   


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


def debugon():
    """
    Turn debug mode on for the server.
    """


def debugoff():
    """
    Turn debug mode off for the server.
    """
#==============================================================================
# EOF
#==============================================================================
