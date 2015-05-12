from rackattack.ssh import connection
from strato.racktest.hostundertest import plugins

import strato.racktest.hostundertest.builtinplugins.rpm
import strato.racktest.hostundertest.builtinplugins.seed
import strato.racktest.hostundertest.builtinplugins.logbeamplugin


class Host:
    def __init__(self, rackattackNode, name):
        self.node = rackattackNode
        self.name = name
        self.ssh = connection.Connection(** rackattackNode.rootSSHCredentials())
        self.__plugins = {}

    def __eq__(self, other):
        # This method is needed in order to allow:  if host1 in [host-list]...
        if self is other:
            return True
        if isinstance(other, Host) and self.name == other.name:
            raise Exception("A new Host object was created for the same host. " \
                "You can no longer rely on custom attributes assigned to these objects.")
        return False

    def __getattr__(self, name):
        if name not in self.__plugins:
            self.__plugins[name] = plugins.plugins[name](self)
        return self.__plugins[name]
