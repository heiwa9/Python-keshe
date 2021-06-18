import time

import serial

ser = serial.Serial("COM5", 57600)  # 开启com5口，波特率115200，超时5
ser.flushInput()  # 清空缓冲区



def serial_read():
    count = ser.inWaiting()  # 获取串口缓冲区数据
    # if count:
    #     recv = ser.read(ser.in_waiting).decode("utf-8")  # 读出串口数据，数据采用gbk编码
    #     _time = int(time.time())
    #     data = [_time, int(recv[14: 16]), int(recv[31:33])]
    #     print(data)
    time.sleep(0.1)
