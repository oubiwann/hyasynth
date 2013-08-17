from twisted.cred import portal
from twisted.conch import manhole_ssh

from carapace.app import cred
from carapace.util import ssh as util

from hyasynth.app.shell import hyshell

from hyasynth import const


def portalFactory(namespace):
    """
    """
    realm = hyshell.HyTerminalRealm(namespace)
    return portal.Portal(realm)


def getHyShellFactory(**namespace):
    """
    The "namespace" kwargs here contains the passed objects that will be
    accessible via the shell, namely:
     * "app"
     * "services"

    These two are passed in the call to hyasynth.app.service.makeService.
    """
    sshRealm = hyshell.HyasynthTerminalRealm(namespace)
    sshPortal = portal.Portal(sshRealm)
    factory = manhole_ssh.ConchFactory(sshPortal)
    factory.privateKeys = {'ssh-rsa': util.getPrivKey()}
    factory.publicKeys = {'ssh-rsa': util.getPubKey()}
    factory.portal.registerChecker(cred.PublicKeyDatabase())
    return factory
