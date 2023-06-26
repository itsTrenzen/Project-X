from googletrans import Translator
import socket

def server_program():
    translator = Translator()
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(3)
    print("Server started. Waiting for connections...")

    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("From connected user: " + str(data))

        splitdata = data.split(";")
        if splitdata[0] == '?TRANS':
            translated_text = translator.translate(splitdata[1], dest=splitdata[2]).text
            conn.send(translated_text.encode())
        
        elif splitdata[0] == '?TEST':
            conn.send("Das kam an".encode())
        
        else:
            translated_text = translator.translate(data).text
            conn.send(translated_text.encode())

    conn.close()

if __name__ == '__main__':
    server_program()