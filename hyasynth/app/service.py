import sys

from twisted.application import service, internet
from twisted.python import usage

from carapace.sdk import const as sshConst, interfaces, registry, scripts

from hyasynth import config, const, meta
from hyasynth.app.shell.service import getHyShellFactory


config = registry.getConfig()


class SubCommandOptions(usage.Options):
    """
    A base class for subcommand options.

    Can also be used directly for subcommands that don't have options.
    """


class Options(usage.Options):
    """
    """
    optParameters = [
        [const.sc.portLongOption, const.sc.portShortOption, const.sc.port,
         ("The SuperCollider port number.")]
        ]
    subCommands = [
        [sshConst.KEYGEN, None, SubCommandOptions,
         "Generate ssh keys for the server"],
        [sshConst.SHELL, None, SubCommandOptions, "Login to the server"],
        [sshConst.STOP, None, SubCommandOptions, "Stop the server"],
        ]

    def parseOptions(self, options):
        config = registry.getConfig()
        usage.Options.parseOptions(self, options)
        # check options
        if self.subCommand == sshConst.KEYGEN:
            scripts.KeyGen()
            sys.exit(0)
        elif self.subCommand == sshConst.SHELL:
            scripts.ConnectToShell()
            sys.exit(0)
        elif self.subCommand == sshConst.STOP:
            scripts.StopDaemon()
            sys.exit(0)


def makeService(options):
    # options
    #someVar = options.get(const.someConst)
    # primary setup
    application = service.Application(meta.description)
    services = service.IServiceCollection(application)
    # setup ssh for the game server
    sshFactory = getHyShellFactory(app=application, services=services)
    sshServer = internet.TCPServer(config.ssh.port, sshFactory)
    sshServer.setName(config.ssh.servicename)
    sshServer.setServiceParent(services)
    # setup server for SC communications
    # XXX
    return services
