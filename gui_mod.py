import threading
import time

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtChart import QLineSeries, QValueAxis, QChartView
from PyQt5.QtCore import QPointF, QThread, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QTableWidgetItem
from numpy import mean

import temp_hum
from dbutils import Mongo, MySQL

mongo = Mongo()


# mysql = MySQL()

def on_table(self):
    self.tableWidget.setHorizontalHeaderLabels(['时间', '温度', '湿度'])
    tabledata = mongo.read_all()
    numrows = len(tabledata)
    numcols = len(tabledata[0])
    for row in range(numrows):  # 遍历行
        for col in range(numcols):  # 遍历列
            if col == 0:
                newItem = QTableWidgetItem(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(tabledata[row][0]))))
            else:
                newItem = QTableWidgetItem(str(tabledata[row][col]))
            newItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(row, col, newItem)
    self.tableWidget.resizeColumnToContents(0)


def on_lcd(self):
    dht_data = mongo.read_ones()
    self.lcdNumber.display(int(dht_data[1]))
    self.lcdNumber_2.display(int(dht_data[2]))


def click_3():
    thread1 = Thread1()
    thread1.start()


def click_4():
    print("按键事件4")


class Thread1(QThread):  # 线程1
    def __init__(self):
        super().__init__()  ## 继承QThread

    def run(self):
        temp_hum.run()
        time.sleep(0.1)


class Thread2(QThread):  # 线程2
    def __init__(self):
        super().__init__()  ## 继承QThread

    def run(self):
        print("按键事件3_1")


def drawboard(self):
    series = QLineSeries()  # 定义LineSerise，将类QLineSeries实例化
    series_01 = QLineSeries()  # 创建曲线

    dht_data = mongo.read_all()
    data1 = []
    data2 = []
    for i in range(0, len(dht_data)):
        data1.append(QPointF(i, int(dht_data[i][1])))
        data2.append(QPointF(i, int(dht_data[i][2])))

    point_list = data1  # 定义折线点清单
    point_list_01 = data2  # 定义折线点清单

    series.append(point_list)  # 折线添加坐标点
    series.setName("温度")  # 折线命名

    series_01.append(point_list_01)  # 折线添加坐标点
    series_01.setName("湿度")  # 折线命名

    x_Aix = QValueAxis()  # 定义x轴，实例化
    x_Aix.setRange(0.00, 100.00)  # 设置量程
    x_Aix.setLabelFormat("%0.2f")  # 设置坐标轴坐标显示方式，精确到小数点后两位
    x_Aix.setTickCount(10)  # 设置x轴有几个量程
    x_Aix.setMinorTickCount(10)  # 设置每个单元格有几个小的分级

    y_Aix = QValueAxis()  # 定义y轴
    y_Aix.setRange(0.00, 100.00)
    y_Aix.setLabelFormat("%0.2f")
    y_Aix.setTickCount(10)
    y_Aix.setMinorTickCount(10)

    charView = QChartView(self.groupBox_3)  # 定义charView，父窗体类型为 Window
    charView.setGeometry(10, 20, 680, 255)  # 设置charView位置、大小
    # charView.resize(800, 600)
    charView.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

    charView.chart().addSeries(series)  # 添加折线
    charView.chart().addSeries(series_01)  # 添加折线

    charView.chart().setAxisX(x_Aix)  # 设置x轴属性
    charView.chart().setAxisY(y_Aix)  # 设置y轴属性
    charView.chart().createDefaultAxes()  # 使用默认坐标系
    # charView.chart().setTitleBrush(QBrush(Qt.cyan))  # 设置标题笔刷
    # charView.chart().setTitle("折线图标题")  # 设置标题
    charView.show()  # 显示charView


def setlabelText(self):
    temp_list = mongo.read_temp_list()
    hum_list = mongo.read_hum_list()
    temp = '温度:\n均值为:{:.2f}   最大值为:{:.2f} \n  最小值为:{:.2f}   平均差为:{:.2f}'.format(mean(temp_list), max(temp_list),
                                                                            min(temp_list), np.std(temp_list, ddof=1))
    hum = '湿度:\n均值为:{:.2f}   最大值为:{:.2f} \n  最小值为:{:.2f}   平均差为:{:.2f}'.format(mean(hum_list), max(hum_list),
                                                                           min(hum_list), np.std(hum_list, ddof=1))
    _translate = QtCore.QCoreApplication.translate
    self.label_3.setText(_translate("MainWindow", temp))
    self.label_4.setText(_translate("MainWindow", hum))
