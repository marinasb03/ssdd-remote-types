import json
from typing import Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet


class PersistenceManager:
    """Utility class to handle persistence."""

    @staticmethod
    def save(filepath: str, data: dict) -> None:
        """Save data to a JSON file."""
        with open(filepath, "w") as f:
            json.dump(data, f)

    @staticmethod
    def load(filepath: str) -> dict:
        """Load data from a JSON file."""
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}


class Factory(rt.Factory):
    """Implementation of the Factory interface."""

    def __init__(self, persistence_file: str = "data.json") -> None:
        self._objects = {}
        self._persistence_file = persistence_file
        self._load_persistent_data()

    def _load_persistent_data(self) -> None:
        """Load persisted data and reconstruct objects."""
        data = PersistenceManager.load(self._persistence_file)
        for identifier, obj_data in data.items():
            obj_type = obj_data["type"]
            content = obj_data["content"]

            if obj_type == "RDict":
                obj = RemoteDict(identifier)
                obj._storage_ = content
            elif obj_type == "RList":
                obj = RemoteList(identifier)
                obj._storage_ = content
            elif obj_type == "RSet":
                obj = RemoteSet(identifier)
                obj._storage_ = set(content)
            else:
                continue

            self._objects[identifier] = obj

    def _save_persistent_data(self) -> None:
        """Save the current state of all objects to a JSON file."""
        data = {}
        for identifier, obj in self._objects.items():
            if isinstance(obj, RemoteDict):
                data[identifier] = {"type": "RDict", "content": obj._storage_}
            elif isinstance(obj, RemoteList):
                data[identifier] = {"type": "RList", "content": obj._storage_}
            elif isinstance(obj, RemoteSet):
                data[identifier] = {"type": "RSet", "content": list(obj._storage_)}
        
        PersistenceManager.save(self._persistence_file, data)

    def get(
        self, typeName: rt.TypeName, identifier: Optional[str] = None, current: Optional[Ice.Current] = None
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
            proxy = current.adapter.add(obj, current.adapter.getCommunicator().stringToIdentity(identifier))
            self._objects[identifier] = proxy
        else:
            self._objects[identifier] = obj
            return obj

        self._save_persistent_data()

        return proxy

