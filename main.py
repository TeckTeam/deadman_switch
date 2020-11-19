import pyAesCrypt
from threading import Thread
import glob
from tqdm import tqdm
import time
import os
import socket

class deadman:
    def __init__(self):
        self.buffer = 64*1024
        
        try:
            self.passwd= open("./files/password.key").read()
        except:
            print("Can't find Key file")
            exit()
        self.path = "./files/"
        self.found = False
        self.sleeptime = 3
        self.switch()
    def encrypt(self, file):
        if file != "" and self.passwd != "" and ".encrypt" not in file:
            try:
                pyAesCrypt.encryptFile(file, file+".encrypt", self.passwd, self.buffer)
                os.system('rm "'+file+'"')
            except :
                print("Can't encrypt ",file)
        else:
            print("Can't encrypt ",file)
    def decrypt(self, file):
        if file != "" and self.passwd != "" and ".encrypt" in file:
            try:
                pyAesCrypt.decryptFile(file, file[:-8], self.passwd, self.buffer)
                os.system('rm "'+file+'"')
            except:
                print("Can't decrypt ",file)
        else:
            print("Can't decrypt ",file)

    def listener(self):
        while self.kill_event == False:
            try:
                conn, addr = self.serv.accept()
                with conn:
                    print("Man found at",addr)
                    conn.close()
                    self.found = True
                    break
            except:
                pass
        


    def switch(self):
        self.sleeptime = self.sleeptime * self.sleeptime
        try:
            print("Start switch")
            self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serv.bind(("0.0.0.0",10000))
            self.serv.settimeout(1)
            self.serv.listen()
            while True:
                self.kill_event = False
                self.found = False #Flag false

                self.ac_thread = Thread(target=self.listener)#Create Thread
                self.ac_thread.start()#Start Thread 
                self.ac_thread.join(timeout=10)#Wait for x sec
                
                

                if self.found == True:
                    print("Wellcome back!\nStart decrypting")
                    self.kill_event = True#Kill Thread
                    files = glob.glob(self.path+"**/*.encrypt",recursive=True) #Find all encrypted files
                    if files != []:
                        for file in tqdm(files):
                            self.decrypt(file)


                else:
                    print("Deadman Found!\nStart encrypting")
                    self.kill_event = True#Kill Thread
                    files = glob.glob(self.path+"**/*.*",recursive=True) #Find all encrypted files
                    if files != []:
                        for file in tqdm(files):
                            if ".encrypt" not in file:
                                self.encrypt(file)

        except KeyboardInterrupt:
            self.kill_event = True
            self.serv.close()
            del(self.passwd)
            for i in range(10):
                self.passwd = "Heksdkjsfhjsdafkasghdfsdbhcfsjgdhfnxshd"
                del(self.passwd)
            print("Shutdown switch")
        except:
            time.sleep(self.sleeptime)
            self.switch()
            
d = deadman()


