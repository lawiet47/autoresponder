from cb_logger import *
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from concurrent.futures import wait
from concurrent.futures import *
import csv
import click
import os, sys, re
import base64

def getFaultyEntries(elist, mode):
	Faulty_entry_list=[]
	for index in range(0,len(elist)):
		if len(elist[index]) < 1:
				Faulty_entry_list.append(index)
		else:
			if mode == "SENSOR" or mode == "FILE" or mode == "REGKEY" or mode == "SERVICE" or mode == "TASK" or mode == "WMI":
				if (all(c != '' or c != '\n' for c in elist[index])) == False:
					Faulty_entry_list.append(index)
			elif mode == "HASH":
				regex = "([a-fA-F\d]{%d})" % len(elist[index])
				if (all(c != '' or c != '\n' for c in elist[index])) == False or len(re.findall(regex, elist[index])) == 0:
					Faulty_entry_list.append(index)
			elif mode == "PID":
				try:
					int(elist[index])
				except ValueError:
					Faulty_entry_list.append(index)
				if (all(c != '' or c != '\n' for c in elist[index])) == False:
					Faulty_entry_list.append(index)
			else:
				pass
	return Faulty_entry_list


def createLogFile(filename):
	try:
		file=open(filename, 'w', newline='')
		return file
	except Exception as e:
		log.warn("Exception Occured \033[37mERROR\033[33m: %s" % str(e))
	return None

def createOutputPath(path):
	STATE=False
	if path == '':
		path ='.'
	if not os.path.exists(path):
		try:
			os.makedirs(path)
			ftemp=open("%s\\%s" % (path, "CBR_AccessCheckTemp.txt"), 'w')
			STATE = True
			ftemp.close()
			os.remove("%s\\%s" % (path, "CBR_AccessCheckTemp.txt"))
		except Exception as e:
			log.warn("Exception Occured \033[37mERROR\033[33m: %s" % str(e))
	else:
		try:
			ftemp=open("%s\\%s" % (path, "CBR_AccessCheckTemp.txt"), 'w')
			STATE = True
			ftemp.close()
			os.remove("%s\\%s" % (path, "CBR_AccessCheckTemp.txt"))
		except Exception as e:
			log.warn("Exception Occured \033[37mERROR\033[33m: %s" % str(e))
	return STATE

def createSensorLogFile(filename):
	try:
		file=open(filename, 'wb')
		return file
	except Exception as e:
		log.warn("Exception Occured \033[37mERROR\033[33m: %s" % str(e))
	return None

def read_file(filename):
	file_content=""
	try:
		with open(filename,"r") as f:
			file_content=f.read().split('\n')
		return file_content
	except Exception as e:
		log.error("Exception Occured: "+str(e))
	return ""

