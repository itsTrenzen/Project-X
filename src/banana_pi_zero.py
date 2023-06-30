import socket
import pyaudio

# Server details
host = socket.gethostname()  # Server IP address
port = 5000  # Server port

# Audio settings
chunk_size = 1024
sample_format = pyaudio.paInt16
channels = 1
sample_rate = 44100

def send_audio():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server")

    audio = pyaudio.PyAudio()
    stream = audio.open(format=sample_format,
                        channels=channels,
                        rate=sample_rate,
                        frames_per_buffer=chunk_size,
                        input=True)

    print("Streaming audio...")

    try:
        while True:
            data = stream.read(chunk_size)
            client_socket.sendall(data)
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        client_socket.close()
        print("Connection closed")

if __name__ == '__main__':
    send_audio()
