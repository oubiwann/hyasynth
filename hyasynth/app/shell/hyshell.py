import os
from pprint import pprint
import sys

from zope.interface import implements

from twisted.conch.manhole import ManholeInterpreter

from carapace.app.shell import base
from carapace.sdk import exceptions, interfaces, registry


config = registry.getConfig()


BANNER_HELP = ("Type 'ls()' or 'dir()' to see the objects in the "
               "current namespace.\n: Use help(...) to get API docs "
               "for available objects.")


class CommandAPI(object):

    def __init__(self):
        self.namespace = None
        self.terminal = None
        self.appData = None
        self.appOrig = None

    def setNamespace(self, namespace):
        self.namespace = namespace

    def setTerminal(self, terminal):
        self.terminal = terminal

    def setAppData(self):
        if not self.namespace:
            return
        if not self.appData:
            self.appData = {
                "servicecollection": self.appOrig._adapterCache.get(
                    "twisted.application.service.IServiceCollection"),
                "multiservice": self.appOrig._adapterCache.get(
                    "twisted.application.service.IService"),
                "process": self.appOrig._adapterCache.get(
                    "twisted.application.service.IProcess"),
                }

    def getAppData(self):
        return pprint(self.appData)

    def ls(self):
        """
        List the objects in the current namespace, in alphabetical order.
        """
        width = max([len(x) for x in self.namespace.keys()])
        for key, value in sorted(self.namespace.items()):
            if key == "_":
                continue
            info = ""
            if (isinstance(value, dict) or
                isinstance(value, list) or key == "services"):
                info = "data"
            elif type(value).__name__ == "module":
                info = value.__name__
            elif type(value).__name__ == "function":
                info = "%s.%s" % (value.__module__, value.__name__)
            elif type(value).__name__ == "instance":
                info = "%s.%s" % (value.__module__, value.__class__.__name__)
            else:
                info = "%s.%s.%s" % (
                    value.im_class.__module__, value.im_class.__name__, key)
            print "\t%s - %s" % (key.ljust(width), info)

    def banner(self):
        """
        Display the login banner and associated help or info.
        """
        print base.renderBanner(help=BANNER_HELP)

    def clear(self):
        self.terminal.reset()

    def quit(self):
        self.terminal.loseConnection()


class HySessionTransport(base.TerminalSessionTransport):

    def getHelpHint(self):
        return BANNER_HELP


class HyTerminalSession(base.ExecutingTerminalSession):
    """
    """
    transportFactory = HySessionTransport

    def _processShellCommand(self, cmd, namespace):
        try:
            eval(cmd, namespace)
        except NameError:
            command = cmd.split("(")[0]
            msg = "Command '%s' not found in namespace!" % command
            raise exceptions.IllegalAPICommand(msg)


class HyInterpreter(ManholeInterpreter):
    """
    """
    implements(interfaces.ITerminalWriter)

    # XXX namespace code needs to be better organized:
    #   * should the CommandAPI be in this module?
    def updateNamespace(self, namespace={}):
        if not self.handler.commandAPI.appOrig:
            self.handler.commandAPI.appOrig = self.handler.namespace.get("app")
        namespace.update({
            "os": os,
            "sys": sys,
            "pprint": pprint,
            "app": self.handler.commandAPI.getAppData,
            "banner": self.handler.commandAPI.banner,
            "info": self.handler.commandAPI.banner,
            "ls": self.handler.commandAPI.ls,
            "clear": self.handler.commandAPI.clear,
            "quit": self.handler.commandAPI.quit,
            "exit": self.handler.commandAPI.quit,
            })
        if "config" not in namespace.keys():
            namespace["config"] = config
        # XXX maybe put this stuff in AdminCommandAPI(CommandAPI)?
        #
        # XXX however, in order to use this appropriately, we'd need to know
        # the avatarId when the interpreter is created, and be able to check if
        # that avatarId has the admin role...
        #
        # if admin role:
        #tcpServer = vars(services).get("services")[0]
        #tcpServer = vars(namespace.get("services").get("services")[0]
        #conchFactory = vars(tcpServer)["args"][1]
        #portal = conchFactory.portal
        #realm = portal.realm
        #users = realm.userComponents.keys()
        #from twisted.conch import interfaces
        #userReg = realm.userComponents.get(users[0])
        #avatar = userReg.getComponent(interfaces.IConchUser)
        #session = userReg.getComponent(interfaces.ISession)
        #transport = session.users.get(avatar).get("transport")
        #server = session.users.get(avatar).get("chainedProtocol")
        #server.write("hey there!")
        self.handler.namespace.update(namespace)


class HyManhole(base.MOTDColoredManhole):
    """
    """
    def setInterpreter(self):
        self.interpreter = HyInterpreter(self, locals=self.namespace)
        registry.registerComponent(
            self.interpreter, interfaces.ITerminalWriter)

    def updateNamespace(self, namespace={}):
        self.interpreter.updateNamespace(namespace)
        self.commandAPI.setNamespace(self.namespace)
        self.commandAPI.setTerminal(self.terminal)
        self.commandAPI.setAppData()


class HyTerminalRealm(base.ExecutingTerminalRealm):
    """
    """
    sessionFactory = HyTerminalSession
    transportFactory = HySessionTransport
    manholeFactory = HyManhole

    def __init__(self, namespace, apiClass=None):
        base.ExecutingTerminalRealm.__init__(self, namespace)
        if not apiClass:
            apiClass = CommandAPI

        def getManhole(serverProtocol):
            return self.manholeFactory(apiClass(), namespace)

        self.chainedProtocolFactory.protocolFactory = getManhole