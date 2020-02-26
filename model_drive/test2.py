
import paho.mqtt.client as paho

#df1 = df(data={'x':0,'y':0,'FB_para':0}, columns=['x','y','FB_para'])

broker="49.50.165.20"
port=1883
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")

def on_message(client,userdata,msg):             #create function for callback
    print("You've got message")
    print(" : " + str(msg.payload))

client1= paho.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.on_message = on_message
client1.connect(broker,port)                                 #establish connection
client1.loop_start()
client1.subscribe("ggg", 0)
while True:
    chat = str(input())
    if chat is "QUIT":
        break
    ret = client1.publish("hhh", chat)
client1.loop_stop()
client1.disconnect()