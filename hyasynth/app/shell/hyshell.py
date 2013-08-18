from twisted.python import log

from carapace.app.shell import base
from carapace.sdk import registry


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