#!/usr/bin/env python3

import sys
import Ice
from typing import List
Ice.loadSlice("remotetypes.ice")
import RemoteTypes as rt  # type: ignore

class RSetClient:
    """Cliente para probar operaciones sobre RSet."""
    def __init__(self, factory_service):
        """Inicializa el cliente RSet."""
        self.factory = factory_service

    def interact(self, rset_proxy):
        """Interacción con el RSet."""
        while True:
            print("\nOperaciones disponibles para el RSet:")
            print("1. Agregar un elemento")
            print("2. Eliminar un elemento")
            print("3. Longitud del RSet")
            print("4. Comprobar existencia de un elemento")
            print("5. Obtener hash del RSet")
            print("6. Ver identificador")
            print("7. Iterar sobre los elementos del RList")
            print("8. Salir")

            try:
                choice = int(input("Selecciona una opción (1-8): "))
            except ValueError as e:
                print(f"Entrada no válida: {e}")
                continue

            if choice == 1:
                element = input("Elemento a agregar: ")
                rset_proxy.add(element)
                print(f"Elemento '{element}' agregado al RSet.")
            elif choice == 2:
                element = input("Elemento a eliminar: ")
                try:
                    rset_proxy.remove(element)
                    print(f"Elemento '{element}' eliminado.")
                except rt.KeyError as e:
                    print(f"No se encuentra el elemento '{element}': {e}")
            elif choice == 3:
                length = rset_proxy.length()
                print(f"El RSet tiene {length} elementos.")
            elif choice == 4:
                element = input("Elemento a comprobar: ")
                if rset_proxy.contains(element):
                    print(f"El elemento '{element}' está en el RSet.")
                else:
                    print(f"El elemento '{element}' no está en el RSet.")
            elif choice == 5:
                rset_hash = rset_proxy.hash()
                print(f"Hash del RSet: {rset_hash}")
            elif choice == 6:
                identifier = rset_proxy.identifier()
                print(f"Identificador del RSet: {identifier}")
            elif choice == 7:
                iterator = rlist_proxy.iter()
                print("Iterando sobre los elementos del RList:")
                while True:
                    try:
                        item = iterator.next()
                        print(item)
                    except rt.StopIteration as e:
                        print("Terminado de iterar, con excepcion: ", e)
                        break
            elif choice == 8:
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")

class RListClient:
    """Cliente para probar operaciones sobre RList."""
    def __init__(self, factory_service):
        """Inicializa el cliente RList."""
        self.factory = factory_service

    def interact(self, rlist_proxy):
        """Interacción con el RList."""
        while True:
            print("\nOperaciones disponibles para el RList:")
            print("1. Agregar un elemento")
            print("2. Eliminar un elemento")
            print("3. Longitud del RList")
            print("4. Comprobar existencia de un elemento")
            print("5. Obtener hash del RList")
            print("6. Ver identificador")
            print("7. Iterar sobre los elementos del RList")
            print("8. Salir")
            
            

            try:
                choice = int(input("Selecciona una opción (1-8): "))
            except ValueError as e:
                print(f"Entrada no válida: {e}")
                continue

            if choice == 1:
                element = input("Elemento a agregar: ")
                rlist_proxy.append(element)
                print(f"Elemento '{element}' agregado al RList.")
            elif choice == 2:
                element = input("Elemento a eliminar: ")
                try:
                    rlist_proxy.remove(element)
                    print(f"Elemento '{element}' eliminado.")
                except rt.KeyError as e:
                    print(f"No se encuentra el elemento '{element}': {e}")
            elif choice == 3:
                length = rlist_proxy.length()
                print(f"El RList tiene {length} elementos.")
            elif choice == 4:
                element = input("Elemento a comprobar: ")
                if rlist_proxy.contains(element):
                    print(f"El elemento '{element}' está en el RList.")
                else:
                    print(f"El elemento '{element}' no está en el RList.")
            elif choice == 5:
                rlist_hash = rlist_proxy.hash()
                print(f"Hash del RList: {rlist_hash}")
            elif choice == 6:
                identifier = rlist_proxy.identifier()
                print(f"Identificador del RList: {identifier}")
            elif choice == 7:
                iterator = rlist_proxy.iter()
                print("Iterando sobre los elementos del RList:")
                while True:
                    try:
                        item = iterator.next()
                        print(item)
                    except rt.StopIteration as e:
                        print("Terminado de iterar, con excepcion: ", e)
                        break
            elif choice == 8:
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")

