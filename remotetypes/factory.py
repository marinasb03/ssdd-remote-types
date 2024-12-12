from typing import Dict, Union, Optional, Set
import json
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet
from remotetypes.customset import StringSet

class PersistenceManager:
    """Utility class to handle persistence."""
    ...

class Factory(rt.Factory):
    """Implementation of the Factory interface."""
    StringSet = Set[str]

    def __init__(self, persistence_file: str = "data.json") -> None:
        """Init."""
        self._objects: Dict[str, Union[RemoteDict, RemoteList, RemoteSet]] = {}
        self._persistence_file: str = persistence_file
        self._load_persistent_data()

    def _load_persistent_data(self) -> None:
        """Load persisted data and reconstruct objects."""
        ...

    def _save_persistent_data(self) -> None:
        """Save the current state of all objects to a JSON file."""
        ...

    def get(
        self,
        typeName: rt.TypeName,
        identifier: Optional[str] = None,
        current: Optional[Ice.Current] = None,
    ) -> rt.RTypePrx:
        """Retrieve or create an object."""
        if not identifier:
            identifier = f"{typeName.name.lower()}-{len(self._objects)}"

        if identifier in self._objects:
            return self._objects[identifier]

        if typeName == rt.TypeName.RDict:
            obj = RemoteDict(identifier)
        elif typeName == rt.TypeName.RList:
            obj = RemoteList(identifier)
        elif typeName == rt.TypeName.RSet:
            obj = RemoteSet(identifier)
        else:
            raise rt.TypeError(description="Invalid type name")

        if current and current.adapter:
            proxy = rt.RTypePrx.uncheckedCast(
                current.adapter.add(obj, current.adapter.getCommunicator().stringToIdentity(identifier))
            )
            self._objects[identifier] = proxy
        else:
            self._objects[identifier] = obj
            return obj

        self._save_persistent_data()

        return proxy
