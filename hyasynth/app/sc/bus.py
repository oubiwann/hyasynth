from hydeyhole.sdk import command

from hyasynth.app.sc import client, commands


class SCControllBusAPI(command.BaseAPI):
    """
    A WIP ...
    """
    @commands.add
    def bus_set(self):
        """
        """
        return client.send("/c_set")

    @commands.add
    def bus_set_range(self):
        """
        """
        return client.send("/c_setn")

    @commands.add
    def bus_fill(self):
        """
        """
        return client.send("/c_fill")

    @commands.add
    def bus_get(self):
        """
        """
        return client.send("/c_get")

    @commands.add
    def bus_get_range(self):
        """
        """
        return client.send("/c_getn")