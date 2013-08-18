from ConfigParser import NoSectionError, NoOptionError
import os

from zope.interface import moduleProvides

from carapace.config import Config
from carapace.sdk import interfaces

from hydeyhole.config import HydeyHoleConfigurator, main, ssh

from hyasynth import meta


moduleProvides(interfaces.IConfig)


# SuperCollider external settings
scext = Config()
scext.host = "127.0.0.1"
scext.port = 57110
scext.servicename = "External SC Process"

# SuperCollider internal settings
scint = Config()
# XXX add the following to the configuration setup below
scint.binary = "/usr/local/bin/scsynth"
scint.defaultboot = False
scint.host = "127.0.0.1"
scint.port = 57111
scint.spawnport = 57112
scint.servicename = "Internal SC Process"

# SuperCollider in-memory settings; these are not saved in a configuration file.
# The default is to use the external settings; if one manually boots a SC server
# using the API, this values will be over-written at that time with the values
# passed to the boot function(s).
sc = Config()
sc.host = scext.host
sc.port = scext.port

# Main
main.config.datadir = os.path.expanduser("~/.%s" % meta.library_name)
main.config.localfile = "config.ini"
main.config.installedfile = os.path.join(
    main.config.datadir, main.config.localfile)


# SSH Server for game
ssh.servicename = meta.description
ssh.port = 19322
ssh.keydir = os.path.join(main.config.datadir, "ssh")
ssh.userdirtemplate = os.path.join(main.config.datadir, "users", "{{USER}}")
ssh.userauthkeys = os.path.join(ssh.userdirtemplate, "authorized_keys")
ssh.banner = """: Welcome to
:  _  _                       _   _
: | || |_  _ __ _ ____  _ _ _| |_| |_
: | __ | || / _` (_-< || | ' \  _| ' \\
: |_||_|\_, \__,_/__/\_, |_||_\__|_||_|
:       |__/         |__/
: {{WELCOME}}{{HELP}}
:
: Enjoy!
:"""
ssh.banner_welcome = """
: You have logged onto a Hyasynth Server; you are currently at a Hy
: command prompt. Hy is a Lisp dialect of Python of which you can
: learn more about here:
:   https://github.com/hylang/hy
: Information on Hyasynth is available here:
:   http://github.com/oubiwann/hyasynth
"""


class HyasynthConfigurator(HydeyHoleConfigurator):
    """
    """
    def __init__(self, main, ssh, scint, scext):
        super(HyasynthConfigurator, self).__init__(main, ssh)
        self.scext = scext
        self.scint = scint

    def buildDefaults(self):
        config = super(HyasynthConfigurator, self).buildDefaults()
        config.set("SSH", "welcome", self.ssh.welcome)
        config.set("SSH", "banner_welcome", self.ssh.banner_welcome)
        config.add_section("SuperCollider")
        config.set("SuperCollider External", "host", self.scext.host)
        config.set("SuperCollider External", "port", self.scext.port)
        config.set("SuperCollider Internal", "host", self.scint.host)
        config.set("SuperCollider Internal", "port", self.scint.port)
        return config

    def updateConfig(self):
        config = super(HyasynthConfigurator, self).updateConfig()
        if not config:
            return
        ssh = self.ssh
        scext = self.scext
        scint = self.scint
        ssh.banner_welcome = config.get("SSH", "banner_welcome")
        scext.host = config.get("SuperCollider External", "host")
        scext.port = config.get("SuperCollider External", "port")
        scint.host = config.get("SuperCollider Internal", "host")
        scint.port = config.get("SuperCollider Internal", "port")
        return config


def configuratorFactory():
    return HyasynthConfigurator(main, ssh, scint, scext)


def updateConfig():
    configurator = configuratorFactory()
    try:
        configurator.updateConfig()
    except (NoSectionError, NoOptionError):
        print ("It seems like your config file is stale; "
               "you should generate a new one.")
