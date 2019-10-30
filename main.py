from Proc import *
import time

c = Config()
s = Spyserver()
d = Database()

def configBuilder():
    bind_host = c.readConfig(readField='bind_host')
    userKey = input('Current Host is ' + bind_host +', Update It? (Y/N)')
    if userKey.upper() == 'Y':
        newValue = input("New Host: ")
        c.updateConfig(updateField='bind_host', updateContent=newValue)

    bind_port = c.readConfig(readField='bind_port')
    userKey = input('Current Port is ' + bind_port + ', Update It? (Y/N)')
    if userKey.upper() == 'Y':
        newValue = input("New Port: ")
        c.updateConfig(updateField='bind_port', updateContent=newValue)

    c.updateConfig(updateField='list_in_directory', updateContent='0')

    owner_name = c.readConfig(readField='owner_name')
    userKey = input('Current Owner Name is ' + owner_name + ', Update It? (Y/N)')
    if userKey.upper() == 'Y':
        newValue = input("New Owner Name: ")
        c.updateConfig(updateField='owner_name', updateContent=newValue)

    owner_email = c.readConfig(readField='owner_email')
    userKey = input('Current Owner Email is ' + owner_email + ', Update It? (Y/N)')
    if userKey.upper() == 'Y':
        newValue = input("New Owner Email: ")
        c.updateConfig(updateField='owner_email', updateContent=newValue)

    antenna_type = c.readConfig(readField='antenna_type')
    userKey = input('Current Antenna Type is \r\n' + antenna_type + ', Update It? (Y/N)')
    if userKey.upper() == 'Y':
        newValue = input("New Antenna Type: \r\n")
        c.updateConfig(updateField='antenna_type', updateContent=newValue)

    general_description = c.readConfig(readField='general_description')
    userKey = input('Current Description is\r\n' + general_description + ', Update It? (Y/N)')
    if userKey.upper() == 'Y':
        newValue = input("New Description:\r\n")
        c.updateConfig(updateField='general_description', updateContent=newValue)

    maximum_clients = c.readConfig(readField='maximum_clients') #10 is max
    userKey = input('Current Max Clients is ' + maximum_clients + ', Update It? (Y/N)')
    if userKey.upper() == 'Y':
        newValue = input("New Max Clients: ")
        c.updateConfig(updateField='maximum_clients', updateContent=newValue)

    maximum_session_duration = c.readConfig(readField='maximum_session_duration') # zero means unlimited
    userKey = input('Current Session Duration is ' + maximum_session_duration + ', Update It? (Y/N)')
    if userKey.upper() == 'Y':
        newValue = input("New Session Duration: ")
        c.updateConfig(updateField='maximum_session_duration', updateContent=newValue)

    allow_control = c.readConfig(readField='allow_control') #Can user control sdr
    userKey = input('Current Allow Control is ' + allow_control + ', Update It? (Y/N)')
    if userKey.upper() == 'Y':
        newValue = input("New Allow Control: ")
        c.updateConfig(updateField='allow_control', updateContent=newValue)

    c.updateConfig(updateField='force_8bit', updateContent='1') #leave this on without user control

##
## FIGURE OUT HOW YOU CAN KEEP SOMETHING OUT OF THE CONFIG UNLESS OTHERWISE NEEDED
## IE: FREQUENCY OPTIONS WILL BE DEFAULT UNTIL PLACED INTO CONFIG, DONT PLACE IF NOT NEEDED
##

#    initial_frequency = readConfig(readField='initial_frequency') #user doesn't have to set this in hz
#    minimum_frequency = readConfig(readField='minimum_frequency') #user doesn't have to set this in hz
#    maximum_frequency = readConfig(readField='maximum_frequency') #user doesn't have to set this in hz

    enable_bias_tee = c.readConfig(readField='enable_bias_tee') #only for airspy
    userKey = input('Current bias Tee for airspy is ' + enable_bias_tee + ', Update It? (Y/N)')
    if userKey.upper() == 'Y':
        newValue = input("New Bias Tee: ")
        c.updateConfig(updateField='enable_bias_tee', updateContent=newValue)


if c.convertConfig('spyserver.config') == True: #If returns true the config has already been converted with the header for configparser
    userKey = input('This configuration has already been converted, do you need to update it? (Y/N)')
    if userKey.upper() == "Y":
        print('starting config process.\r\n')
        configBuilder()
        d.updateConfig()
    else:
        print('Starting spyserver')
        s.startSpyserver()#Here you should start the service and monitor the heartbeat
        print('Sending Database Update')
        d.updateConfig()
else:
    print('This is your first run, we need to setup your config')
    configBuilder()
    d.updateConfig()
    print('Updating Database')
    print("\r\n")
    s.startSpyserver()
    print("Starting Spyserver")

while True:
    try:
        time.sleep(5)
        if s.checkProc() == True:
            print("Spyserver is runnning")
        else:
            print("Spyserver is dead")
        print("Owner: " + c.readConfig(readField='owner_name'))
    except SystemExit:
        s.killProc()
