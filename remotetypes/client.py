import Ice
import sys
import logging

def main(config_file):
    try:
        with Ice.initialize([f"--Ice.Config={config_file}"]) as communicator:
            try:
                factory_proxy = communicator.stringToProxy("factory:tcp -p 10000")
                factory = factory_proxy
                if factory:
                    print("Conexión exitosa al servidor.")
                else:
                    print("No se pudo obtener la referencia al objeto remoto.")
            except Ice.ConnectionLostException:
                print("Error: La conexión con el servidor se perdió.")
            except Ice.LocalException as e:
                print(f"Error local al conectar al servidor: {e}")
    except Ice.FileException as e:
        print(f"Error con el archivo de configuración: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporciona el archivo de configuración como argumento.")
        sys.exit(1)

    config_file = sys.argv[1]
    main(config_file)


