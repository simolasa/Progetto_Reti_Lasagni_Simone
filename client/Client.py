# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 08:17:58 2022

@author: lasag
"""

import base64
import socket as sk
import time
import os

#La funzione Connect_client viene chiamata solo all'avvio del programma e fa si che il client e
#il server si connettano, in caso ci sia un errore lo stampa a video e riprova.

def Connect_client(address):
    print ("Client pronto, mi connetto al server \n")
    sock.sendto(("OK").encode(), address)
    control, address = sock.recvfrom(4096)
    if control.decode() == "OK":
        return ("Client connesso al server")
    else:
        print("Connessione fallita riprovare")
        
#la funzione List_file_client chiede la lista di file presenti sul server e li stampa a video 
#all'utente utilizzatore del client.
        
def List_files_client():
    print("\nLista dei file disponibili:")
    list_file = []
    num = 1
    files, server = sock.recvfrom(4096)
    while(files.decode() != "END"):
        print(num, files.decode())
        list_file.append(files.decode())
        files, server = sock.recvfrom(4096)
        num+=1
    return (list_file)      

#Get_client riceve un file scelto tra quelli presenti sul server e lo copia nel client.
 
def Get_client(address):
    files=List_files_client()
    while True:
        choose_file = int(input("Inserisci il numero del file che vuoi ricevere: "))
        if choose_file>=1 and choose_file<=len(files):
            file = open(files[choose_file - 1], 'wb')
            sock.sendto(str(choose_file).encode(), address)
            control, address = sock.recvfrom(4096)
            if control.decode() == "OK":
                print ("\nScaricando il file "+ files[choose_file-1])
                pack, server =sock.recvfrom(4096)
                while(base64.b64decode(pack.decode())!= "END".encode()):
                    if(base64.b64decode(pack.decode()) != "END".encode()):
                        file.write(base64.b64decode(pack.decode()))
                        pack, server = sock.recvfrom(4096)    
                file.close()
                return("\nIl file "+ files[choose_file-1]+ " è stato scaricato correttamente")
        else:
            print("\nIl numero scelto non corrisponde a nessun file presente sul server,selezionarne un'altro")
                    
#Put_client prende un file scelto presente sul client e lo spedisce al server.

def Put_client():
    files= os.listdir()
    files.remove("Client.py")
    while True:
        print("\nLista dei file disponibli:")
        num=1
        for i in files:
            print (num,i)
            num+=1
        choose_file=int(input("Inserisci il numero del file da inviare: "))
        if choose_file>=1 and choose_file<=len(files):
            sock.sendto(files[choose_file - 1].encode(), address)
            print("E' stato scelto il file", choose_file, files[choose_file - 1],"\n")
            file = open(files[choose_file - 1], 'rb')
            print ("Invio il file selezionato \n")
            pack = file.read(1024)
            while pack:
                sock.sendto(base64.b64encode(pack), address)
                pack=file.read(1024)
                time.sleep(0.0005)
            sock.sendto(base64.b64encode("END".encode()), address)
            file.close()
            return ("Il file " + files[choose_file-1] + " è stato inviato correttamente \n")
        else:
            print("Il numero scelto non corrisponde a nessun file presente nel client, selezionarne un'altro")

#In questa sezione di codice vi è un loop che prende il comando scelto dall'utente e ne avvia la 
#rispettiva funzione inviando al server la scelta in modo che anche lui posssa attivare le sue funzioni
#corrispondenti.
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
address = ('localhost', 10000)
try: 
    print(Connect_client(address))
    list_mod=("\nComandi disponibili:\n "
             "1 - Visualizzare i file presenti sul server\n "
             "2 - Scaricare un file presente sul server\n "
             "3 - Caricare un file sul server\n "
             "4 - Chiusura del server")
    while True:
        print(list_mod)
        choose_com = int(input("Inserisci il numero del comando che vuoi eseguire: "))
        sock.sendto(str(choose_com).encode(), address)
        control, address = sock.recvfrom(4096)
        if control.decode() == "OK":
            if choose_com == 1:
                List_files_client()
            elif choose_com == 2:
                print(Get_client(address))
            elif choose_com == 3:
                print(Put_client())
            elif choose_com == 4:
                break
        else:
            print ("Scegliere un comando valido \n")
except Exception as info:
    print(info)
finally:
    print("Chiudo il client")
    sock.close()