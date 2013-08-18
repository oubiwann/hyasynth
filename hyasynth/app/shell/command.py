from twisted.python import log

from carapace.sdk import registry

from hydeyhole.sdk import command

from hyasynth.app.sc import buffer, bus, group, node, server, synth, ugen


class CommandAPI(command.ShellAPI, server.SCServerAPI, synth.SCSynthDefsAPI,
                 synth.SCSynthAPI, node.SCNodeAPI, group.SCGroupAPI,
                 ugen.SCUGenAPI, buffer.SCBuffersAPI, bus.SCControllBusAPI):
    """
    Gather all of the command APIs together.
    """
    def _getNonSubAPIs(self):
        return [self.command.CommandAPI] + super(
            CommandAPI, self)._getNonSubAPIs()
