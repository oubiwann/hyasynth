from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import os

from zope.interface import moduleProvides

from carapace.config import Config, Configurator, main, ssh
from carapace.sdk import interfaces

from hyasynth import meta


moduleProvides(interfaces.IConfig)


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
ssh.welcome = "Hello, {{NAME}}! You have logged onto a Hysynth Server."
ssh.banner = """:
: Welcome to
:  _  _                       _   _
: | || |_  _ __ _ ____  _ _ _| |_| |_
: | __ | || / _` (_-< || | ' \  _| ' \\
: |_||_|\_, \__,_/__/\_, |_||_\__|_||_|
:       |__/         |__/
: {{WELCOME}}
: {{HELP}}
:
: Enjoy!
:
"""


class HyasynthConfigurator(Configurator):
    """
    """
    def __init__(self, main, db, ssh, telnet):
        super(PeloidMUDConfigurator, self).__init__(main, ssh)
        self.db = db
        self.telnet = telnet

    def buildDefaults(self):
        config = super(PeloidMUDConfigurator, self).buildDefaults()
        config.set("SSH", "welcome", self.ssh.welcome)
        return config

    def updateConfig(self):
        config = super(PeloidMUDConfigurator, self).updateConfig()
        if not config:
            return
        ssh = self.ssh
        ssh.welcome = config.get("SSH", "welcome")
        return config


def configuratorFactory():
    return HyasynthConfigurator(main, db, ssh, telnet)


def updateConfig():
    configurator = configuratorFactory()
    try:
        configurator.updateConfig()
    except (NoSectionError, NoOptionError):
        print ("It seems like your config file is stale; "
               "you should generate a new one.")
