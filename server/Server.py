# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 08:18:56 2022

@author: lasag
"""

import socket as sk
import time
import base64
import os


def Connect_server():
    while True:
        print ("Server in ascolto in attesa della connessione del client ")
        start, address = sock.recvfrom(4096)
        if start :
            sock.sendto(("OK").encode(), address)
            print("Server connesso" )
            return (None)
        else:
            sock.sendto(("ER").encode,address)
            print("Connessione con il client fallita, riprovare")
            
def Get_server():
    files=(File_list_server())
    while True:
        chosen_file, address =sock.recvfrom(4096)
        if files[int(chosen_file.decode()) - 1] in files:
            sock.sendto(("OK").encode(), address)
            print("E' stato scelto il file", chosen_file.decode(), files[int(chosen_file.decode()) - 1],"\n")
            file = open(files[int(chosen_file.decode()) - 1], 'rb')
            print ("Invio il file selezionato \n")
            pack = file.read(1024)
            while pack:
                sock.sendto(base64.b64encode(pack), address)
                pack=file.read(1024)
                time.sleep(0.0005)
            sock.sendto(base64.b64encode("END".encode()), address)
            file.close()
            return ("File inviato correttamente \n")
        else:
            print ("Il file scelto non è presenta sul server sceglierne un altro \n")
            sock.sendto(("ER").encode(), address)
    

def Put_server():
    file_recv, address =sock.recvfrom(4096)
    file = open(file_recv.decode(), 'wb')
    pack, server =sock.recvfrom(4096)
    while(base64.b64decode(pack.decode())!= "END".encode()):
        if(base64.b64decode(pack.decode()) != "END".encode()):
            file.write(base64.b64decode(pack.decode()))
        pack, address = sock.recvfrom(4096)
    file.close()
    return("File scaricato correttamente")
    

def File_list_server():
    print ("Invio la lista dei file presenti sul server \n")
    files = os.listdir()
    for sendable_file in files:
        if(sendable_file == "Server.py"):
            continue
        sock.sendto(sendable_file.encode(), address)

    files.remove("Server.py")
    sock.sendto("END".encode(), address)
    print ("Iinvio riuscito")
    return (files)



sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
address = ('localhost', 10000)
sock.bind(address)
try:
    Connect_server()
    while True:
        
        choose_com, address = sock.recvfrom(4096)
        if int (choose_com.decode())>=1 and int(choose_com.decode())<=4:
            sock.sendto(("OK").encode(), address)
            if int(choose_com.decode()) == 1:
                print ("è stato scelto il comando '1 - visualizzare i file presenti sul server'\n" )
                files=File_list_server()
            elif int(choose_com.decode()) == 2:
                print("è stato scelto il comando '2 - Scaricare un file presente sul server'\n")
                print (Get_server())
        
            elif int(choose_com.decode()) == 3:
                print ("è stato scelto il comando '3 - Caricare un file sul server'\n")
                print(Put_server())
            
            elif int(choose_com.decode()) == 4:
                print ("è stato scelto il comando '4 - Chiusura del server'\n ")
                break
                
        else:
            sock.sendto(("ER").encode(), address)

except Exception as error:
    print (error)
finally:
    sock.close()        















