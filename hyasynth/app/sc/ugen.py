from hydeyhole.sdk import command

from hyasynth.app.sc import client, commands


class SCUGenAPI(command.BaseAPI):
    """
    A WIP ...
    """
    @commands.add
    def ugen_cmd(self):
        """
        """
        return client.send("/u_cmd")
