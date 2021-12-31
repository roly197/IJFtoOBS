import socket
import asyncio
import time
import obsws 

'''---------------------------------Setup variables-------------------------'''
udpPort = 5000                                                     #UDP listening port for IJF SB to connect to
udpIp = ""                                                         #UDP IP for IJF SB to connect to

wsPort = '4444'                                                    #Websocket port to connect to OBS Server
wsHost = '127.0.0.1'                                               #Websocket IP to connect to OBS Server
wsPass = 'judo'                                                    #Password to connect to OBS Server
'''--------------------------------------------------------------------------'''

defaultCountry = 'NED'                                             #Send default 3 digit country code when empty
flagsDirectory = 'C:\\Users\\IEUser\\Documents\\IIFtoOBS\\flags\\' #Local Directory where all country flags are unzipped

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((udpIp, udpPort))

'''setup the Websocket to the OBS server running on this machine. port=4444, password=judo'''
loop = asyncio.get_event_loop()
ws = obsws.obsws(host=wsHost, port=wsPort, password=wsPass, loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.

'''All functions/logic to interpred the fields in the UDP stream'''
def matchTypeCase(i):
        switcher={
                '1':'Elimination',
                'Q':'Quarter Final',
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

def matchStatus(i):
        switcher={
                '1':False,                       # Set the 'match started' to TRUE when the scoreboard is visible (and not the user config)
                '6':True 
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

def selectFlagImage(i):                                             #Make the countru code capitals and set to default value when empty
        i=i.replace(' ','').lower()                                 #remove all whitespaces and transform to lowercase
        if i == '': i = defaultCountry.lower()                      #default to Dutch flag
        return (flagsDirectory + i +'_m.jpg')                       #(flagsDirectory + i() + '_m.jpg')

def pinTimerVisible(i):                                             #Pin Timer should ve visible when tomer <> 00 (..and counting)
        if int(i) == 0: return (False)
        else: return (True)

'''Routine to call the websocket API. Set text (string), visibility (Boolean), picture (File path as string)'''
async def make_request(messagesList):                               #Generic function to send the Websocket Object Visibility data to OBS
        await ws.connect()                                          #Connect websocket
        for i in messagesList:                                      #Iterate through thje message list to be sent
            print (i[0], i[1])
            result = await ws.call(i[0], i[1])
            print(result)
        #result = await ws.call(messagesList)
        #print(result)
        await ws.disconnect()                                       # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events

'''Main loop. Run forever'''
async def make_request_loop():
    try:
        await ws.connect() 
    except:
        print("Connection to OBS server error. Is the OBS server websocket running? ")
        time.sleep(5)
        exit(0)

    '''Empty dictionary for identifying changed attributes. All key-values need to be declared first.'''
    OLDeventData = {'SB_EventName':'', 'SB_Gender':'', 'SB_Category':'', 'SB_MatchType':'', 'SB_Time':'', 'SB_GoldenScore':'', 'SB_Winner':'', 'SB_MatchStarted':'',
        'SB_CountryW':'','SB_FlagW':'', 'SB_WrlW':'', 'SB_FamilyNameW':'', 'SB_IpponW':'', 'SB_WazaAriW':'', 'SB_ShidoHansW':'', 'SB_PinTimeW':'', 'SB_PinTimerW':'',
        'SB_CountryB':'', 'SB_FlagB':'', 'SB_WrlB':'', 'SB_FamilyNameB':'', 'SB_IpponB':'', 'SB_WazaAriB':'', 'SB_ShidoHansB':'', 'SB_PinTimeB':'', 'SB_PinTimerB':''}

    while True:
        swList = []
        recieved = sock.recvfrom(1024)
        udpUpdate = recieved[0].decode('UTF-8')

        '''Deserialize UDP data from the IJF scoreboard software UDP message.''' 
        eventTextData = {'SB_EventName':udpUpdate[4:24], 'SB_Gender':genderCase(udpUpdate[24]), 'SB_Category':(udpUpdate[25:29]+'kg'), 'SB_MatchType':matchTypeCase(udpUpdate[30]), 'SB_Time':(udpUpdate[35]+':'+udpUpdate[36:38]), 'SB_Winner':winnerCase(udpUpdate[163]), 
        'SB_CountryW':cleanupCountry(udpUpdate[38:41]),'SB_WrlW':udpUpdate[60:63], 'SB_FamilyNameW':udpUpdate[63:93], 'SB_WazaAriW':udpUpdate[95], 'SB_PinTimeW':udpUpdate[97:99], 
        'SB_CountryB':cleanupCountry(udpUpdate[100:103]), 'SB_WrlB':udpUpdate[122:125], 'SB_FamilyNameB':udpUpdate[125:155], 'SB_WazaAriB':udpUpdate[157], 'SB_PinTimeB':udpUpdate[159:161]}

        eventVisibleData = { 'SB_GoldenScore':booleanCase(udpUpdate[162]), 'SB_IpponW':booleanCase(udpUpdate[93]), 'SB_IpponB':booleanCase(udpUpdate[155]), 'SB_PinTimerW':pinTimerVisible(udpUpdate[97:99]), 'SB_PinTimerB':pinTimerVisible(udpUpdate[159:161]), 'SB_MatchStarted':matchStatus(udpUpdate[210])}
        eventFaultData = {'SB_ShidoHansW':udpUpdate[96], 'SB_ShidoHansB':udpUpdate[158]}
        eventFlagData = {'SB_FlagW':selectFlagImage(udpUpdate[38:41]),  'SB_FlagB':selectFlagImage(udpUpdate[100:103])}

        for key in eventFlagData.keys():                             #Update changed text fields
            if eventFlagData[key] != OLDeventData[key]:
                data = 'SetSourceSettings',{'sourceName': key, 'sourceSettings': {'file': eventFlagData[key]}} 
                swList.append(data)
                
        for key in eventVisibleData.keys():                          #Update changed text field
            if eventVisibleData[key] != OLDeventData[key]:
                data = 'SetSceneItemProperties',{'item': key, 'visible': eventVisibleData[key]}
                swList.append(data)

        for key in eventTextData.keys():                             #Update changed text fields
            if eventTextData[key] != OLDeventData[key]:
                data = 'SetTextGDIPlusProperties',{'source': key, 'text': eventTextData[key]}
                swList.append(data)

        for key in eventFaultData.keys():                            #Update changed visibility on Shido (1,2,3)/Hansokumake(H)
            if eventFaultData[key] != OLDeventData[key]:              #Fault (Shido/Hansokumake) data has changed
                a = faultCase(eventFaultData[key])                    #Get the list of Shido/fault status
                if key == 'SB_ShidoHansW':                            #Start sending faults for A
                    data = 'SetSceneItemProperties',{'item': 'SB_ShidoW1', 'visible': a[0]}
                    swList.append(data)
                    data = 'SetSceneItemProperties',{'item': 'SB_ShidoW2', 'visible': a[1]}
                    swList.append(data)
                    data = 'SetSceneItemProperties',{'item': 'SB_HansokumakeW', 'visible': a[2]}
                    swList.append(data)
                    #print ('FaultA: ' + str(a[0]), str(a[1]), str(a[2]))
                elif 'SB_ShidoHansB':                                 #Start sending faults for B
                    data = 'SetSceneItemProperties',{'item': 'SB_ShidoB1', 'visible': a[0]}
                    swList.append(data)
                    data = 'SetSceneItemProperties',{'item': 'SB_ShidoB2', 'visible': a[1]}
                    swList.append(data)
                    data = 'SetSceneItemProperties',{'item': 'SB_HansokumakeB', 'visible': a[2]}
                    swList.append(data)
                    #print ('FaultB: ' + str(a[0]), str(a[1]), str(a[2])) 

        #loop.run_until_complete(make_request(swList))
        for i in swList:                                     #Iterate through thje message list to be sent
            print (i[0], i[1])
            result = await ws.call(i[0], i[1])
            print(result)

        OLDeventData = eventTextData.copy()                  #Overwrite old records with new values to see if something changed in the next loop
        OLDeventData.update(eventFaultData)
        OLDeventData.update(eventFlagData)
        OLDeventData.update(eventVisibleData)  

loop.run_until_complete(make_request_loop())
