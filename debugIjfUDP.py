import socket

port = 5000

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

sock.bind(("", port))

#print ("server started")

while True:
   recieved = sock.recvfrom(1024)
#   print (type(recieved))
#   print (recieved[0])
   udpUpdate = recieved[0].decode('UTF-8')
   #udpUpdate = recieved[0]
   print(udpUpdate)

'''
   print (udpUpdate[4:24])      #Event_name <20>
   print (udpUpdate[24])        #Gender <1>
   print (udpUpdate[25:29])     #Category <4>
   print (udpUpdate[29:33])     #Unkonwn <4>
   print (udpUpdate[34])           #0= time stopped 1=time started <1>
#   print (udpUpdate[35])        #Minutes left <1>
#   print (udpUpdate[36:38])     #Seconds left <2>
   print (udpUpdate[35],udpUpdate[36:38],sep=':')     #Time left <3>

   print (udpUpdate[38:41])     #Country #1 <3> 
   print (udpUpdate[41:60])     #Unknown #1 <19>
   print (udpUpdate[60:63])     #WRL #2 <3>
   print (udpUpdate[63:93])     #Family Name #1 <30>
   #----Scores----
   print (udpUpdate[93])        #Ipppon #1 <1>
   print (udpUpdate[94])        #Unkown #1 <1> (probably used for Yuko)
   print (udpUpdate[95])        #Waza-ari #1 <1>
   #----Penalties----
   print (udpUpdate[96])        #Shido (1,2,3)/Hansokumake(H) #1 <1>
   print (udpUpdate[97:99])     #Pin Time #1 <2>
   print (udpUpdate[100])       #Unknown #1 <1>

   print (udpUpdate[100:103])   #Country #2 <3> 
   print (udpUpdate[103:122])   #Unknown #2 <19>
   print (udpUpdate[122:125])   #WRL #2 <3>
   print (udpUpdate[125:155])   #Family Name #2 <30>
   #----Scores----
   print (udpUpdate[155])       #Ipppon #2 <1>
   print (udpUpdate[156])       #Unkown #2 <1> (probably used for Yuko)
   print (udpUpdate[157])       #Waza-ari #2 <1>
   #----Penalties----
   print (udpUpdate[158])       #Shido (1,2,3)/Hansokumake(H) #2 <1>
   print (udpUpdate[159:161])   #Pin Time #2 <2>
   print ('pintomerB')
   print (udpUpdate[161])       #Unknown #2 <1>

   print (udpUpdate[162])       #Golden Score
   print (udpUpdate[163])       #Winner W= White, B=Blue
   print (udpUpdate[164:213])   #Rest
   print (udpUpdate[210])          #6=Score board on 1=Configuration mode <1> 

   print (time.asctime())   #bytes object

'''
