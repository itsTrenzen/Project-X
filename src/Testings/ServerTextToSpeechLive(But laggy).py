# This is client code to receive video and audio frames over UDP

import socket
import threading, wave, pyaudio, time, queue, os

q = queue.Queue(maxsize=2000)

def audio_stream_UDP():
	
    BUFF_SIZE = 65536
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(3)
    print("Server started. Waiting for connections...")

    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    p = pyaudio.PyAudio()
    CHUNK = 10*1024
    stream = p.open(format=p.get_format_from_width(2),
					channels=2,
					rate=44100,
					output=True,
					frames_per_buffer=CHUNK)
					
	# create socket
    message = b'Hello'
    conn.sendto(message,(host,port))
    socket_address = (host,port)
	
    def getAudioData():
    	
        global q

        while True:
            frame,_= conn.recvfrom(BUFF_SIZE)
            q.put(frame)
            print('Queue size...',q.qsize())
            if q.qsize() > 100:
                q = queue.Queue(maxsize=2000)
	    
    t1 = threading.Thread(target=getAudioData, args=())
    t1.start()
    time.sleep(5)
    print('Now Playing...')
    
    while True:
    	
        frame = q.get()
        stream.write(frame)

    conn.close()
    print('Audio closed')
    os._exit(1)



t1 = threading.Thread(target=audio_stream_UDP, args=())
t1.start()

