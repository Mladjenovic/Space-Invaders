class SocketManager:
    def __init__(self, socket):
        self.socket = socket

    def send_message(self, message):
        message_to_send = message
        message_len = len(message_to_send.encode())
        self.send_all_bytes(self.socket, message_len, message_to_send)

    def recv_message(self):
        received_message = self.socket.recv(1024).decode()
        lista = received_message.split('|')
        flag = lista[0]
        message = lista[1]
        spaceship_image = lista[2]

        return flag, message, spaceship_image

    def send_all_bytes(self, socket, message_len, message_to_send):
        encoded_data = message_to_send.encode()
        bytes_sent = 0
        while bytes_sent < message_len:
            try:
                bytes_sent += socket.send(encoded_data)
            except Exception as e:
                print("Error while sending data : ", str(e))