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

from hyasynth.app.shell import command


config = registry.getConfig()


_hymachine = Machine(Idle, 1, 0)


def renderBanner(help="", welcome=""):
    return config.ssh.banner.replace(
        "{{WELCOME}}", welcome).replace(
        "{{HELP}}", help)


def raiseCallException(data):
    """
    """
    msg = "%s: '%s'" % (data.get("error"), data.get("command"))
    raise data.get("exception")(msg)


def checkCallResult(result):
    """
    """
    if isinstance(result, dict) and result.has_key("error"):
        return raiseCallException(result)
    else:
        return result


class HySessionTransport(base.TerminalSessionTransport):
    """
    """
    def writeMOTD(self):
        termProto = self.chainedProtocol.terminalProtocol
        banner = renderBanner(
            help=self.getHelpHint(),
            welcome=self.getWelcomeMessage())
        termProto.terminal.write("\r\n" + banner + "\r\n")
        termProto.terminal.write(termProto.ps[termProto.pn])

    def getHelpHint(self):
        return config.ssh.banner_help

    def getWelcomeMessage(self):
        return config.ssh.banner_welcome


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

    def updateNamespace(self, namespace={}):
        if not self.handler.commandAPI.appOrig:
            self.handler.commandAPI.appOrig = self.handler.namespace.get("app")
        # set some useful modules in the namespace
        namespace.update({
            "os": os,
            "sys": sys,
            "api": self.handler.commandAPI,
            "pprint": pprint})
        # set the defined commands in the namespace
        for name in self.handler.commandAPI.getCommands():
            namespace[name] = getattr(self.handler.commandAPI, name)
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
            checkCallResult(obj)
            self.write(repr(obj))

    def _cbDisplayDeferred(self, result, k, obj):
        self.write("%s\n" % result, True)
        del self._pendingDeferreds[id(obj)]
        return checkCallResult(result)


class HyManhole(base.MOTDColoredManhole):
    """
    """
    ps = (":> ", ".. ")

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
            apiClass = command.CommandAPI

        def getManhole(serverProtocol):
            return self.manholeFactory(apiClass(), namespace)

        self.chainedProtocolFactory.protocolFactory = getManhole