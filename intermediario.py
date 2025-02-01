import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from PIL import Image

# Simulación de dispositivos ONVIF registrados
registered_devices = {}

# Imagen estática para simular el video
def get_static_image():
    # Crea una imagen simple con Pillow
    img = Image.new('RGB', (640, 480), color=(73, 109, 137))
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

class ONVIFHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Leer la solicitud SOAP/XML
        content_length = int(self.headers['Content-Length'])
        soap_request = self.rfile.read(content_length).decode()
        print(f"Solicitud SOAP recibida:\n{soap_request}")

        # Simular una respuesta ONVIF
        if "GetDeviceInformation" in soap_request:
            response = """<?xml version="1.0" encoding="UTF-8"?>
            <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope">
                <SOAP-ENV:Body>
                    <tds:GetDeviceInformationResponse>
                        <tds:Manufacturer>Simulated Camera</tds:Manufacturer>
                        <tds:Model>ONVIF Camera</tds:Model>
                        <tds:FirmwareVersion>1.0</tds:FirmwareVersion>
                    </tds:GetDeviceInformationResponse>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""
            self.send_response(200)
            self.send_header("Content-Type", "application/soap+xml")
            self.end_headers()
            self.wfile.write(response.encode())

    def do_GET(self):
        # Simular una respuesta de descubrimiento WS-Discovery
        if "onvif/device_service" in self.path:
            response = """<?xml version="1.0" encoding="UTF-8"?>
            <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope">
                <SOAP-ENV:Body>
                    <wsdd:ProbeMatches>
                        <wsdd:ProbeMatch>
                            <wsdd:XAddrs>http://prueba-36vg.onrender.com/onvif/device_service</wsdd:XAddrs>
                        </wsdd:ProbeMatch>
                    </wsdd:ProbeMatches>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""
            self.send_response(200)
            self.send_header("Content-Type", "application/soap+xml")
            self.end_headers()
            self.wfile.write(response.encode())

def start_onvif_server():
    server = HTTPServer(("0.0.0.0", 8080), ONVIFHandler)
    print("Servidor ONVIF iniciado en 0.0.0.0:8080")
    server.serve_forever()

def start_rtsp_server():
    # Simular un servidor RTSP que envía una imagen estática
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 554))  # Puerto estándar para RTSP
    server_socket.listen(5)
    print("Servidor RTSP iniciado en 0.0.0.0:554")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Conexión RTSP entrante desde {address}")
        threading.Thread(target=handle_rtsp_connection, args=(client_socket,)).start()

def handle_rtsp_connection(client_socket):
    try:
        # Simular una respuesta RTSP
        client_socket.send(b"RTSP/1.0 200 OK\r\nCSeq: 1\r\n\r\n")
        while True:
            # Enviar la imagen estática como un frame de video
            image_data = get_static_image()
            client_socket.send(image_data)
    except Exception as e:
        print(f"Error en la conexión RTSP: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Iniciar el servidor ONVIF
    threading.Thread(target=start_onvif_server, daemon=True).start()

    # Iniciar el servidor RTSP
    threading.Thread(target=start_rtsp_server, daemon=True).start()

    print("Intermediario ONVIF activo.")
