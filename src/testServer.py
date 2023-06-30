import socket
import speech_recognition as sr

# Server details
host = socket.gethostname() 
port = 5000  # Server port

def receive_audio():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server listening on", (host, port))

    client_socket, client_address = server_socket.accept()
    print("Connected to client", client_address)

    r = sr.Recognizer()

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            #print("Received audio:", data)
            #audio = sr.AudioData(data, sample_rate=44100, sample_width=2)
            #ext = r.recognize_google(audio, language='de-DE')
            #print(text)
            print(data)
    except KeyboardInterrupt:
        print("Interrupted")
    except sr.UnknownValueError:
        print('Could not understand audio')
    finally:
        client_socket.close()
        server_socket.close()
        print("Connection closed")

if __name__ == '__main__':
    receive_audio()
