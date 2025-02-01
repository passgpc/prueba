import socket
import threading

# Diccionario para almacenar las conexiones activas
connected_devices = {}

# Credenciales válidas para el XVR
VALID_CREDENTIALS = {
    "xvr_user": "passgpc",  # Usuario válido
    "xvr_password": "passgpc1978"  # Contraseña válida
}

def handle_device_connection(client_socket, address):
    device_id = None
    try:
        # Paso 1: Recibir las credenciales del dispositivo
        credentials = client_socket.recv(1024).decode()
        print(f"Credenciales recibidas de {address}: {credentials}")

        # Parsear las credenciales (formato: "user:password")
        try:
            user, password = credentials.split(":")
        except ValueError:
            client_socket.send("ERROR: Formato de credenciales incorrecto".encode())
            return

        # Validar las credenciales
        if user == VALID_CREDENTIALS["xvr_user"] and password == VALID_CREDENTIALS["xvr_password"]:
            client_socket.send("AUTH_SUCCESS".encode())
            print(f"Autenticación exitosa para {address}.")
        else:
            client_socket.send("AUTH_FAILED".encode())
            print(f"Autenticación fallida para {address}. Credenciales incorrectas.")
            return

        # Paso 2: Recibir el ID del dispositivo después de la autenticación
        device_id = client_socket.recv(1024).decode()
        print(f"Dispositivo registrado: {device_id} desde {address}")

        # Almacenar la conexión en el diccionario
        connected_devices[device_id] = client_socket
        print(f"Conexiones activas: {list(connected_devices.keys())}")

        # Paso 3: Manejar mensajes del dispositivo
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if message.startswith("CONNECT_TO:"):
                target_device_id = message.split(":")[1]
                if target_device_id in connected_devices:
                    # Enviar la dirección del dispositivo objetivo
                    target_socket = connected_devices[target_device_id]
                    target_address = target_socket.getpeername()
                    client_socket.send(f"PEER_ADDRESS:{target_address}".encode())
                    print(f"Conexión P2P establecida entre {device_id} y {target_device_id}")
                else:
                    client_socket.send("ERROR: Dispositivo no encontrado".encode())

    except Exception as e:
        print(f"Error con el dispositivo {address}: {e}")
    finally:
        client_socket.close()
        # Eliminar la conexión del diccionario cuando el dispositivo se desconecta
        if device_id in connected_devices:
            del connected_devices[device_id]

def start_server():
    # Crear un socket TCP/IP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 10000))  # Puerto 10000
    server.listen(5)
    print("Servidor intermediario iniciado en 0.0.0.0:10000")

    while True:
        client_socket, address = server.accept()
        print(f"Conexión entrante desde {address}")
        # Manejar cada conexión en un hilo separado
        threading.Thread(target=handle_device_connection, args=(client_socket, address)).start()

if __name__ == "__main__":
    start_server()
