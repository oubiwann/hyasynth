from twisted.python import log

from carapace.sdk import registry

from hydeyhole.sdk import command

from hyasynth.app.sc import client, process


config = registry.getConfig()
commands = command.CommandRegistry()


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


class SCUGenAPI(command.BaseAPI):
    """
    A WIP ...
    """
    @commands.add
    def ugen_cmd(self):
        """
        """
        return client.send("/u_cmd")


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


class CommandAPI(command.ShellAPI, SCServerAPI, SCSynthDefsAPI, SCNodeAPI,
                 SCSynthAPI, SCGroupAPI, SCUGenAPI, SCBuffersAPI,
                 SCControllBusAPI):
    """
    Gather all of the command APIs together.
    """
    def _getNonSubAPIs(self):
        return [self.command.CommandAPI] + super(
            CommandAPI, self)._getNonSubAPIs()
