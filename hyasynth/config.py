from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import os

from zope.interface import moduleProvides

from carapace.config import Config, Configurator, main, ssh
from carapace.sdk import interfaces

from hyasynth import meta


moduleProvides(interfaces.IConfig)


# SuperCollider external settings
scext = Config()
scext.host = "127.0.0.1"
scext.port = 57110

# SuperCollider internal settings
scint = Config()
# XXX add the following to the configuration setup below
scint.binary = "/usr/local/bin/scsynth"
# XXX add the following to the configuration setup below
scint.defaultboot = False
scint.host = "127.0.0.1"
scint.port = 57111

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
ssh.banner = """:
: Welcome to
:  _  _                       _   _
: | || |_  _ __ _ ____  _ _ _| |_| |_
: | __ | || / _` (_-< || | ' \  _| ' \\
: |_||_|\_, \__,_/__/\_, |_||_\__|_||_|
:       |__/         |__/
:
: {{WELCOME}}
: {{HELP}}
:
: Enjoy!
:
"""
ssh.welcome = """
: Hello, {{NAME}}! You have logged onto a Hysynth Server."""
ssh.banner_help = """
: Type '(ls)' or '(dir)' to see the objects in the current namespace.
: Use (help ...) to get API docs for available objects."""

class HyasynthConfigurator(Configurator):
    """
    """
    def __init__(self, main, ssh, sc, receiver):
        super(HyasynthConfigurator, self).__init__(main, ssh)
        self.scext = scext
        self.scint = scint
        self.receiver = receiver

    def buildDefaults(self):
        config = super(HyasynthConfigurator, self).buildDefaults()
        config.set("SSH", "welcome", self.ssh.welcome)
        config.set("SSH", "banner_help", self.ssh.banner_help)
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
        receiver = self.receiver
        ssh.welcome = config.get("SSH", "welcome")
        ssh.banner_help = config.get("SSH", "banner_help")
        scext.host = config.get("SuperCollider External", "host")
        scext.port = config.get("SuperCollider External", "port")
        scint.host = config.get("SuperCollider Internal", "host")
        scint.port = config.get("SuperCollider Internal", "port")
        return config


def configuratorFactory():
    return HyasynthConfigurator(main, ssh, sc, receiver)


def updateConfig():
    configurator = configuratorFactory()
    try:
        configurator.updateConfig()
    except (NoSectionError, NoOptionError):
        print ("It seems like your config file is stale; "
               "you should generate a new one.")
