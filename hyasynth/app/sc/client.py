from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.error import ConnectionRefusedError
from twisted.python import log

from txosc import osc
from txosc import async

from hyasynth import config
from hyasynth.app.sc import receiver


def handleError(failure):
    log.err("Error in client: %s" % str(failure))
    error = failure.trap(ConnectionRefusedError)
    if error == ConnectionRefusedError:
        return {"status": "connection refused"}
    return failure


def makeClient(host, port, callback, arg):
    endpoint = TCP4ClientEndpoint(reactor, host, port)
    client = async.ClientFactory(receiver.receiverAPI)
    d = endpoint.connect(client)
    d.addCallbacks(callback,
                   handleError,
                   callbackArgs=[client, arg])
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


def connect(mode=""):
    """
    This is needed when one has booted an internal server and connected to it,
    resetting the default connection variables to internal host/port. By calling
    this function, the connection variables are reset to use the external
    server.

    Similarly if one has connected to an external server, resetting the
    defaults, and one ones to switch back to an internal server.
    """
    if mode == "external":
        config.sc.host = config.scext.host
        config.sc.port = config.scext.port
    elif mode == "internal":
        config.sc.host = config.scint.host
        config.sc.port = config.scint.port