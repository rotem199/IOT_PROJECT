import subprocess
import sys


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])


# Example
if __name__ == '__main__':

    try:
        import paho.mqtt.client as mqtt

        print('Pass! Take a break and drink something :)')


    except:
        install('paho-mqtt')
        print('Failed! Check "paho" package installation!')
import paho.mqtt.client as mqtt
import time
import random
import sqlite3
global click
global button_click
button_click = 1
def get_status_airConditioner_by_number(airConditionerNumber):
    c.execute("SELECT * FROM airConditionersData WHERE airConditionerNumber=:airConditionerNumber", {'airConditionerNumber': airConditionerNumber})
    return c.fetchone()

def update_airConditioner(airConditionerNumber, open_close):
    with conn:
        c.execute("""UPDATE airConditionersData SET open_close = :open_close WHERE airConditionerNumber =:airConditionerNumber""",{'airConditionerNumber':airConditionerNumber, 'open_close':open_close})

def get_status_boiler_by_number(boilersNumber):
    c2.execute("SELECT * FROM boilersData WHERE boilersNumber=:boilersNumber", {'boilersNumber': boilersNumber})
    return c2.fetchone()

def update_boiler(boilersNumber, open_close):
    with conn2:
        c2.execute("""UPDATE boilersData SET open_close = :open_close WHERE boilersNumber =:boilersNumber""",{'boilersNumber':boilersNumber, 'open_close':open_close})

# broker list
brokers=["iot.eclipse.org","broker.hivemq.com",\
         "test.mosquitto.org"]

broker=brokers[1]


def on_log(client, userdata, level, buf):
        print("log: "+buf)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
def on_disconnect(client, userdata, flags, rc=0):
        print("DisConnected result code "+str(rc))
def on_message(client,userdata,msg):
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print("message received: ",m_decode)
        msg_parse(m_decode)

def msg_parse(m_decode):
        print(m_decode) 
        global button_click
        global click
        subString="Temperature:" 
        if subString in m_decode:    
            rez=float(m_decode.split('Temperature: ')[1].split(' Humidity:')[0])
            print(rez) 
            if rez >= 25 :
                client.publish(pub_topic,"too hot The the air conditioner turn on automaticly in all the rooms")
                conn2 = sqlite3.connect('airConditioners.db')
                c2=conn2.cursor()
                for airConditionerNumber in range(20):
                    c2.execute("""UPDATE airConditionersData SET open_close = :open_close WHERE airConditionerNumber =:airConditionerNumber""",{'airConditionerNumber':airConditionerNumber+1, 'open_close':'open'})
                    conn2.commit()
                time.sleep(3)
        elif "open" in m_decode:
            conn = sqlite3.connect('boilers.db')
            c=conn.cursor()
            c.execute("""UPDATE boilersData SET open_close = :open_close WHERE boilersNumber =:boilersNumber""",{'boilersNumber':21, 'open_close':'open'})
            conn.commit()
        elif "close" in m_decode:
            conn = sqlite3.connect('boilers.db')
            c=conn.cursor()
            c.execute("""UPDATE boilersData SET open_close = :open_close WHERE boilersNumber =:boilersNumber""",{'boilersNumber':21, 'open_close':'close'})
            conn.commit()
            
client = mqtt.Client("IOT_project", clean_session=True) # create new client instance

client.on_connect=on_connect  #bind call back function
client.on_disconnect=on_disconnect
client.on_log=on_log
client.on_message=on_message
print("Connecting to broker ",broker)
port=1883
client.connect(broker,port)     #connect to broker
pub_topic= 'IOT_PROJECT'



conn = sqlite3.connect('airConditioners.db')
conn2 = sqlite3.connect('boilers.db')
c=conn.cursor()
c2=conn2.cursor()
for airConditionerNumber in range(20):
    if (get_status_airConditioner_by_number(airConditionerNumber+1)[1] == "open"):
        client.publish(pub_topic," There are open air conditioners in the room " + str(airConditionerNumber+1)+" The system will close the air condition")
        update_airConditioner(airConditionerNumber+1, 'close')
        time.sleep(1.5)
        client.publish(pub_topic," The system closed the air conditioner")
    else:
        client.publish(pub_topic, "There are no open air conditioners in the room " + str(airConditionerNumber+1))
    time.sleep(1.5)
for boilersNumber in range(20):
    
    if (get_status_boiler_by_number(boilersNumber+1)[1] == "open"):
        client.publish(pub_topic," There are open boiler in shower " + str(boilersNumber+1)+" The system will close the boiler")
        update_boiler(boilersNumber+1, 'close')
        time.sleep(1.5)
        client.publish(pub_topic," The system closed the boiler")
    else:
        client.publish(pub_topic, "There are no open boiler in the showers " + str(boilersNumber+1))

    time.sleep(1.5)
client.publish(pub_topic, "The scan is finished all the air conditioners and boilers are colse ")
client.loop_start()
client.subscribe("IOT_PROJECT")
time.sleep(300)
client.loop_stop()

client.disconnect() # disconnect
print("End publish_client run script")