class RDictClient:
    """Cliente para probar operaciones sobre RDict."""
    def __init__(self, factory_service):
        """Inicializa el cliente RDict."""
        self.factory = factory_service

    def interact(self, rdict_proxy):
        """Interacción con el RDict."""
        while True:
            print("\nOperaciones disponibles para el RDict:")
            print("1. Agregar un elemento")
            print("2. Obtener un elemento")
            print("3. Eliminar un elemento")
            print("4. Longitud del RDict")
            print("5. Comprobar existencia de una clave")
            print("6. Obtener hash del RDict")
            print("7. Ver identificador")
            print("8. Iterar sobre los elementos del RList")
            print("9. Salir")

            try:
                choice = int(input("Selecciona una opción (1-9): "))
            except ValueError as e:
                print(f"Entrada no válida: {e}")
                continue

            if choice == 1:
                key = input("Clave a agregar: ")
                value = input("Valor a agregar: ")
                rdict_proxy.setItem(key, value)
                print(f"Elemento '{key}: {value}' agregado al RDict.")
            elif choice == 2:
                key = input("Clave a obtener: ")
                try:
                    value = rdict_proxy.getItem(key)
                    print(f"Elemento con clave '{key}': {value}")
                except rt.KeyError as e:
                    print(f"No se encuentra la clave '{key}': {e}")
            elif choice == 3:
                key = input("Clave a eliminar: ")
                try:
                    rdict_proxy.pop(key)
                    print(f"Elemento con clave '{key}' eliminado.")
                except rt.KeyError as e:
                    print(f"No se encuentra la clave '{key}': {e}")
            elif choice == 4:
                length = rdict_proxy.length()
                print(f"El RDict tiene {length} elementos.")
            elif choice == 5:
                key = input("Clave a comprobar: ")
                if rdict_proxy.contains(key):
                    print(f"La clave '{key}' está en el RDict.")
                else:
                    print(f"La clave '{key}' no está en el RDict.")
            elif choice == 6:
                rdict_hash = rdict_proxy.hash()
                print(f"Hash del RDict: {rdict_hash}")
            elif choice == 7:
                identifier = rdict_proxy.identifier()
                print(f"Identificador del RDict: {identifier}")
            elif choice == 8:
                iterator = rdict_proxy.iter()
                print("Iterando sobre las claves del RDict:")
                while True:
                    try:
                        key = iterator.next()
                        print(key)
                    except rt.StopIteration as e:
                        print("iteracion termianda, excepcion:", e)
                        break
            elif choice == 9:
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")

class Cliente(Ice.Application):
    """Cliente para interactuar con el servidor."""
    def run(self, argv: List[str]) -> int:
        """Configura y ejecuta el cliente."""
        proxy_string = "factory:default -p 10000"
        print(f"Usando el proxy: {proxy_string}")

        try:
            proxy = self.communicator().stringToProxy(proxy_string)
        except Exception as e:
            print(f"Error al crear el proxy: {e}")
            return -1

        factory = rt.FactoryPrx.checkedCast(proxy)
        if not factory:
            print("No se pudo conectar con el servidor.")
            return -1

        while True:
            print("\nSelecciona un tipo de operación:")
            print("1. Salir")
            print("2. RList")
            print("3. RDict")
            print("4. RSet")

            try:
                option = int(input("Opción (1-4): "))
            except ValueError:
                print("Opción no válida.")
                continue

            if option == 1:
                print("Saliendo del cliente.")
                break

            elif option == 2:
                transfer = factory.get(rt.TypeName.RList)
                rlist_proxy = rt.RListPrx.checkedCast(transfer)
                if not rlist_proxy:
                    print("No se pudo crear el RList.")
                    continue
                RListClient(factory).interact(rlist_proxy)

            elif option == 3:
                transfer = factory.get(rt.TypeName.RDict)
                rdict_proxy = rt.RDictPrx.checkedCast(transfer)
                if not rdict_proxy:
                    print("No se pudo crear el RDict.")
                    continue
                RDictClient(factory).interact(rdict_proxy)

            elif option == 4:
                transfer = factory.get(rt.TypeName.RSet)
                rset_proxy = rt.RSetPrx.checkedCast(transfer)
                if not rset_proxy:
                    print("No se pudo crear el RSet.")
                    continue
                RSetClient(factory).interact(rset_proxy)
                
            else:
                print("Opción no válida.")

        return 0


if __name__ == '__main__':
    client = Cliente()
    sys.exit(client.main(sys.argv))
