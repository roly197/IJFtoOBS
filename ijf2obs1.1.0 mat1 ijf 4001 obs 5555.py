#from asyncio.windows_events import IocpProactor
import socket
import asyncio
import time
import os
import simpleobsws 

'''---------------------------------Setup variables-------------------------'''
udpPort = 4001                                                    #UDP listening port for IJF SB to connect to
udpIp = ""                                                         #UDP IP for IJF SB to connect to. Keep empty to liten to te bradcast address,

wsPort = '5555'                                                    #Websocket port to connect to OBS Server
wsHost = '127.0.0.1'                                               #Websocket IP to connect to OBS Server
wsPass = 'judo'                                                    #Password to connect to OBS Server

defaultCountry = 'JYU'                                             #Send default 3 digit country code when empty
#flagsDirectory = '/Users/roly/Projects/IJFtoOBS/flags/'           #Local Directory where all country flags are unzipped
flagsDirectory = os.getcwd()+'\\flags\\'                           #Automatically find the flags directory as a subdir to the executable location. Do not change!
'''--------------------------------------------------------------------------'''

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((udpIp, udpPort))

'''setup the Websocket to the OBS server running on this machine. port=4444, password=judo'''
loop = asyncio.get_event_loop()
ws = simpleobsws.obsws(host=wsHost, port=wsPort, password=wsPass, loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.

ts = time.time()
scoreBoardInstances = {}                                                              #Create a dictionary with instances of scoreboards. UNique id is the mat # (0..9)

class Deser_ijf():
        def __init__(self, default_country=None, flags_directory=None, mat = '1', ip = None):
                import logging
                self.logger = logging.getLogger("UDPtoOBSserializer")
                self.default_country = default_country
                self.ip = ip 
                self.mat = mat
                self.subst = ('SB'+mat+'_')
                self.flags_directory = flags_directory
                self._resetObjects()
        
        def _resetObjects (self):
            self.oldEventData = {self.subst+'EventName':'', 
                                        self.subst+'Gender':'', 
                                        self.subst+'Category':'', 
                                        self.subst+'MatchType':'', 
                                        self.subst+'Time':'', 
                                        self.subst+'GoldenScore':'', 
                                        self.subst+'Winner':'', 
                                        self.subst+'MatchStarted':'',
                                        self.subst+'CountryW':'',
                                        self.subst+'FlagW':'', 
                                        self.subst+'WrlW':'', 
                                        self.subst+'FamilyNameW':'', 
                                        self.subst+'IpponW':'', 
                                        self.subst+'WazaAriW':'', 
                                        self.subst+'ShidoHansW':'', 
                                        self.subst+'PinTimerW':'', 
                                        self.subst+'TeamScoreW':'',
                                        self.subst+'CountryB':'', 
                                        self.subst+'FlagB':'', 
                                        self.subst+'WrlB':'', 
                                        self.subst+'FamilyNameB':'', 
                                        self.subst+'IpponB':'', 
                                        self.subst+'WazaAriB':'', 
                                        self.subst+'ShidoHansB':'', 
                                        self.subst+'PinTimerB':'', 
                                        self.subst+'TeamScoreB':''}
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
                self.eventTextData = {self.subst+'EventName':udpUpdate[4:24], 
                        self.subst+'Gender':self._genderCase(udpUpdate[24]), 
                        self.subst+'Category':(udpUpdate[25:29]+'kg'), 
                        self.subst+'MatchType':self._matchTypeCase(udpUpdate[30]),
                        self.subst+'Time':(udpUpdate[35]+':'+udpUpdate[36:38]), 
                        self.subst+'Winner':self._winnerCase(udpUpdate[163]), 
                        self.subst+'CountryW':self._cleanupCountry(udpUpdate[38:41]),
                        self.subst+'WrlW':udpUpdate[60:63], 
                        self.subst+'FamilyNameW':udpUpdate[63:93], 
                        self.subst+'WazaAriW':udpUpdate[95],  
                        self.subst+'TeamScoreW':udpUpdate[99],
                        self.subst+'CountryB':self._cleanupCountry(udpUpdate[100:103]), 
                        self.subst+'WrlB':udpUpdate[122:125], 
                        self.subst+'FamilyNameB':udpUpdate[125:155], 
                        self.subst+'WazaAriB':udpUpdate[157],  
                        self.subst+'TeamScoreB':udpUpdate[161]}
                self.eventVisibleData = {self.subst+'GoldenScore':self._booleanCase(udpUpdate[162]), 
                        self.subst+'IpponW':self._booleanCase(udpUpdate[93]), 
                        self.subst+'IpponB':self._booleanCase(udpUpdate[155]), 
                        self.subst+'MatchStarted':self._matchStatus(udpUpdate[210])}
                self.eventPinTimer = {self.subst+'PinTimerW':udpUpdate[97:99], 
                        self.subst+'PinTimerB':udpUpdate[159:161]}
                self.eventFaultData = {self.subst+'ShidoHansW':udpUpdate[96], 
                        self.subst+'ShidoHansB':udpUpdate[158]} 
                self.eventFlagData = {self.subst+'FlagW':self._selectFlagImage(udpUpdate[38:41]),  
                        self.subst+'FlagB':self._selectFlagImage(udpUpdate[100:103])}

        def toObsObjects(self):
                #Iterate through the dictionaries, collect only the changed attributes and return this in a list of OBS objects
                sb_list = []                                                      #Empty scorebord list to fill and return
                for key in self.eventTextData.keys():                             #Update changed text fields
                        if self.eventTextData[key] != self.oldEventData[key]:
                                data = 'SetTextGDIPlusProperties',{'source': key, 'text': self.eventTextData[key]}
                                sb_list.append(data)
                
                for key in self.eventPinTimer.keys():                          #Update changed text field
                        #print (self.eventPinTimer[key])
                        #print (self.oldEventData[key])
                        if self.eventPinTimer[key] != self.oldEventData[key]:
                            if int(self.eventPinTimer[key]) == 0: 
                                data = 'SetSceneItemRender',{'source': key, 'render': False}
                                sb_list.append(data)
                            else: 
                                data = 'SetSceneItemRender',{'source': key, 'render': True}
                                sb_list.append(data)
                                data = 'SetTextGDIPlusProperties',{'source': key, 'text': self.eventPinTimer[key]}
                                sb_list.append(data)
                                

                for key in self.eventVisibleData.keys():                          #Update changed text field
                        if self.eventVisibleData[key] != self.oldEventData[key]:
                                data = 'SetSceneItemRender',{'source': key, 'render': self.eventVisibleData[key]}
                                sb_list.append(data)

                for key in self.eventFaultData.keys():                            #Update changed visibility on Shido (1,2,3)/Hansokumake(H)
                        if self.eventFaultData[key] != self.oldEventData[key]:             #Fault (Shido/Hansokumake) data has changed
                                a = self._faultCase(self.eventFaultData[key])          #Get the list of Shido/fault status
                                if key == self.subst+'ShidoHansW':                            #Start sending faults for A
                                        data = 'SetSceneItemRender',{'source': self.subst+'ShidoW1', 'render': a[0]}
                                        sb_list.append(data)
                                        data = 'SetSceneItemRender',{'source': self.subst+'ShidoW2', 'render': a[1]}
                                        sb_list.append(data)
                                        data = 'SetSceneItemRender',{'source': self.subst+'HansokumakeW', 'render': a[2]}
                                        sb_list.append(data)
                                        #print ('FaultA: ' + str(a[0]), str(a[1]), str(a[2]))
                                elif self.subst+'ShidoHansB':                                 #Start sending faults for B
                                        data = 'SetSceneItemRender',{'source': self.subst+'ShidoB1', 'render': a[0]}
                                        sb_list.append(data)
                                        data = 'SetSceneItemRender',{'source': self.subst+'ShidoB2', 'render': a[1]}
                                        sb_list.append(data)
                                        data = 'SetSceneItemRender',{'source': self.subst+'HansokumakeB', 'render': a[2]}
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
                self.oldEventData.update(self.eventPinTimer)
                
        def update_sb(self, udpUpdate, redraw=False):
                '''Wrapper method. Takes IJF udp data as utf-8 string  input. Returns a list of dictionaries of changes OBS objects'''
                self.deserializeIjf(udpUpdate)                                        #Deserialize IIJF udp data into OBS objects
                self.logger.debug ('Scoreboard instance for mat: %s deserializes IJF message: %s', self.mat, udpUpdate)

                if redraw:                                                            #If redraw == True then the Scene has changed. This requires all objects to be updated 
                    self._resetObjects()
                result = self.toObsObjects()                                          #Collect only the changed objects since last run
                self.logger.debug ('Scoreboard instance for mat: %s creates obes objects for updated records.', self.mat)

                self.update_state()                                                   #Now set the new state to the old state so that only changes can be detected next run
                self.logger.debug ('Scoreboard instance for mat: %s new OBS objects overwrites old OBS objects to find changes in next update.', self.mat)

                return (result)                                                       #Return the list of changes OBS objects

async def make_request_loop():
        import logging
        oldScene = ''

        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(level=logging.INFO,
                            format = LOG_FORMAT)
        try:
                await ws.connect() 
        except:
                logging.error("Connection to OBS server error. Is the OBS server websocket running, or password set? ")
                time.sleep(5)
                exit(0)

        logging.info ("IJF2OBS interface ready. \n- Listening for IJF Scoreboard data on port: " + str(udpPort) + "\n- Connected on OBS Server on port: " + str(wsPort))

        '''Main loop. Listen to broadcast data from IJF scoreboards and run until keyboard interrupt'''
        while True:
                recieved = sock.recvfrom(1024)
                udpUpdate = recieved[0].decode('UTF-8')
                ip = str(recieved[1][0])
                mat = udpUpdate[209]                                                  #From the received message get the mat# as int to use as a unique identifier

                result = await ws.call('GetCurrentScene')                             #Get current active scene
                currentScene = (result['name'])                                       #Check currentscene to check if cscene has changed and a redraw is needed
                if currentScene != oldScene: 
                    redraw = True
                    logging.info ('OBS Scene has changed from %s to %s, redrawing all Scene objects: ', oldScene, currentScene)
                else:
                    redraw = False
                oldScene = currentScene

                result = await ws.call('SetTextGDIPlusProperties', {'source': 'SB_Matnumber', 'text': mat}) # Updata generic mat identifier

                if mat in scoreBoardInstances.keys():                                 # Check if an instance with mat # exists
                        if ip !=scoreBoardInstances[mat].ip:                          # Check if the ip source is identical to the source that created the sb object
                                logging.error ('Duplicate scorebords %s and %s reporting updates on mat: %s', ip, scoreBoardInstances[mat].ip, mat )
                        for i in scoreBoardInstances[mat].update_sb(udpUpdate, redraw):       #If exists: Iterate through the message list to be sent
                            result = await ws.call(i[0], i[1])                        #Send inidividual results to the OBS websocket
                            logging.info ('Updated: host %s, mat %s updated the OBS object %s %s. With result: %s', ip, mat, i[0], i[1], result)
                else:
                        scoreBoardInstances[mat] = Deser_ijf(defaultCountry, flagsDirectory, mat, ip)   #If not exists, first create a k,v with mat, object in the dictionary
                        logging.info ('New instance of OBS scoreboard handler created for mat: %s. Source: %s', mat, ip)
                        for i in scoreBoardInstances[mat].update_sb(udpUpdate):       #With the new instance: Iterate through the message list to be sent
                            result = await ws.call(i[0], i[1])                        #Send inidividual results to the OBS websocket
                            logging.info ('Updated: host %s, mat %s updated the OBS object %s %s. With result: %s', ip, mat, i[0], i[1], result)

loop.run_until_complete(make_request_loop())