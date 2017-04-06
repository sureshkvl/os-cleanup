from six import add_metaclass
from neutronclient.v2_0 import client
import abc


@add_metaclass(abc.ABCMeta)
class BaseResource(object):
    """
    Abstract Base Class for all the Resource classes.
    """

    def __init__(self, options):
        """Initialize routine. Creates a neutron client object """
        #
        self.options = options
        # neutron client
        self.nc = client.Client(**self.options.creds)
        # variable to hold the resource lists
        self.data = []

    def list(self, filter=None):
        return self.data

    @abc.abstractmethod
    def delete(self, **f):
        pass

    # @abc.abstractmethod
    # def populate(self, **f):
    #    pass

    def find(self, **f):
        """
        Returns the subset of the resources based on the filter conditions.

        params:
            dict - condition (only one key, value).  Ex: {"name": "router1"}
            returns:  List of resources

        conditions:
            1.Exact match. (Equally matching resources).

                Example:
                {"name": "router1"}
                Returns the resources which has "name" is "router1"

            2.Likely match.(regex *, only at the end)
                Example:
                {"name": "router*"}
                It returns the resources name containes "router".
                it can be router1, demorouter.
            3.Value is empty ([],""," " )
                Example:
                {"name": ""}  or {"name": "[]"} or {"name": " "}
                Returns the resources which name is None/Empty/Not set.
        """
        # limited to one key,value in the filter condition
        if not f:
            return []
        key = f.keys()
        value = f.values()

        # Checks the value for the Empty value condition
        if "[]" == value[0] or "" == value[0] or " " == value[0]:
            return list(filter(lambda x: not x.get(key[0]), self.data))

        # Checks the value for the Likely match condition
        elif "*" == value[0][-1]:
            # removes the * from string
            searchstr = value[0][:len(value[0])-1]
            return list(filter(lambda x: searchstr in str(x.get(key[0])),
                               self.data))

        # Exact match condition
        else:
            return list(filter(lambda x: x.get(key[0]) == value[0], self.data))
