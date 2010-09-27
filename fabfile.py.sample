from fabric.api import *

#==============================================================================
# Project profile
#==============================================================================
# Project name
PROJECT_NAME = ''
# Project souce code repository
PROJECT_REPOSITORY = ''

#==============================================================================
# Hosts
#==============================================================================
def prod():
    """Set the target to production."""
    env.hosts = [''] # change to domain, after register
    env.http_dir = '/home/kuno/http'
    env.app_dir = '/home/kuno/http/' + PROJECT_NAME
    env.settings_file = 'settings.py'
    env.admin_media = ''
    env.tag = 'production'

def test():
    """Set the target to local site."""
#==============================================================================
# Tasks
#==============================================================================
def test():
    """Do local test."""
    pass
    #TODO

def deploy():
    """First time deployment."""
    require('hosts', provided_by=[prod])
    require('http_dir', provided_by=[prod])
    require('app_dir', provided_by=[prod])
    require('admin_media', provided_by=[prod])
    require('tag', provided_by=[prod])

    local("hg tag --local --force %s" % env.tag)
    local("hg push")
    run("cd %s; hg clone %s" % (env.http_dir, PROJECT_REPOSITORY))
    run("cd %s; mkdir -p logs" % env.app_dir)
    run("cd %s; ln -s %s media" % (env.app_dir, app.admin_media))
    start()


def launch():
    """Re-launch the application."""
    require('hosts', provided_by=[prod])

    sudo("/etc/rc.d/fastcgi start")

def maintain():
    """Turn application into maintian stages."""
    require('hosts', provided_by=[prod])

    sudo("/etc/rc.d/fastcgi stop")

def start():
    """Start nginx."""
    require('hosts', provided_by=[prod])

    sudo("/etc/rc.d/nginx start")

def stop():
    """Stop nginx."""
    require('hosts', provided_by=[prod])

    sudo("/etc/rc.d/nginx stop")

def restart():
    """Restart nginx."""
    require('hosts', provided_by=[prod])

    sudo("/etc/rc.d/nginx restart")

def update():
    """Update the code from repository."""
    require('hosts', provided_by=[prod])
    require('app_dir', provided_by=[prod])
    require('settings_file', provided_by=[prod])
    require('tag', provided_by=[prod])

    local("hg tag --local --force %s" % env.tag)
    local("hg push")
    run("cd %s; hg pull" % env.app_dir)
    put(".hg/localtags", "%s/.hg/localtags" % env.app_dir)
    run("cd %s; hg update -C %s" % (env.app_dir, env.tag))
    put("%s" % env.settings_file, "%s/settings.py" % env.app_dir)
    run("cd %s;rm -rf *.pyc" % env.app_dir)
    restart()

def debugon():
    """Turn debug mode on for the server."""
    require('hosts', provided_by=[prod, test])
    require('app_dir', provided_by=[prod, test])
    require('settings_file', provided_by=[prod, test])

    run("cd %s; sed -i -e 's/DEBUG = .*/DEBUG = True/' %s" % 
        (env.app_dir, env.settings_file))
    run("cd %s; rm -rf *.pyc" % env.app_dir)
    restart()

def debugoff():
    """Turn debug mode off for the server."""
    require('hosts', provided_by=[prod, test])
    require('app_dir', provided_by=[prod, test])
    require('settings_file', provided_by=[prod, test])

    run("cd %s; sed -i -e 's/DEBUG = .*/DEBUG = False/' %s" % 
        (env.app_dir, env.settings_file))
    run("cd %s; rm -rf *.pyc" % env.app_dir)
    restart()
#==============================================================================
# EOF
#==============================================================================
