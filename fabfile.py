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
# Project profile
#==============================================================================
# Project souce code repository
PROJECT_NAME = {PROJECT_NAME}

# Project directory
PROJECT_DIR = os.path.dirname(__file__)

# Setting file
PERFERENCE_FILE = os.path.join(os.path.dirname(__file__), 'perference.py')

# Javascript file dir
JSFILEDIR = os.path.join(os.path.dirname(__file__), 'static/js')

# Javascript compiler
JSCOMPILER = 'closure-compiler.appspot.com'

#==============================================================================
# Inner functions
#==============================================================================
def _optimize_code(javascript_code):
    """
    Opitimize javascript code before publishing to the wild.
    """
    params = urllib.urlencode([
        ('js_code', javascript_code),
        ('compilation_level', 'WHITESPACE_ONLY'),
        ('output_format', 'text'),
        ('output_info', 'compiled_code'),
    ])
    # Always use the following value for the Content-type header.
    headers = { "Content-type": "application/x-www-form-urlencoded" }
    conn = httplib.HTTPConnection(JSCOMPILER)
    conn.request('POST', '/compile', params, headers)
    response = conn.getresponse()
    new_code = response.read()

    return new_code


def _replace_code(javascript_file):
    """
    Replace old, un-optimized js code with the  optimized code.
    """
    path = os.path.join(JSFILEDIR, javascript_file)
    old_code = open(path, 'r').read()
    new_code = _optimize_code(old_code)

    f = open(path, 'w+')
    f.write(new_code)
    f.close()

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
    file_list = os.listdir(JSFILEDIR)
    local("cd %s" % JSFILEDIR)   
    for f in file_list:
        local("cp %s/%s /tmp" % (JSFILEDIR, f))
        _replace_code(f)


def decompact():
    """
    Reverse of previous task.
    """
    file_list = os.listdir(JSFILEDIR)
    for f in file_list:
        local("mv /tmp/%s %s" % (f, JSFILEDIR))


def localize():
    """
    Switch to local development mode.
    """
    local("sed -i -e 's/ajax\.googleapis\.com/lapi/' %s " % BASE_LAYER)


def i18nize():
    """
    Switch to publish to wild mode.
    """
    local("sed -i -e 's/lapi/ajax\.googleapis\.com/' %s " % BASE_LAYER)

def update():
    """
    Upload the application.
    """
    reversion = "\"" + date.today().isoformat() + "\""
    local("sed -i -e 's/REVERSION = .*/REVERSION = %s/' %s" % 
          (reversion, PERFERENCE_FILE))
    compact()
    i18nize()  
    local("appcfg.py --email=neokuno@gmail.com --passin update %s" % PROJECT_DIR)
    decompact()
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
