#!/usr/bin/env python3
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import pyqtSlot
#import rospy
import redis
import time
from threading import Thread

class EmbTerminal(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmbTerminal, self).__init__(parent)
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.terminal)
        # Works also with urxvt:
        self.process.start('urxvt',['-embed', str(int(self.winId()))])
        self.setFixedSize(500, 431)
        self.thread_flag = False

class main_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        self.r = redis.Redis()
        self.window()
        self.frame()
        self.gridlayout()
        self.pushbutton()
        self.label()
        self.lcd_number()
        # mbTerminal()
        # th = Thread(target = self.read_data)
        # th.start()
        self.connect()

    def window(self):
        self.setWindowTitle("Ros")
        #self.resize(600, 480) 

    def frame(self):
        self.move_frame = QtWidgets.QFrame(self)
        self.move_frame.setGeometry(QtCore.QRect(0, 225, 300, 300))
        self.move_frame.setStyleSheet("background-color : rgb(0, 255, 0)")

        self.info_frame = QtWidgets.QFrame(self)
        self.info_frame.setGeometry(QtCore.QRect(300, 0, 500, 800))
        self.info_frame.setStyleSheet("background-color : rgb(199, 0, 0)")

    def gridlayout(self):
        self.move_gridLayoutWidget= QtWidgets.QWidget(self.move_frame)
        self.move_gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 300, 300))
        self.move_gridLayoutWidget.setObjectName("move_gridLayoutWidget")

        self.move_gridLayout = QtWidgets.QGridLayout(self.move_gridLayoutWidget)
        self.move_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.move_gridLayout.setObjectName("move_gridLayout")

        self.info_gridLayoutWidget= QtWidgets.QWidget(self.info_frame)
        self.info_gridLayoutWidget.setGeometry(QtCore.QRect(0, 80, 500, 720))
        self.info_gridLayoutWidget.setObjectName("info_gridLayoutWidget")

        self.info_gridLayout = QtWidgets.QGridLayout(self.info_gridLayoutWidget)
        self.info_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.info_gridLayout.setObjectName("info_gridLayout")

    def pushbutton(self):
        self.read_data_pushbutton = QtWidgets.QPushButton(self)
        self.read_data_pushbutton.setStyleSheet("background-color:rgb(255,255,0)")
        self.read_data_pushbutton.setGeometry(QtCore.QRect(0, 0, 100, 50))
        self.read_data_pushbutton.setText("Read")

        self.stop_Readdata_pushbutton = QtWidgets.QPushButton(self)
        self.stop_Readdata_pushbutton.setStyleSheet("background-color:rgb(255,255,0)")
        self.stop_Readdata_pushbutton.setGeometry(QtCore.QRect(200, 0, 100, 50))
        self.stop_Readdata_pushbutton.setText("Stop Read")


        self.move_forward_pushbutton = QtWidgets.QPushButton(self.move_gridLayoutWidget)
        self.move_forward_pushbutton.setStyleSheet("background-color:rgb(255,255,0)")
        #                                                     left up
        # self.move_forward_pushbutton.setGeometry(QtCore.QRect(175, 0, 100, 50))
        self.move_forward_pushbutton.setText("Forward")
        self.move_gridLayout.addWidget(self.move_forward_pushbutton, 0, 3, 1, 1)


        self.move_back_pushbutton = QtWidgets.QPushButton(self.move_gridLayoutWidget)
        self.move_back_pushbutton.setStyleSheet("background-color:rgb(255,0,255)")
        # self.move_back_pushbutton.setGeometry(QtCore.QRect(100, 100, 100, 50))
        self.move_back_pushbutton.setText("Back")
        self.move_gridLayout.addWidget(self.move_back_pushbutton, 2, 3, 1, 1)

        self.move_left_pushbutton = QtWidgets.QPushButton(self.move_gridLayoutWidget)
        self.move_left_pushbutton.setStyleSheet("background-color:rgb(255,0,120)")
        # self.move_left_pushbutton.setGeometry(QtCore.QRect(175, 200, 100, 50))
        self.move_left_pushbutton.setText("Left")
        self.move_gridLayout.addWidget(self.move_left_pushbutton, 1, 2, 1, 1)

        self.move_right_pushbutton = QtWidgets.QPushButton(self.move_gridLayoutWidget)
        self.move_right_pushbutton.setStyleSheet("background-color:rgb(255,120,0)")
        # self.move_right_pushbutton.setGeometry(QtCore.QRect(250, 100, 100, 50))
        self.move_right_pushbutton.setText("Right")
        self.move_gridLayout.addWidget(self.move_right_pushbutton, 1, 4, 1, 1)

        self.move_stop_pushbutton = QtWidgets.QPushButton(self.move_gridLayoutWidget)
        self.move_stop_pushbutton.setStyleSheet("background-color:rgb(255,0,0)")
        self.move_stop_pushbutton.setText("Stop")
        self.move_gridLayout.addWidget(self.move_stop_pushbutton, 1, 3, 1, 1)
    
    def label(self):
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        font.setWeight(40)

        self.status_label = QtWidgets.QLabel(self.info_frame)
        self.status_label.setGeometry(QtCore.QRect(90, 30, 321, 20))
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setText("Status")

        self.x_label = QtWidgets.QLabel(self.info_gridLayoutWidget)
        self.x_label.setFont(font)
        self.x_label.setText("X :")
        self.info_gridLayout.addWidget(self.x_label, 0, 1, 1, 1)

        self.y_label = QtWidgets.QLabel(self.info_gridLayoutWidget)
        self.y_label.setFont(font)
        self.y_label.setText("Y :")
        self.info_gridLayout.addWidget(self.y_label, 1, 1, 1, 1)

        self.theta_label = QtWidgets.QLabel(self.info_gridLayoutWidget)
        self.theta_label.setFont(font)
        self.theta_label.setText("Theta :")
        self.info_gridLayout.addWidget(self.theta_label, 2, 1, 1, 1)

        self.linearVelocity_label = QtWidgets.QLabel(self.info_gridLayoutWidget)
        self.linearVelocity_label.setFont(font)
        self.linearVelocity_label.setText("Linear Velocity :")
        self.info_gridLayout.addWidget(self.linearVelocity_label, 3, 1, 1, 1)

        self.angularVelocity_label = QtWidgets.QLabel(self.info_gridLayoutWidget)
        self.angularVelocity_label.setFont(font)
        self.angularVelocity_label.setText("Angular Velocity :")
        self.info_gridLayout.addWidget(self.angularVelocity_label, 4, 1, 1, 1)
        
    def lcd_number(self):
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(15)
        font.setWeight(40)

        self.x_lcdNumber = QtWidgets.QLCDNumber(self.info_gridLayoutWidget)
        self.x_lcdNumber.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.x_lcdNumber.setDigitCount(10)
        self.x_lcdNumber.setProperty("value", 0)
        self.x_lcdNumber.setFont(font)
        self.info_gridLayout.addWidget(self.x_lcdNumber, 0, 2, 1, 1)

        self.y_lcdNumber = QtWidgets.QLCDNumber(self.info_gridLayoutWidget)
        self.y_lcdNumber.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.y_lcdNumber.setDigitCount(10)
        self.y_lcdNumber.setProperty("value", 1)
        self.info_gridLayout.addWidget(self.y_lcdNumber, 1, 2, 1, 1)

        self.theta_lcdNumber = QtWidgets.QLCDNumber(self.info_gridLayoutWidget)
        self.theta_lcdNumber.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.theta_lcdNumber.setDigitCount(10)
        self.theta_lcdNumber.setProperty("value", 2)
        self.info_gridLayout.addWidget(self.theta_lcdNumber, 2, 2, 1, 1)

        self.linearVelocity_lcdNumber = QtWidgets.QLCDNumber(self.info_gridLayoutWidget)
        self.linearVelocity_lcdNumber.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.linearVelocity_lcdNumber.setDigitCount(10)
        self.linearVelocity_lcdNumber.setProperty("value", 3)
        self.info_gridLayout.addWidget(self.linearVelocity_lcdNumber, 3, 2, 1, 1)

        self.angularVelocity_lcdNumber = QtWidgets.QLCDNumber(self.info_gridLayoutWidget)
        self.angularVelocity_lcdNumber.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.angularVelocity_lcdNumber.setDigitCount(10)
        self.angularVelocity_lcdNumber.setProperty("value", 4)
        self.info_gridLayout.addWidget(self.angularVelocity_lcdNumber, 4, 2, 1, 1)

        self.info_gridLayout.addWidget(EmbTerminal(), 6, 1, 1, 1)
        
    def read_data(self):
        while self.thread_flag:
            incoming_msg = self.r.rpop('incoming_messages')
            if incoming_msg is None:
                time.sleep(0.1)
            else:
                incoming_msg = incoming_msg.decode().split(",")
                # print(incoming_msg)
                if incoming_msg[0] != '':
                    self.x_lcdNumber.display(float(incoming_msg[0]))
                    self.y_lcdNumber.display(float(incoming_msg[1]))
                    self.theta_lcdNumber.display(float(incoming_msg[2]))
                    self.linearVelocity_lcdNumber.display(float(incoming_msg[3]))
                    self.angularVelocity_lcdNumber.display(float(incoming_msg[4]))
                else:
                    pass
                time.sleep(0.1)
    

    def connect(self):
        self.stop_Readdata_pushbutton.clicked.connect(self.on_stop_read)
        self.read_data_pushbutton.clicked.connect(self.on_read_data)
        self.move_forward_pushbutton.clicked.connect(self.on_move_forward)
        self.move_back_pushbutton.clicked.connect(self.on_move_back)
        self.move_left_pushbutton.clicked.connect(self.on_move_left)
        self.move_right_pushbutton.clicked.connect(self.on_move_right)
        self.move_stop_pushbutton.clicked.connect(self.on_move_stop)



    @pyqtSlot()
    def on_read_data(self):
        print("In thread")
        self.thread_flag = True
        th = Thread(target = self.read_data)
        th.start()

    def on_stop_read(self):
        self.thread_flag = False
        
    def on_move_stop(self):
        self.r.rpush('outgoing_messages', "close")

    def on_move_forward(self):
        print("forward")
        self.r.rpush('outgoing_messages', "forward")
    
    def on_move_back(self):
        print("back")
        self.r.rpush('outgoing_messages', "back")

    def on_move_left(self):
        print("left")
        self.r.rpush('outgoing_messages', "left")

    def on_move_right(self):
        print("right")
        self.r.rpush('outgoing_messages', "right")

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = main_window()
    w.show()
    w.setFixedSize(800, 800) 
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
