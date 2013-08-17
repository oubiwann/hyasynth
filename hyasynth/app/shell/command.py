import inspect
from operator import itemgetter

from twisted.python import log

from carapace.app import registry
from carapace.app.shell import base
from carapace.sdk import registry

from hyasynth.app import shell
from hyasynth.app.sc import client, process

from hydeyhole.sdk import command

config = registry.getConfig()


commands = command.CommandRegistry()


class SuperColliderAPI(command.BaseAPI):
    """
    """
    @commands.add
    def send(self, *args, **kwargs):
        return client.send(*args, **kwargs)

    @commands.add
    def status(self):
        return client.send("/status")

    @commands.add
    def server_status(self):
        return self.status()

    @commands.add
    def kill_server(self):
        return client.send("/quit")

    @commands.add
    def connect_external_server(self):
        return client.connect(mode="external")

    @commands.add
    def connect_internal_server(self):
        return client.connect(mode="internal")

    @commands.add
    def boot_internal_server(self):
        self.connect_internal_server()
        services = self.app().get("servicecollection")
        return process.boot(mode="internal", services=services)


class CommandAPI(command.ShellAPI, SuperColliderAPI):
    """
    Gather all of the command APIs together.
    """
    def _getNonSubAPIs(self):
        return [self.command.CommandAPI] + super(
            CommandAPI, self)._getNonSubAPIs()
