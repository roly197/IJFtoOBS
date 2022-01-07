from asyncio.windows_events import IocpProactor
import socket
import asyncio
import time
import obsws 

'''---------------------------------Setup variables-------------------------'''
udpPort = 5000                                                     #UDP listening port for IJF SB to connect to
udpIp = ""                                                         #UDP IP for IJF SB to connect to. Keep empty to liten to te bradcast address,

wsPort = '4444'                                                    #Websocket port to connect to OBS Server
wsHost = '127.0.0.1'                                               #Websocket IP to connect to OBS Server
wsPass = 'judo'                                                    #Password to connect to OBS Server

defaultCountry = 'NED'                                             #Send default 3 digit country code when empty
flagsDirectory = '/Users/roly/Projects/IJFtoOBS/flags/'            #Local Directory where all country flags are unzipped
'''--------------------------------------------------------------------------'''

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((udpIp, udpPort))

'''setup the Websocket to the OBS server running on this machine. port=4444, password=judo'''
loop = asyncio.get_event_loop()
ws = obsws.obsws(host=wsHost, port=wsPort, password=wsPass, loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.

ts = time.time()

class Deser_ijf():
        def __init__(self, default_country=None, flags_directory=None, mat = '1', ip = None):
                import logging
                self.logger = logging.getLogger("UDPtoOBSserializer")
                self.ip = ip 
                self.mat = mat
                self.default_country = default_country
                self.flags_directory = flags_directory
                self.oldEventData = {'SB_EventName':'', 
                                        'SB_Gender':'', 
                                        'SB_Category':'', 
                                        'SB_MatchType':'', 
                                        'SB_Time':'', 
                                        'SB_GoldenScore':'', 
                                        'SB_Winner':'', 
                                        'SB_MatchStarted':'',
                                        'SB_CountryW':'',
                                        'SB_FlagW':'', 
                                        'SB_WrlW':'', 
                                        'SB_FamilyNameW':'', 
                                        'SB_IpponW':'', 
                                        'SB_WazaAriW':'', 
                                        'SB_ShidoHansW':'', 
                                        'SB_PinTimeW':'', 
                                        'SB_PinTimerW':'', 
                                        'SB_TeamScoreW':'',
                                        'SB_CountryB':'', 
                                        'SB_FlagB':'', 
                                        'SB_WrlB':'', 
                                        'SB_FamilyNameB':'', 
                                        'SB_IpponB':'', 
                                        'SB_WazaAriB':'', 
                                        'SB_ShidoHansB':'', 
                                        'SB_PinTimeB':'', 
                                        'SB_PinTimerB':'', 
                                        'SB_TeamScoreB':''}

        '''All functions/logic to interpred the fields in the UDP stream'''
        def _matchTypeCase(self, i):
                switcher={
                        '1':'Elimination',
                        'Q':'Quarter Final',
                        'R':'Repechage',
                        'S':'Semi Final',
                        'B':'Bronze',
                        'F':'Final',
                }
                return switcher.get(i," ")              # Space is required as default; otherwise old values are not updated

        def _booleanCase(self, i):
                switcher={
                        '1':True,                       # Set the 'Golden Score' Group to Visible True or False
                        '0':False 
                }
                return switcher.get(i, False)  

        def _matchStatus(self, i):
                switcher={
                        '1':False,                       # Set the 'match started' to TRUE when the scoreboard is visible (and not the user config)
                        '6':True 
                }
                return switcher.get(i, False)         

        def _winnerCase(self, i):
                switcher={
                        'B':'Blue',
                        'W':'White'
                }
                return switcher.get(i," ")              # Space is required as default; otherwise old values are not updated

        def _genderCase(self, i):
                switcher={
                        'm':'Men\'s',
                        'f':'Woman\s'
                }
                return switcher.get(i," ")              # Space is required as default; otherwise old values are not updated

        def _faultCase(self, i):
                switcher={
                #SB :[Yellow1, Yellow2, Red]
                        '0':[False, False, False],
                        '1':[True, False, False],
                        '2':[True, True, False],
                        '3':[False, False, True],
                        'H':[False, False, True]
                }
                return switcher.get(i,'false,false,false') 

        def _cleanupCountry(self, i):
                if i.replace(' ','') == '': i = defaultCountry              #default to Dutch 
                return (i.upper())

        def _selectFlagImage(self, i):                                             #Make the countru code capitals and set to default value when empty
                i=i.replace(' ','').lower()                                 #remove all whitespaces and transform to lowercase
                if i == '': i = defaultCountry.lower()                      #default to Dutch flag
                return (flagsDirectory + i +'_m.jpg')                       #(flagsDirectory + i() + '_m.jpg')

        def _pinTimerVisible(self, i):                                             #Pin Timer should ve visible when tomer <> 00 (..and counting)
                if int(i) == 0: return (False)
                else: return (True)

        def deserializeIjf(self, udpUpdate):
                '''Deserialize UDP data from the IJF scoreboard software UDP message.'''
                self.eventTextData = {'SB_EventName':udpUpdate[4:24], 
                        'SB_Gender':self._genderCase(udpUpdate[24]), 
                        'SB_Category':(udpUpdate[25:29]+'kg'), 
                        'SB_MatchType':self._matchTypeCase(udpUpdate[30]),
                        'SB_Time':(udpUpdate[35]+':'+udpUpdate[36:38]), 
                        'SB_Winner':self._winnerCase(udpUpdate[163]), 
                        'SB_CountryW':self._cleanupCountry(udpUpdate[38:41]),
                        'SB_WrlW':udpUpdate[60:63], 
                        'SB_FamilyNameW':udpUpdate[63:93], 
                        'SB_WazaAriW':udpUpdate[95], 
                        'SB_PinTimeW':udpUpdate[97:99], 
                        'SB_TeamScoreW':udpUpdate[99],
                        'SB_CountryB':self._cleanupCountry(udpUpdate[100:103]), 
                        'SB_WrlB':udpUpdate[122:125], 
                        'SB_FamilyNameB':udpUpdate[125:155], 
                        'SB_WazaAriB':udpUpdate[157], 
                        'SB_PinTimeB':udpUpdate[159:161], 
                        'SB_TeamScoreW':udpUpdate[161]}
                self.eventVisibleData = {'SB_GoldenScore':self._booleanCase(udpUpdate[162]), 
                        'SB_IpponW':self._booleanCase(udpUpdate[93]), 
                        'SB_IpponB':self._booleanCase(udpUpdate[155]), 
                        'SB_PinTimerW':self._pinTimerVisible(udpUpdate[97:99]), 
                        'SB_PinTimerB':self._pinTimerVisible(udpUpdate[159:161]), 
                        'SB_MatchStarted':self._matchStatus(udpUpdate[210])}
                self.eventFaultData = {'SB_ShidoHansW':udpUpdate[96], 
                        'SB_ShidoHansB':udpUpdate[158]} 
                self.eventFlagData = {'SB_FlagW':self._selectFlagImage(udpUpdate[38:41]),  
                        'SB_FlagB':self._selectFlagImage(udpUpdate[100:103])}

        def toObsObjects(self):
                #Iterate through the dictionaries, collect only the changed attributes and return this in a list of OBS objects
                sb_list = []                                                      #Empty scorebord list to fill and return
                for key in self.eventTextData.keys():                             #Update changed text fields
                        if self.eventTextData[key] != self.oldEventData[key]:
                                data = 'SetTextGDIPlusProperties',{'source': key, 'text': self.eventTextData[key]}
                                sb_list.append(data)
                
                for key in self.eventVisibleData.keys():                          #Update changed text field
                        if self.eventVisibleData[key] != self.oldEventData[key]:
                                data = 'SetSceneItemProperties',{'item': key, 'visible': self.eventVisibleData[key]}
                                sb_list.append(data)

                for key in self.eventFaultData.keys():                            #Update changed visibility on Shido (1,2,3)/Hansokumake(H)
                        if self.eventFaultData[key] != self.oldEventData[key]:             #Fault (Shido/Hansokumake) data has changed
                                a = self._faultCase(self.eventFaultData[key])          #Get the list of Shido/fault status
                                if key == 'SB_ShidoHansW':                            #Start sending faults for A
                                        data = 'SetSceneItemProperties',{'item': 'SB_ShidoW1', 'visible': a[0]}
                                        sb_list.append(data)
                                        data = 'SetSceneItemProperties',{'item': 'SB_ShidoW2', 'visible': a[1]}
                                        sb_list.append(data)
                                        data = 'SetSceneItemProperties',{'item': 'SB_HansokumakeW', 'visible': a[2]}
                                        sb_list.append(data)
                                        #print ('FaultA: ' + str(a[0]), str(a[1]), str(a[2]))
                                elif 'SB_ShidoHansB':                                 #Start sending faults for B
                                        data = 'SetSceneItemProperties',{'item': 'SB_ShidoB1', 'visible': a[0]}
                                        sb_list.append(data)
                                        data = 'SetSceneItemProperties',{'item': 'SB_ShidoB2', 'visible': a[1]}
                                        sb_list.append(data)
                                        data = 'SetSceneItemProperties',{'item': 'SB_HansokumakeB', 'visible': a[2]}
                                        sb_list.append(data)
                                        #print ('FaultB: ' + str(a[0]), str(a[1]), str(a[2])) 
                
                for key in self.eventFlagData.keys():                             #Update changed text fields
                        if self.eventFlagData[key] != self.oldEventData[key]:
                                data = 'SetSourceSettings',{'sourceName': key, 'sourceSettings': {'file': self.eventFlagData[key]}} 
                                sb_list.append(data)
                
              
                

                return(sb_list)

        def update_state(self):
                '''Overwrite old records with new values to see if something changed in the next loop. Updates the old'''
                self.oldEventData = self.eventTextData.copy()                
                self.oldEventData.update(self.eventVisibleData)
                self.oldEventData.update(self.eventFaultData)
                self.oldEventData.update(self.eventFlagData)
                
        def update_sb(self, udpUpdate):
                '''Wrapper method. Takes IJF udp data as utf-8 string  input. Returns a list of dictionaries of changes OBS objects'''
                self.deserializeIjf(udpUpdate)                                        #Deserialize IIJF udp data into OBS objects
                result = self.toObsObjects()                                          #Collect only the changd obejects since last run
                self.update_state()                                                   #Now set the new state to the old state so that only changes can be detected next run
                return (result)                                                       #Return the list of changes OBS objects

sb=Deser_ijf(defaultCountry, flagsDirectory)

scoreBoardInstances = []

async def make_request_loop():
        import logging
        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(level=logging.DEBUG,
                            format = LOG_FORMAT)
        try:
                await ws.connect() 
        except:
                logging.error("Connection to OBS server error. Is the OBS server websocket running, or password set? ")
                time.sleep(5)
                exit(0)

        logging.info ("IJF2OBS interface ready. \n- Listening for IJF Scoreboard data on port: " + str(udpPort) + "\n- Connected on OBS Server on port: " + str(wsPort))

        '''Main loop. Run forever'''
        while True:
                recieved = sock.recvfrom(1024)
                udpUpdate = recieved[0].decode('UTF-8')
                ip = str(recieved[1][0])
                mat = udpUpdate[209]

                #loop.run_until_complete(make_request(sb_list))
                for i in sb.update_sb(udpUpdate):                                     #Iterate through thje message list to be sent
                        result = await ws.call(i[0], i[1])
                        # needs looking into - logging.info ("Host: %s", str(recieved[1]), "Mat: " , udpUpdate[209], " Updated te OBS objects: %s",  i[0] ," %s", str(i[1]), " With the result: %s", result)
                        print ("Host: ", ip) 
                        print ("Mat: " , mat)
                        print (" Updated te OBS objects: ",  i[0] ," ", str(i[1]))
                        print (" With the result: ", result)     #Field 209 is the mat nr 0-9 his should select the instance to update 

loop.run_until_complete(make_request_loop())