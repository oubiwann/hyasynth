from twisted.python import log

from txosc import osc
from txosc import dispatch

from hyasynth import exceptions


def parseStatus(_, ugens, synths, groups, loaded, avg, peak, nominal, actual):
    data = {"unit generators": ugens,
            "synths": synths,
            "groups": groups,
            "loaded synths": loaded,
            "average cpu": avg,
            "peak cpu": peak,
            "nominal sample rate": nominal,
            "actual sample rate": actual}
    return {"status": data}


def handleStatus(message, client):
    """
    """
    result = parseStatus(*message.getValues())
    log.msg("Result in handleStatus: %s" % result)
    client.deferredResult.callback(result)


def handleDone(message, client):
    """
    """
    result = message.getValues()
    if result == ['/quit']:
        result = {"shutdown": "done"}
    log.msg("Result in handleDone: %s" % result)
    client.deferredResult.callback(result)


def handleFail(message, client):
    """
    """
    errorData = message.getValues()
    log.err("Failure: %s" % str(errorData))
    error = {"error": errorData[1],
             "command": errorData[0],
             "exception": exceptions.RemoteCallError}
    #client.deferredResult.errback(exceptions.RemoteCallError(errorData[1]))
    client.deferredResult.callback(error)


receiverAPI = dispatch.Receiver()
receiverAPI.addCallback("/status.reply", handleStatus)
receiverAPI.addCallback("/done", handleDone)
receiverAPI.addCallback("/fail", handleFail)
