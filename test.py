import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
                             QVBoxLayout, QApplication)
from random import uniform, normalvariate, randint
import time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        lcd = QLCDNumber(self)
        self.data=DataThread()
        vbox = QVBoxLayout()
        vbox.addWidget(lcd)

        self.setLayout(vbox)
        self.data.valueChanged.connect(lcd.display)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Callback')
        self.data.start()
        self.show()

class DataThread(QThread):
    valueChanged = pyqtSignal(object)
    val=0

    def on_message(mqttc, obj, msg):
        mstr=msg.payload.decode("ascii")
        val=mstr
        self.valueChanged.emit(val)

    def on_subscribe(mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def run(self):
        msg = subscribe.simple("shok2", hostname="broker.hivemq.com")
        print("%s %s" % (msg.topic, msg.payload))
        mqttc = mqtt.Client()
        mqttc.on_subscribe = self.on_subscribe
        mqttc.on_message = self.on_message
        mqttc.connect("broker.hivemq.com")
        print("subsrcibe")
        mqttc.subscribe("shok2")
        mqttc.loop_forever()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())