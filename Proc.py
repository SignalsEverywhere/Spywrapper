from google.cloud import firestore, storage
import os
import psutil
import subprocess
import configparser

class Spyserver:

    def __init__(self):
        pass

    def checkProc(self):  # Returns True if spyserver is running/None if it is not
        for proc in psutil.process_iter(attrs=['name']):
            if proc.name().lower() == 'spyserver.exe':
                return True

    def killProc(self):
        for proc in psutil.process_iter(attrs=['name']):
            if proc.name() == 'spyserver.exe':
                proc.kill()

    def startSpyserver(self): #starts the spyserver application assuming it's in the same directory as this script
        subprocess.Popen("spyserver.exe")


class Config:

    def __init__(self):
        pass


    def convertConfig(self, confFile='spyserver.config'): #Opens an existing spyserver.config file and adds the header that makes it functional with configparser
        with open(confFile, 'r+') as f:
            content = f.read()
            if content.__contains__("[SPYSERVER_CONFIG]"):
                return True
            else:
                f.seek(0, 0)
                f.write("[SPYSERVER_CONFIG]" + '\n' + content)
                return False

    def updateConfig(self, confFile='spyserver.config',updateField=None, updateContent=None): #Takes arguments to update a single line in your config file
        config = configparser.ConfigParser()
        config.read(confFile)
        config['SPYSERVER_CONFIG'][updateField] = updateContent
        with open(confFile, 'w') as confFile:
            config.write(confFile)

    def readConfig(self, confFile='spyserver.config', readField=None): #Reads any one line of the config file
        try:
            config = configparser.ConfigParser()
            config.read(confFile)
            return config['SPYSERVER_CONFIG'][readField]
        except:
            return 'No Entry Exists'


class Database:

    def __init__(self):
        pass

    def dbAdd(self, serverName, serverHost, serverPort, serverOwner, serverEmail, serverAntenna, serverLocation, serverDescription, serverClients, ):
        credPath = 'key.json'
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credPath

        db = firestore.Client()
        doc_ref = db.collection(u'spyservers').document(serverName)
        doc_ref.set({
            u'serverName': serverName,
            u'serverHost': serverHost,
            u'serverPort': serverPort,
            u'serverOwner': serverOwner,
            u'serverEmail': serverEmail,
            u'serverAntenna': serverAntenna,
            u'serverLocation': serverLocation,
            u'serverDescription': serverDescription,
            u'serverClients': serverClients
        })

    def dbRead(self, server, field):
        credPath = 'key.json'
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credPath

        db = firestore.Client()
        doc_ref = db.collection(u'spyservers').document(server)
        container = doc_ref.get()
        return container.get(field)

    def updateConfig(self):
        serverHost = Config.readConfig(self, readField='bind_host')
        serverPort = Config.readConfig(self, readField='bind_port')
        serverOwner = Config.readConfig(self, readField='owner_name')
        serverEmail = Config.readConfig(self, readField='owner_email')
        serverAntenna = Config.readConfig(self, readField='antenna_type')
        serverLocation = Config.readConfig(self, readField='antenna_location')
        serverDecription = Config.readConfig(self, readField='general_description')
        serverClients = Config.readConfig(self, readField='maximum_clients')


        self.dbAdd(serverName='test', serverHost=serverHost, serverPort=serverPort, serverOwner=serverOwner, serverEmail=serverEmail, serverAntenna=serverAntenna, serverLocation=serverLocation, serverDescription=serverDecription, serverClients=serverClients)

