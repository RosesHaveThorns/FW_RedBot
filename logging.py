import os
import time

class logger:

	self.currentLogPath = ""
	self.maxSize = 500	# max size of log files before a new one is created, in MB

	def __init__(self, maxSize=500):
		currentLogPath = "{str(time.strftime('%Y%m%d-%H%M%S'))}.LOG"
		self.maxSize = maxSize

	def ConvertBytesToMB(self, num):
		mb = num/1000000
		return mb

	def FileSize(self, filePath):
		if os.path.isfile(filePath):
			fileInfo = os.stat(filePath)
			return ConvertBytesToMB(fileInfo.st_size)
		return 0

	def log(self, txt):
		if FileSize(currentLogPath) > maxSize:
			currentLogPath = "{str(time.strftime('%Y%m%d-%H%M%S'))}.LOG"

		updateText = time.strftime("%Y-%m-%d %H:%M:%S") + " >>> " + txt + "\n"
		print(updateText)

		f_Log = open(currentLogPath, 'a+')
		f_Log.write(updateText)
		f_Log.close()
