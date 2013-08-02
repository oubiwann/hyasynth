from twisted.internet import defer, reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.python import log

from txosc import osc
from txosc import dispatch
from txosc import async

from hyasynth import config
from hyasynth.app.sc import receiver

def handleError(reason):
    log.err(reason)


def makeClient(host, port, callback, arg):
    log.msg("Preparing to create client ...")
    endpoint = TCP4ClientEndpoint(reactor, host, port)
    client = async.ClientFactory(receiver.receiverAPI)
    d = endpoint.connect(client)
    d.addErrback(handleError)
    d.addCallback(callback, client, arg)
    d.addErrback(handleError)
    return d


def handleProtocol(protocol, client, message):
    log.msg("Got protocol: %s" % str(protocol))
    log.msg("Sending message '%s' ..." % message)
    d = client.send(osc.Message(message))
    log.msg("Send deferred: %s" % d)
    d.addErrback(handleError)
    client.deferredResult = d
    return d


def send(message):
    d = makeClient(
        config.sc.host,
        config.sc.port,
        handleProtocol,
        message)
    return d