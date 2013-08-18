from hydeyhole.sdk import command

from hyasynth.app.sc import client, commands


class SCBuffersAPI(command.BaseAPI):
    """
    A WIP ...
    """
    @commands.add
    def buffer_allocate(self):
        """
        """
        return client.send("/b_alloc")

    @commands.add
    def buffer_allocate_read(self):
        """
        """
        return client.send("/b_allocRead")

    @commands.add
    def buffer_allocate_read_channels(self):
        """
        """
        return client.send("/b_allocReadChannel")

    @commands.add
    def buffer_read(self):
        """
        """
        return client.send("/b_read")

    @commands.add
    def buffer_read_channel(self):
        """
        """
        return client.send("/b_readChannel")

    @commands.add
    def buffer_write(self):
        """
        """
        return client.send("/b_write")

    @commands.add
    def buffer_free(self):
        """
        """
        return client.send("/b_free")

    @commands.add
    def buffer_zero(self):
        """
        """
        return client.send("/b_zero")

    @commands.add
    def buffer_set(self):
        """
        """
        return client.send("/b_set")

    @commands.add
    def buffer_set_range(self):
        """
        """
        return client.send("/b_setn")

    @commands.add
    def buffer_fill_range(self):
        """
        """
        return client.send("/b_fill")

    @commands.add
    def buffer_gen(self):
        """
        """
        return client.send("/b_gen")

    @commands.add
    def buffer_close(self):
        """
        """
        return client.send("/b_close")

    @commands.add
    def buffer_query(self):
        """
        """
        return client.send("/b_query")

    @commands.add
    def buffer_get(self):
        """
        """
        return client.send("/b_get")

    @commands.add
    def buffer_get_range(self):
        """
        """
        return client.send("/b_getn")