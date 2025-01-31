import asyncio
import websockets

# Diccionario para almacenar las conexiones activas
connected_devices = {}

# Credenciales válidas para el XVR
VALID_CREDENTIALS = {
    "xvr_user": "passgpc",  # Usuario válido
    "xvr_password": "passgpc1978"  # Contraseña válida
}

async def handle_connection(websocket, path):
    try:
        # Recibir las credenciales del dispositivo
        credentials = await websocket.recv()
        print(f"Credenciales recibidas: {credentials}")

        # Parsear las credenciales (formato: "user:password")
        user, password = credentials.split(":")
        
        # Validar las credenciales
        if user == VALID_CREDENTIALS["xvr_user"] and password == VALID_CREDENTIALS["xvr_password"]:
            await websocket.send("AUTH_SUCCESS")
            print("Autenticación exitosa.")
        else:
            await websocket.send("AUTH_FAILED")
            print("Autenticación fallida. Credenciales incorrectas.")
            return  # Terminar la conexión si las credenciales son inválidas

        # Recibir el ID del dispositivo después de la autenticación
        device_id = await websocket.recv()
        print(f"Dispositivo registrado: {device_id}")
        
        # Almacenar la conexión en el diccionario
        connected_devices[device_id] = websocket
        print(f"Conexiones activas: {list(connected_devices.keys())}")
        
        # Manejar mensajes del dispositivo
        async for message in websocket:
            if message.startswith("CONNECT_TO:"):
                target_device_id = message.split(":")[1]
                if target_device_id in connected_devices:
                    # Enviar la dirección del dispositivo objetivo
                    target_websocket = connected_devices[target_device_id]
                    await websocket.send(f"PEER_ADDRESS:{target_websocket.remote_address}")
                    print(f"Conexión P2P establecida entre {device_id} y {target_device_id}")
                else:
                    await websocket.send("ERROR: Dispositivo no encontrado")
    except websockets.exceptions.ConnectionClosed:
        print(f"Dispositivo desconectado.")
    finally:
        # Eliminar la conexión del diccionario cuando el dispositivo se desconecta
        if device_id in connected_devices:
            del connected_devices[device_id]

# Iniciar el servidor WebSocket
start_server = websockets.serve(handle_connection, "0.0.0.0", 8765)

print("Servidor intermediario iniciado en ws://0.0.0.0:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
