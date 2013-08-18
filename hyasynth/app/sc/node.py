from hydeyhole.sdk import command

from hyasynth.app.sc import client, commands


class SCNodeAPI(command.BaseAPI):
    """
    A WIP ...
    """
    @commands.add
    def node_delete(self):
        """
        """
        return client.send("/n_free")

    @commands.add
    def node_run(self):
        """
        """
        return client.send("/n_run")

    @commands.add
    def node_set(self):
        """
        """
        return client.send("/n_set")

    @commands.add
    def node_set_range(self):
        """
        """
        return client.send("/n_setn")

    @commands.add
    def node_fill(self):
        """
        """
        return client.send("/n_fill")

    @commands.add
    def node_map(self):
        """
        """
        return client.send("/n_map")

    @commands.add
    def node_map_range(self):
        """
        """
        return client.send("/n_mapn")

    @commands.add
    def node_before(self):
        """
        """
        return client.send("/n_before")

    @commands.add
    def node_after(self):
        """
        """
        return client.send("/n_after")

    @commands.add
    def node_query(self):
        """
        """
        return client.send("/n_query")

    @commands.add
    def node_trace(self):
        """
        """
        return client.send("/n_trace")
