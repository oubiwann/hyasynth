from hydeyhole.sdk import command

from hyasynth.app.sc import client, commands



class SCGroupAPI(command.BaseAPI):
    """
    A WIP ...
    """
    @commands.add
    def group_create(self):
        """
        """
        return client.send("/g_new")

    @commands.add
    def group_prepend_node(self):
        """
        """
        return client.send("/g_head")

    @commands.add
    def group_append_node(self):
        """
        """
        return client.send("/g_tail")

    @commands.add
    def group_free_nodes(self):
        """
        """
        return client.send("/g_freeAll")

    @commands.add
    def group_free_synths(self):
        """
        """
        return client.send("/g_deepFree")

    @commands.add
    def group_dump_tree(self):
        """
        """
        return client.send("/g_dumpTree")

    @commands.add
    def group_query_tree(self):
        """
        """
        return client.send("/g_queryTree")