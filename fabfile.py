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
PROJECT_CODENAME = {}

#
REMOTE_HOST = {}

#
LOCALE_HOST = {}

# Project directory
PROJECT_DIR = os.path.dirname(__file__)

# Setting file
PERFERENCE_FILE = os.path.join(os.path.dirname(__file__), 'perference.py')

# Javascript file dir
JS_DIR = os.path.join(os.path.dirname(__file__), 'static/js')

# Javascript compiler
JS_COMPILER = 'closure-compiler.appspot.com'

#==============================================================================
# Inner functions
#==============================================================================
def _compress_Js_code(javascript_code):
    """
    Compress javascript code for better performance.
    """
    params = urllib.urlencode([
        ('js_code', javascript_code),
        ('compilation_level', 'WHITESPACE_ONLY'),
        ('output_format', 'text'),
        ('output_info', 'compiled_code'),
    ])
    # Always use the following value for the Content-type header.
    headers = { "Content-type": "application/x-www-form-urlencoded" }
    conn = httplib.HTTPConnection(JS_COMPILER)
    conn.request('POST', '/compile', params, headers)
    response = conn.getresponse()
    new_code = response.read()

    return new_code


def _replace_js_file(javascript_file):
    """
    Replace old, un-optimized js file with the compressed file.
    """
    path = os.path.join(JS_DIR, javascript_file)
    old_code = open(path, 'r').read()
    new_code = _compress_js_code(old_code)

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
    files = os.listdir(JS_DIR)
    for f in files:
        if not f.startswith('.') and f.split('.')[-1] == 'js':
            local("cp %s/%s %s/%s" % (JS_DIR, f, JS_DIR, '.'+f))
            _replace_js_file(f)
        else:
            pass


def decompact():
    """
    Reverse of previous task.
    """
    files = os.listdir(JS_DIR)
    for f in files:
        if f.startswith('.') and f.split('.')[-1] == 'js':
            local("cp %s/%s %s/%s" % (JS_DIR, f, JS_DIR, f.lstrip('.')))
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
