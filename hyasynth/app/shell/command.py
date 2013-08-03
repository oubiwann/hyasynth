from hyasynth.app.sc import client


# XXX add a decorator that can be used by methods in this class to say
# whether a given method is to be used in the shell as a command; will probably
# update a dict/list on the class that holds all command methods.
class BaseAPI(object):
    """
    """


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
            else:
                info = "%s.%s.%s" % (
                    value.im_class.__module__, value.im_class.__name__, key)
            print "\t%s - %s" % (key.ljust(width), info)

    def banner(self):
        """
        Display the login banner and associated help or info.
        """
        print base.renderBanner(help=BANNER_HELP)

    def clear(self):
        self.terminal.reset()

    def quit(self):
        self.terminal.loseConnection()


class OSCAPI(BaseAPI):
    """
    """
    def send(self, *args, **kwargs):
        return client.send(*args, **kwargs)

    def status(self, *args, **kwargs):
        return client.status(*args, **kwargs)

    def server_status(self, *args, **kwargs):
        return client.server_status(*args, **kwargs)


class CommandAPI(ShellAPI, OSCAPI):
    """
    """
