import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# Simulación de dispositivos ONVIF registrados
registered_devices = {}

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
                        <tds:SerialNumber>123456789</tds:SerialNumber>
                        <tds:HardwareId>HW123</tds:HardwareId>
                    </tds:GetDeviceInformationResponse>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""
            self.send_response(200)
            self.send_header("Content-Type", "application/soap+xml")
            self.end_headers()
            self.wfile.write(response.encode())

        elif "GetCapabilities" in soap_request:
            response = """<?xml version="1.0" encoding="UTF-8"?>
            <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope">
                <SOAP-ENV:Body>
                    <tds:GetCapabilitiesResponse>
                        <tds:Capabilities>
                            <tds:Device>
                                <tt:XAddr>http://prueba-36vg.onrender.com/onvif/device_service</tt:XAddr>
                            </tds:Device>
                            <tds:Media>
                                <tt:XAddr>http://prueba-36vg.onrender.com/onvif/media_service</tt:XAddr>
                            </tds:Media>
                        </tds:Capabilities>
                    </tds:GetCapabilitiesResponse>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""
            self.send_response(200)
            self.send_header("Content-Type", "application/soap+xml")
            self.end_headers()
            self.wfile.write(response.encode())

        else:
            self.send_response(400)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Solicitud no soportada")

    def do_GET(self):
        # Simular una respuesta de descubrimiento WS-Discovery
        if "onvif/device_service" in self.path:
            response = """<?xml version="1.0" encoding="UTF-8"?>
            <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope">
                <SOAP-ENV:Body>
                    <wsdd:ProbeMatches>
                        <wsdd:ProbeMatch>
                            <wsdd:XAddrs>http://prueba-36vg.onrender.com/onvif/device_service</wsdd:XAddrs>
                            <wsdd:Types>dn:NetworkVideoTransmitter</wsdd:Types>
                        </wsdd:ProbeMatch>
                    </wsdd:ProbeMatches>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""
            self.send_response(200)
            self.send_header("Content-Type", "application/soap+xml")
            self.end_headers()
            self.wfile.write(response.encode())

def start_onvif_server():
    # Obtener el puerto principal de la variable de entorno PORT
    ONVIF_PORT = int(os.getenv("PORT", 8080))  # Usa el puerto asignado por Render o 8080 como predeterminado

    server = HTTPServer(("0.0.0.0", ONVIF_PORT), ONVIFHandler)
    print(f"Servidor ONVIF iniciado en 0.0.0.0:{ONVIF_PORT}")
    server.serve_forever()

if __name__ == "__main__":
    # Iniciar el servidor ONVIF
    threading.Thread(target=start_onvif_server, daemon=True).start()
    print("Intermediario ONVIF activo.")
