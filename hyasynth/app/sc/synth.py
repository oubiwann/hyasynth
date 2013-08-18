from hydeyhole.sdk import command

from hyasynth.app.sc import client, commands


class SCSynthDefsAPI(command.BaseAPI):
    """
    A WIP ...
    """
    @commands.add
    def synthdef_recv(self):
        """
        """
        return client.send("/d_recv")

    @commands.add
    def synthdef_load(self):
        """
        """
        return client.send("/d_load")

    @commands.add
    def synthdef_load_dir(self):
        """
        """
        return client.send("/d_loadDir")

    @commands.add
    def synthdef_delete(self):
        """
        """
        return client.send("/d_free")


class SCSynthAPI(command.BaseAPI):
    """
    A WIP ...
    """
    @commands.add
    def synth_create(self):
        """
        """
        return client.send("/s_new")

    @commands.add
    def synth_get(self):
        """
        """
        return client.send("/s_get")

    @commands.add
    def synth_get_range(self):
        """
        """
        return client.send("/s_getn")

    @commands.add
    def synth_noid(self):
        """
        """
        return client.send("/s_noid")
