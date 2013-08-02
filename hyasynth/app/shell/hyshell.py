import ast
from pprint import pprint
import os
import sys

from zope.interface import implements

from twisted.internet import defer
from twisted.conch.manhole import FileWrapper, ManholeInterpreter
from twisted.python import log

from carapace.app.shell import base
from carapace.sdk import exceptions, interfaces, registry

from hy.compiler import hy_compile
from hy.importer import ast_compile
from hy.lex.machine import Machine
from hy.lex.states import Idle, LexException
from hy.macros import process

from hyasynth.app.sc import client


config = registry.getConfig()


BANNER_HELP = ("Type '(ls)' or '(dir)' to see the objects in the "
               "current namespace.\n: Use (help ...) to get API docs "
               "for available objects.")


_hymachine = Machine(Idle, 1, 0)


def raiseCallException(data):
    """
    """
    msg = "%s: '%s'" % (data.get("error"), data.get("command"))
    raise data.get("exception")(msg)


def checkCallResult(result):
    """
    """
    if isinstance(result, dict) and result.haskey("error"):
        return raiseCallException(result)
    else:
        return result


# XXX add a decorator that can be used by methods in this class to say
# whether a given method is to be used in the shell as a command; will probably
# update a dict/list on the class that holds all command methods.
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
            # XXX create a "generateNamespaceData" method on commandAPI that
            # does all of this, returning a dict that can just be .update'd
            # here.
            "app": self.handler.commandAPI.getAppData,
            "banner": self.handler.commandAPI.banner,
            "info": self.handler.commandAPI.banner,
            "ls": self.handler.commandAPI.ls,
            "clear": self.handler.commandAPI.clear,
            "quit": self.handler.commandAPI.quit,
            "exit": self.handler.commandAPI.quit,
            "send": client.send,
            "status": client.status,
            "server_status": client.server_status,
            })
        if "config" not in namespace.keys():
            namespace["config"] = config
        self.handler.namespace.update(namespace)

    def runsource(self, source, filename='<input>', symbol='single'):
        global _hymachine

        try:
            _hymachine.process(source + "\n")
        except LexException:
            _hymachine = Machine(Idle, 1, 0)
            self.showsyntaxerror(filename)
            return False

        if type(_hymachine.state) != Idle:
            _hymachine = Machine(Idle, 1, 0)
            return True

        try:
            tokens = process(_hymachine.nodes, "__console__")
        except Exception:
            _hymachine = Machine(Idle, 1, 0)
            self.showtraceback()
            return False

        _hymachine = Machine(Idle, 1, 0)
        try:
            _ast = hy_compile(tokens, "__console__", root=ast.Interactive)
            code = ast_compile(_ast, filename, symbol)
        except Exception:
            self.showtraceback()
            return False

        self.runcode(code)
        return False

    def displayhook(self, obj):
        self.locals['_'] = obj
        log.msg("debug: type = %s" % type(obj))
        if isinstance(obj, defer.Deferred):
            if hasattr(obj, "result"):
                result = obj.result
                self.write(str(obj.result))
                return checkCallResult(result)
            else:
                d = self._pendingDeferreds
                k = self.numDeferreds
                d[id(obj)] = (k, obj)
                self.numDeferreds += 1
                obj.addCallbacks(self._cbDisplayDeferred, self._ebDisplayDeferred,
                                 callbackArgs=(k, obj), errbackArgs=(k, obj))
        elif obj is not None:
            checkCallResult(result)
            self.write(repr(obj))

    def _cbDisplayDeferred(self, result, k, obj):
        self.write("%s\n" % result, True)
        del self._pendingDeferreds[id(obj)]
        return checkCallResult(result)


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