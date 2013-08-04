import os

from twisted.internet import defer, reactor
from twisted.internet.protocol import ProcessProtocol
from twisted.python import log

from carapace.sdk import registry


config = registry.getConfig()


class SCProcessProtocol(ProcessProtocol):
    """
    A process protocol for the SuperCollider executable.
    """
    def connectionMade(self):
        log.msg("Connection to SuperCollider process made.")
        #self.deferred.callback({"status": "process running"})

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


def boot_internal(protocol):
    processName = config.scint.binary.split("/")[-1]
    args = [processName,
            "-t", str(config.scint.port),
            "-u", str(config.scint.port)]
    log.msg("Spawning '%s' with args '%s' ..." % (
        config.scint.binary, " ".join(args[1:])))
    reactor.spawnProcess(
        protocol,
        config.scint.binary,
        args=args,
        env=os.environ)


def boot_external(protocol):
    raise NotImplementedError()


def boot(mode=""):
    """
    """
    def process_result(result):
        log.msg("Boot result: %s" % result)
        return result

    protocol = SCProcessProtocol()
    protocol.deferred = defer.Deferred()
    if mode == "internal":
        boot_internal(protocol)
    if mode == "external":
        boot_external(protocol)
    protocol.deferred.addCallback(process_result)
    return protocol.deferred