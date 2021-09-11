import serial
import time

ser=serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=0.1, rtscts=0)

def sendCommand(com):
	ser.write(str.encode(com+"\r\n"))
	time.sleep(0.5)
	ret = []
	while ser.inWaiting() > 0:
		msg = ser.readline().strip()
		#print("debug1: "+msg)
		msg = msg.replace("\r","")
		msg = msg.replace("\n","")
		if msg!="":
			ret.append(msg)
	return ret

def readSMS():
	list = sendCommand("AT+CMGL=\"ALL\"")
	#print(list)
	ret = []
	count=0
	time = []
	msn = []
	text = []
	for item in list:
		#print(item)
		if item.startswith("+CMGL:"):
			count+=1
			#print(item)
			data = item.split(',',4)
			time.append(data[4])
			data[2] = data[2].replace("\"","")
			msn.append(ucs2decode(data[2]))
		if item.startswith("+CMGL:") == False:
			if item!="OK":
				#print(item)
				text.append(ucs2decode(item))
	if (count):
		for i in range(count):
			print(time[i]+"	"+msn[i]+"	"+text[i])

def killSMS():
	com="ERROR"
	com=sendCommand("AT+CMGD=,1")
	#print("debug3: "+com[0])

def ucs2decode(text):
	ret = unicode(text.decode("hex"), "utf-16-be", "ignore").encode("utf8", "ignore")
	#print("debug5: "+ret)
	return ret

def main():
	# return
	
	#print("SENDING HELLO")
	com="ERROR"
	count=0
	while(com[0]!="OK"):
		com=sendCommand("ATE0")
		#print("debug2: "+com[0])
		count+=1
		if(count>5):
			#print("COULD NOT GET OK")
			return

	#print("SENDING TEXT MODE")
	com="ERROR"
	count=0
	while(com[0]!="OK"):
		com=sendCommand("AT+CMGF=1")
		#print(com[0])
		count+=1
		if(count>5):
			#print("COULD NOT GET OK")
			return

	#print("SENDING NEW MESSAGE INDICATIONS")
        com="ERROR"
        count=0
        while(com[0]!="OK"):
                com=sendCommand("AT+CNMI=0,0,0,0,1")
                #print(com[0])
                count+=1
                if(count>5):
                        #print("COULD NOT GET OK")
                        return

	#print("SENDING CHARACTER SET")
	com="ERROR"
	count=0
        while(com[0]!="OK"):
                com=sendCommand("AT+CSCS=\"UCS2\"")
                #print(com[0])
                count+=1
                if(count>5):
                        #print("COULD NOT GET OK")
                        return

	#print("READ SMS MESSAGE")
	readSMS()
	#time.sleep(1)
	
	#print("DELETING READ MESSAGES")
	killSMS()

if __name__ == "__main__":
	if ser.isOpen():
		main()
	else:
		print("ERROR: CAN'T OPEN CONNECTION")
	ser.close()

