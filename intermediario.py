import asyncio
import websockets

# Diccionario para almacenar las conexiones activas
connected_devices = {}

async def handle_connection(websocket, path):
    # Recibir el ID del dispositivo
    device_id = await websocket.recv()
    print(f"Dispositivo registrado: {device_id}")
    
    # Almacenar la conexión en el diccionario
    connected_devices[device_id] = websocket
    print(f"Conexiones activas: {list(connected_devices.keys())}")
    
    try:
        async for message in websocket:
            # Si el mensaje es una solicitud de conexión
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
        print(f"Dispositivo desconectado: {device_id}")
        del connected_devices[device_id]

# Iniciar el servidor WebSocket
start_server = websockets.serve(handle_connection, "0.0.0.0", 8765)

print("Servidor intermediario iniciado en ws://0.0.0.0:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
