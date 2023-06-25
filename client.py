import socket
import speech_recognition as sr
#import pyttsx3
from threading import Thread
import time
 
# Initialize the recognizer
r = sr.Recognizer()
MyText = 'r'
# Function to convert text to
# speech
"""
def SpeakText(command):
     
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
"""
     
# Loop infinitely for user to
# speak
def record():
    while(1):   
        
        try:
         
            # use the microphone as source for input.
            with sr.Microphone() as source2:
             
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)
             
                #listens for the user's input
                audio2 = r.listen(source2)
             
                # Using google to recognize audio
                global MyText
                MyText = r.recognize_google(audio2, language="de-DE")
                MyText = MyText.lower()
 
                print(MyText)
                #SpeakText(MyText) die Stimme nervt
             
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
         
        except sr.UnknownValueError:
            print("unknown error occurred")



def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    #message = input(" -> ")  # take input
    global MyText
    message = MyText

    while message.lower().strip() != 'bye':
        message = 'Hallo großer'
        message = MyText
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        #message = input(" -> ")  # again take input
        message = MyText
        time.sleep(0.1)

    client_socket.close()  # close the connection

if __name__ == '__main__':
    t1 = Thread(target = client_program)
    t2 = Thread(target = record)
    t1.start()
    t2.start()