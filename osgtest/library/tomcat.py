import os
import time

import osgtest.library.core as core

def majorver():
    "Tomcat major version"
    if core.el_release() == 7:
        return 7
    if core.el_release() == 6:
        return 6
    else:
        return 5

def pkgname():
    "Name of the Tomcat package"
    if majorver() <= 6:
        return "tomcat" + str(majorver())
    return "tomcat"

def datadir():
    "Path of data directory of Tomcat"
    return os.path.join("/usr/share", pkgname())

def logdir():
    "Path of log directory of Tomcat"
    return os.path.join("/var/log", pkgname())

def sysconfdir():
    "Path of config directory of Tomcat (i.e. what is in /etc)"
    return os.path.join("/etc", pkgname())

def conffile():
    "Path of main config file of Tomcat"
    return os.path.join(sysconfdir(), pkgname() + ".conf")

def contextfile():
    "Path of main context.xml file of Tomcat"
    return os.path.join(sysconfdir(), 'context.xml')

def catalinafile():
    "Path of Catalina log file that contains the startup sentinel"
    if majorver() <= 6:
        return os.path.join(logdir(), 'catalina.out')
    else:
        return os.path.join(logdir(), 'catalina.%s.log' % time.strftime('%F', time.gmtime()))

def pidfile():
    "Path of pid file of a running Tomcat"
    return os.path.join("/var/run", pkgname() + ".pid")

def serverlibdir():
    "Path of the server libraries dir of Tomcat"
    if majorver() >= 6:
        return os.path.join(datadir(), "lib")
    else:
        return os.path.join(datadir(), "server/lib")

