import socket
import asyncio
from asyncio.queues import QueueEmpty
import simpleobsws

#Setup variables
udpport = 5000                                   
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("", udpport))
defaultCountry = 'NED'
flagsDirectory = 'C:\\Users\\IEUser\\Documents\\IIFtoOBS\\flags\\'

#Empty dictionalry for identifying changed attributes. All key-values need to be decared first.
OLDeventData = {'SB_EventName':'', 'SB_Gender':'', 'SB_Category':'', 'SB_MatchType':'', 'SB_Time':'', 'SB_GoldenScore':'', 'SB_Winner':'',
 'SB_CountryW':'','SB_FlagW':'', 'SB_WrlW':'', 'SB_FamilyNameW':'', 'SB_IpponW':'', 'SB_WazaAriW':'', 'SB_ShidoHansW':'', 'SB_PinTimeW':'', 
 'SB_CountryB':'', 'SB_FlagB':'', 'SB_WrlB':'', 'SB_FamilyNameB':'', 'SB_IpponB':'', 'SB_WazaAriB':'', 'SB_ShidoHansB':'', 'SB_PinTimeB':''}

#Setup the Websocket to the OBS server running on this machine. port=4444, password=judo
loop = asyncio.get_event_loop()
ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password='judo', loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.

def matchTypeCase(i):
        switcher={
                '1':'Elimination',
                'R':'Repechage',
                'S':'Semi Final',
                'B':'Bronze',
                'F':'Final',
             }
        return switcher.get(i," ")              # Space is required as default; otherwise old values are not updated

def booleanCase(i):
        switcher={
                '1':True,                       # Set the 'Golden Score' Group to Visible True or False
                '0':False 
             }
        return switcher.get(i, False)           

def winnerCase(i):
        switcher={
                'B':'Blue',
                'W':'White'
             }
        return switcher.get(i," ")              # Space is required as default; otherwise old values are not updated

def genderCase(i):
        switcher={
                'm':'Men\'s',
                'f':'Woman\s'
             }
        return switcher.get(i," ")              # Space is required as default; otherwise old values are not updated

def faultCase(i):
        switcher={
               #SB :[Yellow1, Yellow2, Red]
                '0':[False, False, False],
                '1':[True, False, False],
                '2':[True, True, False],
                '3':[False, False, True],
                'H':[False, False, True]
             }
        return switcher.get(i,'false,false,false') 

def cleanupCountry(i):
        if i.replace(' ','') == '': i = defaultCountry              #default to Dutch 
        return (i.upper())

def selectFlagImage(i):
        if i == '': i = defaultCountry                              #default to Dutch flag
        #print (i.replace(' ',''))
        return (flagsDirectory + 'ned_m.jpg')                       #(flagsDirectory + i.lower() + '_m.jpg')

async def make_textRequest(OBS_GDISource, OBS_SourceData):          #Function to send the Websocket Text data to OBS
        await ws.connect()                                          # Make the connection to OBS-Websocket
        data = {'source':OBS_GDISource, 'text':OBS_SourceData}      #Set the OBS source 'Time'
        result = await ws.call('SetTextGDIPlusProperties', data)    #Make a request with the given data
        print(result)
        await ws.disconnect()                                       # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events

async def make_JPGRequest(OBS_ColorSource, OBS_SourceData):         #Function to send the Websocket Object Visibility data to OBS
        await ws.connect()                                          # Make the connection to OBS-Websocket
        data = {'item':OBS_ColorSource, 'visible':OBS_SourceData}   #Set the OBS source 'Time'
        result = await ws.call('SetSceneItemProperties', data)      #Make a request with the given data
        print(result)
        await ws.disconnect()                                       # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events

async def make_visibilityRequest(OBS_Source, OBS_SourceData):  #Function to send the Websocket Object Visibility data to OBS
        await ws.connect()                                          # Make the connection to OBS-Websocket
        data = {'item':OBS_Source, 'visible':OBS_SourceData}   #Set the OBS source 'Time'
        result = await ws.call('SetSceneItemProperties', data)      #Make a request with the given data
        print(result)
        await ws.disconnect()                                       # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events

