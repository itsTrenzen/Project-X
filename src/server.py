from googletrans import Translator
import socket
from resemble import Resemble

Resemble.api_key('zVGJevvgoXrs2NGTG8GKFAtt')

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
        #Server protocol
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

#API functions
def createProject(name: str, desc: str, isPublic: bool, isArchived: bool, isCollaborative: bool):
    response = Resemble.v2.projects.create(name, desc, isPublic, isCollaborative, isArchived)
    project = response['item']
    return project

def getProject(uuid: str):
    response = Resemble.v2.projects.get(uuid)
    project = response['item']
    return project

def getAllProjects(page: int, pageSize: int):
    respone = Resemble.v2.projects.all(page, pageSize)
    projects = respone['items']
    return projects

def updateProject(uuid: str, name: str, desc: str, isPublic: bool, isArchived: bool, isCollaborative: bool):
    response = Resemble.v2.projects.update(uuid, name, desc, isPublic, isCollaborative, isArchived)

def deleteProject(uuid: str):
    response = Resemble.v2.projects.delete(uuid)

if __name__ == '__main__':
    server_program()