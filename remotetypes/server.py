"""Clase servidor."""
import logging
import Ice
from remotetypes.factory import Factory

class Server(Ice.Application):
    """Inicio de clase."""

    def __init__(self):
        """Init."""
        super().__init__()
        self.logger = logging.getLogger(__file__)

    def run(self, args: list[str]) -> int:
        """Run."""
        factory_servant = Factory()
        adapter = (
            self.communicator().createObjectAdapterWithEndpoints("remotetypes", "default -p 10000")
        )
        identity = self.communicator().stringToIdentity("factory")
        proxy = adapter.add(factory_servant, identity)
        self.logger.info('Proxy: "%s"', proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()
        return 0

