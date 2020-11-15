#!/usr/bin/env python3
# from __future__ import print_function
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import time
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from xnotify.notify import notify

PID = os.getpid()
print("PID:", PID)

class Datetray(QApplication):
	def __init__(self, *args, **kwargs):
		super(Datetray, self).__init__([])
		
		self.setQuitOnLastWindowClosed(False)
		self.now = datetime.now()
		self.next_time = datetime(self.now.year, self.now.month, self.now.day + 1, 23, 59, 59, 0)
		# self.next_time = datetime(self.now.year, self.now.month, self.now.day, 14, 7, 0, 0)

		self.sleep = self.next_time - self.now
		self.sleep = self.sleep.seconds
		self.name = os.path.join(os.path.dirname(__file__), 'date.png')
		self.draw_date()
		self.icon = QIcon(self.name)

		self.tray = QSystemTrayIcon()
		self.tray.setIcon(self.icon)
		self.tray.setVisible(True) 

		# Creating the options 
		self.menu = QMenu() 
		self.option1 = QAction("Update") 
		self.option1.triggered.connect(self.updateIcon)
		#option2 = QAction("GFG") 
		self.menu.addAction(self.option1) 
		#menu.addAction(option2) 

		# To quit the app 
		self.quit_action = QAction("Quit") 
		self.quit_action.triggered.connect(self.quit) 
		self.menu.addAction(self.quit_action) 

		# Adding options to the System Tray 
		self.tray.setContextMenu(self.menu) 
		self.timer = QTimer()
		msg = "Next Update => Sleep: " + str(self.get_jedi()) + " seconds => Update at: " + str(datetime.strftime(self.next_time, '%Y/%m/%d %H:%M:%S'))
		self.tray.setToolTip(msg)
		self.tray.showMessage('DateTray', msg, QSystemTrayIcon.Information)
		# self.tray.setToolTip("TEST setToolTip")
		notify("DateTray", "DateTray", "start", msg, icon = self.name, direct_run = True)
		self.timer.setInterval(self.get_jedi() * 1000)
		self.timer.timeout.connect(self.updateIcon)
		self.timer.start()

	def get_jedi(self):
		now = datetime.now()
		next_time = datetime(now.year, now.month, now.day + 1, 23, 59, 59, 0)
		return (next_time - datetime.now()).seconds

	def format_number(self, number, length = 10):
	    number = str(number).strip()
	    zeros = len(str(length)) - len(number)
	    r = ("0" * zeros) + str(number)
	    if len(r) == 1:
	        return "0" + r
	    return r
	 
	def draw_date(self):
		img = Image.new('RGB', (512, 512), color = (0, 0, 0))
		fontsize = 350
		font = ImageFont.truetype("arial.ttf", fontsize) 
		# while font.getsize(txt)[0] < img_fraction*image.size[0]:
		#     # iterate until the text size is just larger than the criteria
		#     fontsize += 1
		#     font = ImageFont.truetype("arial.ttf", fontsize)

		d = ImageDraw.Draw(img)
		d.text((55,180), self.format_number(str(datetime.now().day)), fill=(255,255,0), font=font)
		 
		img.save(self.name)

		month = Image.open(self.name)
		draw = ImageDraw.Draw(month)
		fontsize1 = 250
		font1 = ImageFont.truetype("arial.ttf", fontsize1) 
		# font1.set_variation_by_name('Bold')
		draw.text((5,1), self.format_number(str(datetime.now().month)), font=font1, fill='white')
		# draw.text((5,1), self.format_number(str(datetime.now().minute)), font=font1, fill='white')

		month.save(self.name)


	def updateIcon(self):
		self.tray.setVisible(False)
		print("Update ...")
		msg = "Update datetime to:", datetime.strftime(self.next_time, '%Y/%m/%d %H:%M:%S')
		notify("DateTray", "DateTray", "update", msg, icon = self.name, direct_run = True)
		msg1 = "Next Update => Sleep: " + str(self.get_jedi()) + " seconds => Update at: " + str(datetime.strftime(self.next_time, '%Y/%m/%d %H:%M:%S'))
		self.tray.setToolTip(msg1)
		self.tray.showMessage('DateTray', msg1, QSystemTrayIcon.Information)
		print(msg1)
		notify("DateTray", "DateTray", "update", msg1, icon = self.name, direct_run = True)
		self.draw_date()
		icon = QIcon(self.name)
		self.tray.setIcon(icon) 
		self.tray.setVisible(True) 

if __name__ == '__main__':
	c = Datetray()
	c.exec_()
		