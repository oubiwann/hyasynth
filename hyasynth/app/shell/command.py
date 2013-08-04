from carapace.app import registry
from carapace.app.shell import base
from carapace.sdk import registry

from hyasynth.app.sc import client


config = registry.getConfig()


class CommandRegistry(object):
    """
    """
    registry = []

    def add(self, func):
        """
        """
        self.registry.append(func.func_name)

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper


commands = CommandRegistry()


class BaseAPI(object):
    """
    """
    _commands = commands

    def getCommands(self):
        """
        """
        return self._commands.registry


class ShellAPI(BaseAPI):
    """
    """
    def __init__(self):
        self.namespace = None
        self.terminal = None
        self.appData = None
        self.appOrig = None

    def setNamespace(self, namespace):
        self.namespace = namespace

    def setTerminal(self, terminal):
        self.terminal = terminal

    def setAppData(self):
        if not self.namespace:
            return
        if not self.appData:
            self.appData = {
                "servicecollection": self.appOrig._adapterCache.get(
                    "twisted.application.service.IServiceCollection"),
                "multiservice": self.appOrig._adapterCache.get(
                    "twisted.application.service.IService"),
                "process": self.appOrig._adapterCache.get(
                    "twisted.application.service.IProcess"),
                }

    def getAppData(self):
        return pprint(self.appData)

    @commands.add
    def app(self):
        return self.getAppData()

    @commands.add
    def ls(self):
        """
        List the objects in the current namespace, in alphabetical order.
        """
        width = max([len(x) for x in self.namespace.keys()])
        for key, value in sorted(self.namespace.items()):
            if key == "_":
                continue
            info = ""
            if (isinstance(value, dict) or
                isinstance(value, list) or key == "services"):
                info = "data"
            elif type(value).__name__ == "module":
                info = value.__name__
            elif type(value).__name__ == "function":
                info = "%s.%s" % (value.__module__, value.__name__)
            elif type(value).__name__ == "instance":
                info = "%s.%s" % (value.__module__, value.__class__.__name__)
            elif hasattr(value, "im_class"):
                info = "%s.%s.%s" % (
                    value.im_class.__module__, value.im_class.__name__, key)
            elif hasattr(value, "__class__") and hasattr(value, "__module__"):
                info = "%s.%s.%s" % (
                    value.__module__, value.__class__.__name__, key)
            else:
                info = "<Unknown>"
            print "\t%s - %s" % (key.replace("_", "-").ljust(width), info)

    @commands.add
    def banner(self):
        """
        Display the login banner and associated help or info.
        """
        banner = base.renderBanner(help=config.ssh.banner_help)
        print banner.replace("{{WELCOME}}", config.ssh.welcome)

    @commands.add
    def welcome(self):
        """
        """
        print config.ssh.banner.replace("{{WELCOME}}", config.ssh.welcome)

    @commands.add
    def clear(self):
        self.terminal.reset()

    @commands.add
    def quit(self):
        self.terminal.loseConnection()


class SuperColliderAPI(BaseAPI):
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
        return client.send("/status")

    @commands.add
    def kill_server(self):
        return client.send("/quit")

    @commands.add
    def connect_external_server(self):
        return client.connect(mode="external")

    @commands.add
    def connect_internal_server(self):
        return client.connect(mode="internal")


class CommandAPI(ShellAPI, SuperColliderAPI):
    """
    Gather all of the command APIs together.
    """
