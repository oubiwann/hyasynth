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

from hydeyhole.app.shell import hyshell

from hyasynth.app.shell import command


config = registry.getConfig()


class HyasynthTerminalRealm(hyshell.HyTerminalRealm):
    """
    """
    def __init__(self, namespace, apiClass=None):
        base.ExecutingTerminalRealm.__init__(self, namespace)
        if not apiClass:
            apiClass = command.CommandAPI

        def getManhole(serverProtocol):
            return self.manholeFactory(apiClass(), namespace)

        self.chainedProtocolFactory.protocolFactory = getManhole