while True:
   recieved = sock.recvfrom(1024)
   udpUpdate = recieved[0].decode('UTF-8')
   
                                                        #Deserialize UDP data from the IJF scoreboard software. 
   eventTextData = {'SB_EventName':udpUpdate[4:24], 'SB_Gender':genderCase(udpUpdate[24]), 'SB_Category':(udpUpdate[25:29]+'kg'), 'SB_MatchType':matchTypeCase(udpUpdate[30]), 'SB_Time':(udpUpdate[35]+':'+udpUpdate[36:38]), 'SB_Winner':winnerCase(udpUpdate[163]), 
   'SB_CountryW':cleanupCountry(udpUpdate[38:41]),'SB_WrlW':udpUpdate[60:63], 'SB_FamilyNameW':udpUpdate[63:93], 'SB_WazaAriW':udpUpdate[95], 'SB_PinTimeW':udpUpdate[97:99], 
   'SB_CountryB':cleanupCountry(udpUpdate[100:103]), 'SB_WrlB':udpUpdate[122:125], 'SB_FamilyNameB':udpUpdate[125:155], 'SB_WazaAriB':udpUpdate[157], 'SB_PinTimeB':udpUpdate[159:161]}
   
   eventVisibleData = { 'SB_GoldenScore':booleanCase(udpUpdate[162]), 'SB_IpponW':booleanCase(udpUpdate[93]), 'SB_IpponB':booleanCase(udpUpdate[155]), }
   eventFaultData = {'SB_ShidoHansW':udpUpdate[96], 'SB_ShidoHansB':udpUpdate[158]}
   eventFlagData = {'SB_FlagW':selectFlagImage(udpUpdate[38:41]),  'SB_FlagB':selectFlagImage(udpUpdate[100:103])}
   
   for key in eventFlagData.keys():                     #Update changed text fields
      if eventFlagData[key] != OLDeventData[key]:
         loop.run_until_complete(make_JPGRequest (key, eventFlagData[key]))
         print (key + ' : ' + eventFlagData[key])
        
   for key in eventVisibleData.keys():                     #Update changed text field
      if eventVisibleData[key] != OLDeventData[key]:
         loop.run_until_complete(make_visibilityRequest (key, eventVisibleData[key]))
         print (key + ' : ' + str(eventVisibleData[key])) 
   
   for key in eventTextData.keys():                     #Update changed text fields
      if eventTextData[key] != OLDeventData[key]:
         loop.run_until_complete(make_textRequest(key, eventTextData[key])) 
   
   for key in eventFaultData.keys():                     #Update changed visibility on Shido (1,2,3)/Hansokumake(H)
      if eventFaultData[key] != OLDeventData[key]:      #Fault (Shido/Hansokumake) data has changed
          a = faultCase(eventFaultData[key])            #Get the list of Shido/fault status
          if key == 'SB_ShidoHansW':                    #Start sending faults for A
            loop.run_until_complete(make_visibilityRequest('SB_ShidoW1', a[0]))
            loop.run_until_complete(make_visibilityRequest('SB_ShidoW2', a[1]))
            loop.run_until_complete(make_visibilityRequest('SB_HansokumakeW', a[2]))
            print ('FaultA: ' + str(a[0]), str(a[1]), str(a[2]))
          elif 'SB_ShidoHansB':                         #Start sending faults for B
            loop.run_until_complete(make_visibilityRequest('SB_ShidoB1', a[0]))
            loop.run_until_complete(make_visibilityRequest('SB_ShidoB2', a[1]))
            loop.run_until_complete(make_visibilityRequest('SB_HansokumakeB', a[2]))
            print ('FaultB: ' + str(a[0]), str(a[1]), str(a[2])) 

   OLDeventData = eventTextData.copy()                  #Overwrite old records with new values to see if something changed in the next loop
   OLDeventData.update(eventFaultData)
   OLDeventData.update(eventFlagData)
   OLDeventData.update(eventVisibleData)
     

   