from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import os

from zope.interface import moduleProvides

from carapace.config import Config, Configurator, main, ssh
from carapace.sdk import interfaces

from hyasynth import meta


moduleProvides(interfaces.IConfig)


# SuperCollider settings
sc = Config()
sc.host = "127.0.0.1"
sc.port = 57110


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
        self.sc = sc
        self.receiver = receiver

    def buildDefaults(self):
        config = super(HyasynthConfigurator, self).buildDefaults()
        config.set("SSH", "welcome", self.ssh.welcome)
        config.set("SSH", "banner_help", self.ssh.banner_help)
        config.add_section("SuperCollider")
        config.set("SuperCollider", "host", self.sc.host)
        config.set("SuperCollider", "port", self.sc.port)
        return config

    def updateConfig(self):
        config = super(HyasynthConfigurator, self).updateConfig()
        if not config:
            return
        ssh = self.ssh
        sc = self.sc
        receiver = self.receiver
        ssh.welcome = config.get("SSH", "welcome")
        ssh.banner_help = config.get("SSH", "banner_help")
        sc.host = config.get("SuperCollider", "host")
        sc.port = config.get("SuperCollider", "port")
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
