import socket
import speech_recognition as sr
import time

r = sr.Recognizer()
running = True
MyText = False

def handle_response(data):
    print('Received from server:', data)  # show in terminal


def client_program():
    host = socket.gethostname()  # as both code is running on the same machine
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    global running
    while running:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                global MyText
                MyText = r.recognize_google(audio2, language="de-DE")
                MyText = MyText.lower()

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error occurred:", e)

        if MyText:
            print(MyText)
            message = '?TRANS;' + MyText + ';en'
            if MyText == 'beenden':
                client_socket.close()
                running = False
            else:
                MyText = False #prevents the resending of old messages
                client_socket.send(message.encode())  # send message
                data = client_socket.recv(1024).decode()  # receive response
                handle_response(data)

                time.sleep(0.1)

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()