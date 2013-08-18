from hydeyhole.sdk import command

from hyasynth.app.sc import client, commands, process


class SCServerAPI(command.BaseAPI):
    """
    SuperCollider Server Control API.
    """
    @commands.add
    def send(self, *args, **kwargs):
        """
        """
        return client.send(*args, **kwargs)

    @commands.add
    def status(self):
        """
        """
        return client.send("/status")

    @commands.add
    def server_status(self):
        """
        """
        return self.status()

    @commands.add
    def kill_server(self):
        """
        """
        return client.send("/quit")

    @commands.add
    def connect_external_server(self):
        """
        """
        return client.connect(mode="external")

    @commands.add
    def connect_internal_server(self):
        """
        """
        return client.connect(mode="internal")

    @commands.add
    def boot_internal_server(self):
        """
        """
        self.connect_internal_server()
        services = self.app().get("servicecollection")
        return process.boot(mode="internal", services=services)
