import os
import re

from twisted.application import internet
from twisted.internet import defer, reactor
from twisted.internet.protocol import Factory, ProcessProtocol
from twisted.python import log

from carapace.sdk import registry


config = registry.getConfig()


class SCProcessProtocol(ProcessProtocol):
    """
    A process protocol for the SuperCollider executable.
    """
    def __init__(self, type="", mode=""):
        self.type = type
        self.mode = mode
        ProcessProtocol.__init__(self)

    def boot_internal(self):
        processName = config.scint.binary.split("/")[-1]
        args = [processName,
                "-t", str(config.scint.port),
                "-u", str(config.scint.port)]
        log.msg("Spawning '%s' with args '%s' ..." % (
            config.scint.binary, " ".join(args[1:])))
        reactor.spawnProcess(
            self,
            config.scint.binary,
            args=args,
            env=os.environ)

    def boot_external(self):
        raise NotImplementedError()

    def connectionMade(self):
        log.msg("Starting SuperCollider ...")
        if self.mode == "internal":
            self.boot_internal()
        log.msg("Connection to SuperCollider process made.")

    def outReceived(self, data):
        log.msg("SuperCollider: %s" % str(data).strip())

    def processExited(self, reason):
        log.msg("SuperCollider process exited; status: %d" % (
            reason.value.exitCode,))

    def processEnded(self, reason):
        log.msg("SuperCollider process ended; status: %d" % (
            reason.value.exitCode,))
        log.msg("Quitting ...")
        data = {"status": "process exited"}
        self.deferred.result = data
        self.deferred.callback(str(data))

    def errReceived(self, data):
        log.msg("errReceived! with %d bytes!" % len(data))

    def inConnectionLost(self):
        log.msg("inConnectionLost! stdin is closed! (we probably did it)")

    def outConnectionLost(self):
        log.msg("outConnectionLost! The child closed their stdout!")
        (dummy, lines, words, chars, file) = re.split(r'\s+', self.data)
        log.msg("I saw %s lines" % lines)

    def errConnectionLost(self):
        log.msg("errConnectionLost! The child closed their stderr.")


class ProcessFactory(Factory):
    """
    """
    protocol = SCProcessProtocol

    def __init__(self, type="", mode=""):
        self.type = type
        self.mode = mode

    def processResult(self, result):
        log.msg("Boot result: %s" % result)
        return result

    def buildProtocol(self, addr):
        log.msg("Building process protocol ...")
        p = self.protocol()
        p.deferred = defer.Deferred()
        p.deferred.addCallback(self.processResult)
        p.factory = self
        return p


def boot(mode="", options=None, services=None):
    """
    """
    log.msg("Starting to book scsynth in %s mode ..." % mode)
    factory = ProcessFactory(type="", mode=mode)
    if mode == "internal":
        log.msg("Set internal port and service name.")
        port = config.scint.spawnport
        name = config.scint.servicename
    try:
        log.msg("Starting TCP server for scsynth ...")
        processServer = internet.TCPServer(port, factory)
        processServer.setName(name)
        processServer.setServiceParent(services)
        log.msg("Set scsynth service parent.")
        return processServer
    except Exception, error:
        log.err(error)
        return {"error": str(error)}
