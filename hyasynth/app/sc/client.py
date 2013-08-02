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
    endpoint = TCP4ClientEndpoint(reactor, host, port)
    client = async.ClientFactory(receiver.receiverAPI)
    d = endpoint.connect(client)
    d.addErrback(handleError)
    d.addCallback(callback, client, arg)
    d.addErrback(handleError)
    return d


def send(message):
    """
    """
    def handleProtocol(protocol, client, message):
        d = client.send(osc.Message(message))
        d.addErrback(handleError)
        client.deferredResult = d
        return d

    return makeClient(config.sc.host, config.sc.port, handleProtocol, message)