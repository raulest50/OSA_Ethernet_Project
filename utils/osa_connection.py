import socket
import time

class AQ6370D:
    def __init__(self, address, port=10001):
        self.address = address
        self.port = port
        self.socket = None
    
    def open_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)  # Timeout más corto para prueba de conexión
            self.socket.connect((self.address, self.port))
            return True, "Conexión establecida con el dispositivo en " + self.address
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"
    
    def close_socket(self):
        if self.socket:
            self.socket.close()
            return "Conexión cerrada."
    
    def send_command(self, command):
        try:
            if self.socket:
                self.socket.send((command + "\r\n").encode())
                time.sleep(0.2)
                return True, "Comando enviado correctamente"
            else:
                return False, "Socket no inicializado."
        except Exception as e:
            return False, f"Error al enviar comando: {str(e)}"
    
    def test_connection(self):
        """
        Prueba la conexión con el OSA y devuelve el resultado
        """
        success, message = self.open_socket()
        if success:
            # Intentar enviar un comando simple para verificar la comunicación
            self.send_command("*IDN?")
            try:
                # Intentar recibir respuesta
                response = self.socket.recv(1024).decode('utf-8', errors='ignore')
                if response:
                    message += f"\nDispositivo identificado: {response.strip()}"
            except:
                pass  # Si no hay respuesta, continuamos con el mensaje de conexión exitosa
            self.close_socket()
        return success, message