from utils import *
from cbapi.response import*
from cbapi.errors import*
from cbapi.live_response_api import*
from cbapi.response.models import Process, Sensor, Binary, Watchlist, Feed, Investigation

def cbr_restart_endpoints(session, sensor):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	COMMAND_TO_RUN = "cmd.exe /C shutdown.exe /r /c \"Reboot command was issued by CBR sensor\""
	try:
		out=session.create_process(COMMAND_TO_RUN, wait_timeout=10)
		OUTPUT_MSG += "An endpoint restart was issued for the host\n"
		log.info("An endpoint restart was issued for the host \033[37mHOST:\033[36m %s" % sensor['hostname'])
	except LiveResponseError as cblrerr:
		CBLR_ERROR_MSG += "%s\n" % (str(cblrerr))
		log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, sensor['hostname']))
	except Exception as e:
		ERROR_MSG += "%s\n" % (str(e))
		log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), sensor['hostname']))
	
	return OUTPUT_MSG, ERROR_MSG, CBLR_ERROR_MSG

def cbr_find_file(session, sensor, ioc_name_list):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	FOUND_FILE=0
	for index in range(0, len(ioc_name_list)):
		DIRECTORY = os.path.dirname(str(ioc_name_list[index]))
		FILENAME = os.path.basename(str(ioc_name_list[index]))
		try:
			directory=session.list_directory(DIRECTORY+"\\")
			for file in directory:
				if file['filename'] == FILENAME:
					FOUND_FILE+=1
					OUTPUT_MSG +=str(ioc_name_list[index])+"\n"
					log.log(SUCCESS, "File was found \033[37mFILE:\033[32m %s \033[37mSIZE:\033[32m %s bytes \033[37mHOST:\033[32m %s" % (ioc_name_list[index], str(file['size']), sensor['hostname']))
		except LiveResponseError as cblrerr:
			if "ERROR_PATH_NOT_FOUND" not in str(cblrerr):
				CBLR_ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(cblrerr)))
				log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mFILE:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, str(ioc_name_list[index]), sensor['hostname']))
		except Exception as e:
			ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(e)))
			log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mFILE:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), str(ioc_name_list[index]), sensor['hostname']))
	if FOUND_FILE == 0:
		OUTPUT_MSG = ("Given IOCs are not found.")

	return OUTPUT_MSG, FOUND_FILE, ERROR_MSG, CBLR_ERROR_MSG

def cbr_get_tasks(session, sensor, output_path):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	COMMAND_TO_RUN = "cmd.exe /C schtasks.exe /query /FO CSV /v"
	filename=output_path+"\\"+sensor['hostname'] + "-Tasks.csv"
	try:
		out=session.create_process(COMMAND_TO_RUN, wait_timeout=10)
		sensor['output_content']=out
		OUTPUT_MSG = ("Successfully retrieved entries.")
		log.log(SUCCESS, "Successfully retrieved TASK entries \033[37mHOST:\033[32m %s", sensor['hostname'])
	except LiveResponseError as cblrerr:
		CBLR_ERROR_MSG += "%s\n" % (str(cblrerr))
		log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, sensor['hostname']))
	except Exception as e:
		ERROR_MSG += "%s\n" % (str(e))
		log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), sensor['hostname']))
	
	return filename, OUTPUT_MSG, ERROR_MSG, CBLR_ERROR_MSG

def cbr_get_wmi_persistence(session, sensor, output_path):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	COMMAND_TO_RUN = "cmd.exe /C powershell.exe -command \"$Classes= @('__EventFilter', '__EventConsumer', '__FilterToConsumerBinding') ; ForEach ($NameSpace in 'root/subscription','root/default', 'root/cimv2') { Write-Host '[NAMESPACE:' $Namespace ']'; Write-Host; ForEach ($Class  in $Classes) { Write-Host '[' $Class ']:'; Write-Host; get-wmiobject -namespace $NameSpace -class $Class} Write-Host '==============================================================';}\""
	filename=output_path+"\\"+sensor['hostname'] + "-WMI_Subscriptions.txt"
	try:
		out=session.create_process(COMMAND_TO_RUN, wait_timeout=10)
		sensor['output_content']=out
		OUTPUT_MSG = ("Successfully retrieved entries.")
		log.log(SUCCESS, "Successfully retrieved WMI entries \033[37mHOST:\033[32m %s", sensor['hostname'])
	except LiveResponseError as cblrerr:
		CBLR_ERROR_MSG += "%s\n" % (str(cblrerr))
		log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, sensor['hostname']))
	except Exception as e:
		ERROR_MSG += "%s\n" % (str(e))
		log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), sensor['hostname']))
	
	return filename, OUTPUT_MSG, ERROR_MSG, CBLR_ERROR_MSG

def cbr_get_services(session, sensor, output_path):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	COMMAND_TO_RUN = "cmd.exe /C mode 800 & powershell.exe -command \"Get-WmiObject win32_service|Select-Object Name, DisplayName, StartName, PathName, ProcessId, ServiceType, Started, State, Description |ConvertTo-Csv -Delimiter '|' -NoTypeInformation\""
	filename=output_path+"\\"+sensor['hostname'] + "-Services.csv"
	try:
		out=session.create_process(COMMAND_TO_RUN, wait_timeout=10)
		sensor['output_content']=out
		OUTPUT_MSG = ("Successfully retrieved entries.")
		log.log(SUCCESS, "Successfully retrieved SERVICE entries \033[37mHOST:\033[32m %s", sensor['hostname'])
	except LiveResponseError as cblrerr:
		CBLR_ERROR_MSG += "%s\n" % (str(cblrerr))
		log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, sensor['hostname']))
	except Exception as e:
		ERROR_MSG += "%s\n" % (str(e))
		log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), sensor['hostname']))
	
	return filename, OUTPUT_MSG, ERROR_MSG, CBLR_ERROR_MSG

def cbr_delete_file(session, sensor, ioc_name_list):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	FOUND_FILE=0
	for index in range(0, len(ioc_name_list)):
		DIRECTORY = os.path.dirname(str(ioc_name_list[index]))
		FILENAME = os.path.basename(str(ioc_name_list[index]))
		try:
			session.delete_file(ioc_name_list[index])
			FOUND_FILE+=1
			OUTPUT_MSG+=str(ioc_name_list[index])+"\n"
			log.log(SUCCESS, "File was deleted \033[37mFILE:\033[32m %s \033[37mHOST:\033[32m %s" % ((ioc_name_list[index], sensor['hostname'])))
		except LiveResponseError as cblrerr:
			if "ERROR_PATH_NOT_FOUND" not in str(cblrerr) and "ERROR_FILE_NOT_FOUND" not in str(cblrerr):
				CBLR_ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(cblrerr)))
				log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mFILE:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, str(ioc_name_list[index]), sensor['hostname']))
		except Exception as e:
			ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(e)))
			log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mFILE:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), str(ioc_name_list[index]), sensor['hostname']))
	if FOUND_FILE == 0:
		OUTPUT_MSG = ("Given IOCs are not found.")

	return OUTPUT_MSG, FOUND_FILE, ERROR_MSG, CBLR_ERROR_MSG

def cbr_delete_task(session, sensor, ioc_name_list):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	FOUND_TASK=0
	for index in range(0 , len(ioc_name_list)):
		taskname = ioc_name_list[index]
		COMMAND_TO_RUN = "cmd.exe /C schtasks.exe /delete /TN \"%s\" /f" % taskname
		try:
			out=session.create_process(COMMAND_TO_RUN, wait_timeout=10)
			if "SUCCESS" in str(out):
				FOUND_TASK+=1
				OUTPUT_MSG +=str(taskname)+"\n"
				log.log(SUCCESS, "Task Entry was deleted \033[37mENTRY:\033[32m %s \033[37mHOST:\033[32m %s" % ((ioc_name_list[index], sensor['hostname'])))
			elif "ERROR:" in str(out) and "cannot find the file specified" not in str(out) and "does not exist in the system" not in str(out):
				ERROR_MSG=str(out)
				log.warn("An Error Occured Deleting a Task Entry \033[37mERROR:\033[33m %s \033[37mENTRY:\033[33m %s \033[37mHOST:\033[33m %s" % (ERROR_MSG, str(taskname), sensor['hostname']))
		except LiveResponseError as cblrerr:
			CBLR_ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(cblrerr)))
			log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mENTRY:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, str(taskname), sensor['hostname']))
		except Exception as e:
			ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(e)))
			log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mENTRY:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), str(taskname), sensor['hostname']))
	if FOUND_TASK == 0:
		OUTPUT_MSG = ("Given IOCs are not found.")

	return OUTPUT_MSG, FOUND_TASK, ERROR_MSG, CBLR_ERROR_MSG

def cbr_find_regkey(session, sensor, ioc_name_list):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	FOUND_REGKEY=0
	for index in range(0, len(ioc_name_list)):
		regkey = ioc_name_list[index]
		try:
			keys=session.get_registry_value(regkey)
			FOUND_REGKEY+=1
			OUTPUT_MSG +=str(regkey)+"\n"
			log.log(SUCCESS, "Registry Key was found \033[37mREGKEY:\033[32m %s \033[37mHOST:\033[32m %s" % ((ioc_name_list[index], sensor['hostname'])))
		except LiveResponseError as cblrerr:
			if "ERROR_FILE_NOT_FOUND" not in str(cblrerr):
				CBLR_ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(cblrerr)))
				log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mREGKEY:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, str(regkey), sensor['hostname']))
		except Exception as e:
			ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(e)))
			log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mREGKEY:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), str(regkey), sensor['hostname']))
	if FOUND_REGKEY == 0:
		OUTPUT_MSG = ("Given IOCs are not found.")
	
	return OUTPUT_MSG, FOUND_REGKEY, ERROR_MSG, CBLR_ERROR_MSG

def cbr_delete_regkey(session, sensor, ioc_name_list):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	FOUND_REGKEY=0
	for index in range(0, len(ioc_name_list)):
		regkey = ioc_name_list[index]
		try:
			keys=session.delete_registry_value(str(regkey))
			FOUND_REGKEY+=1
			OUTPUT_MSG +=str(regkey)+"\n"
			log.log(SUCCESS, "Registry Key was deleted \033[37mREGKEY:\033[32m %s \033[37mHOST:\033[32m %s" % ((ioc_name_list[index], sensor['hostname'])))
		except LiveResponseError as cblrerr:
			if "ERROR_FILE_NOT_FOUND" not in str(cblrerr):
				CBLR_ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(cblrerr)))
				log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mREGKEY:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, str(regkey), sensor['hostname']))
		except Exception as e:
			ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(e)))
			log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mREGKEY:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), str(regkey), sensor['hostname']))
	if FOUND_REGKEY == 0:
		OUTPUT_MSG = ("Given IOCs are not found.")

	return OUTPUT_MSG, FOUND_REGKEY, ERROR_MSG, CBLR_ERROR_MSG

def cbr_delete_service(session,sensor,ioc_name_list):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	FOUND_SERVICE=0
	for index in range(0 , len(ioc_name_list)):
		servicename = ioc_name_list[index]
		COMMAND_TO_RUN = "cmd.exe /C sc.exe stop \"%s\" & sc.exe delete \"%s\"" % (str(servicename),str(servicename))
		try:
			out=session.create_process(COMMAND_TO_RUN, wait_timeout=10)
			if "SUCCESS" in str(out) and "DeleteService" in str(out):
				FOUND_SERVICE+=1
				OUTPUT_MSG +=str(servicename)+"\n"
				log.log(SUCCESS, "Service Entry was deleted \033[37mENTRY:\033[32m %s \033[37mHOST:\033[32m %s" % ((ioc_name_list[index], sensor['hostname'])))
			elif "FAILED" in str(out) and "FAILED 1060" not in str(out):
				ERROR_MSG+="%s: %s\n" % (ioc_name_list[index], str(out))
				log.warn("An Error Occured Deleting a Service Entry \033[37mERROR:\033[33m %s \033[37mENTRY:\033[33m %s \033[37mHOST:\033[33m %s" % (str(out), str(servicename), sensor['hostname']))
		except LiveResponseError as cblrerr:
			CBLR_ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(cblrerr)))
			log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mENTRY:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, str(servicename), sensor['hostname']))
		except Exception as e:
			ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(e)))
			log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mENTRY:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), str(servicename), sensor['hostname']))
	if FOUND_SERVICE == 0:
		OUTPUT_MSG = ("Given IOCs are not found.")

	return OUTPUT_MSG, FOUND_SERVICE, ERROR_MSG, CBLR_ERROR_MSG

def cbr_kill_process(session,sensor,ioc_name_list):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	FOUND_PROCESS=0
	for index in range(0, len(ioc_name_list)):
		pid = ioc_name_list[index]
		try:
			if session.kill_process(pid):
				FOUND_PROCESS+=1
				OUTPUT_MSG+=str(pid)+"\n"
				log.log(SUCCESS, "A Process was killed \033[37mPID:\033[32m %s \033[37mHOST:\033[32m %s" % ((ioc_name_list[index], sensor['hostname'])))
			else:
				OUTPUT_MSG+="Could not kill:"+str(pid)+"\n"
				log.warn("An Error Occured Killing a Process \033[37mPID:\033[33m %s \033[37mHOST:\033[33m %s" % (str(pid), sensor['hostname']))
		except LiveResponseError as cblrerr:
			if "ERROR_INVALID_PARAMETER" not in str(cblrerr):
				CBLR_ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(cblrerr)))
				log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mPID:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, str(pid), sensor['hostname']))
		except Exception as e:
			ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(e)))
			log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mPID:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), str(pid), sensor['hostname']))
	if FOUND_PROCESS == 0:
		OUTPUT_MSG = ("Given IOCs are not found.")

	return OUTPUT_MSG, FOUND_PROCESS, ERROR_MSG, CBLR_ERROR_MSG

def cbr_execute_command(session, sensor, command):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	try:
		out=session.create_process("{0}".format(command), wait_timeout=10)
		log.info("Command Sent \033[37mCOMMAND:\033[32m %s \033[37mHOST:\033[32m %s" % ((str(command), sensor['hostname'])))
	except LiveResponseError as cblrerr:
		CBLR_ERROR_MSG += "%s: %s\n" % (str(command), (str(cblrerr)))
		log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mCOMMAND:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, str(command), sensor['hostname']))
	except Exception as e:
		ERROR_MSG += "%s: %s\n" % (str(command), (str(e)))

	return OUTPUT_MSG, ERROR_MSG, CBLR_ERROR_MSG

def cbr_get_file(session,sensor,ioc_name_list, output_path):
	OUTPUT_MSG=""
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	FOUND_FILE=0
	for index in range(0, len(ioc_name_list)):
		DIRECTORY = os.path.dirname(str(ioc_name_list[index]))
		FILENAME = os.path.basename(str(ioc_name_list[index]))
		try:
			directory=session.list_directory(DIRECTORY+"\\")
			for file in directory:
				if file['filename'] == FILENAME:
					FOUND_FILE+=1
					if 'DIRECTORY' in file['attributes']:
						log.warn("File is a directory \033[37mFILE:\033[33m %s \033[37mHOST:\033[33m %s" % (str(ioc_name_list[index]), sensor['hostname']))
						OUTPUT_MSG += "File is a directory\n"
						pass
					else:
						log.info("File was found \033[37mFILE:\033[36m %s \033[37mSIZE:\033[36m %s bytes \033[37mHOST:\033[36m %s" % (ioc_name_list[index], str(file['size']), sensor['hostname']))
						if file['size'] > 100000000:#100MB
							log.warn("File is too big \033[37mFILE:\033[33m %s \033[37mSIZE:\033[33m %s bytes \033[37mHOST:\033[33m %s" % (str(ioc_name_list[index]),str(file['size']), sensor['hostname']))
							pass
						else:
							output_filename = "%s\\%s\\%s" % (output_path, sensor['hostname'],file['filename'])
							try:
								out = session.get_file(str(ioc_name_list[index]))
								if createOutputPath("%s\\%s" %(output_path,sensor['hostname'])) == False:
									log.warn("Directory Could not be created \033[37mDIRECTORY:\033[33m %s\\%s" % (output_path, sensor['hostname']))
									pass
								OUT_FILE = createSensorLogFile(output_filename)
								if OUT_FILE == None:
									log.warn("File Could not be created \033[37mFILE:\033[33m %s" % (output_filename))
									pass
								else:
									OUT_FILE.write(out)
									log.log(SUCCESS, "File is downloaded \033[37mFILE:\033[32m %s \033[37mHOST:\033[32m %s" % ((output_filename, sensor['hostname'])))
									OUTPUT_MSG += str(ioc_name_list[index])+"\n"
									OUT_FILE.close()
							except LiveResponseError as cblrerr:
								CBLR_ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(cblrerr)))
								log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mFILE:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, str(ioc_name_list[index]), sensor['hostname']))
							except Exception as e:
								ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(e)))
								log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mFILE:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), str(ioc_name_list[index]), sensor['hostname']))
		except LiveResponseError as cblrerr:
			if "ERROR_PATH_NOT_FOUND" not in str(cblrerr):
				CBLR_ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(cblrerr)))
				log.warn("Live Response Error Occured \033[37mERROR:\033[33m %s \033[37mFILE:\033[33m %s \033[37mHOST:\033[33m %s" % (cblrerr, str(ioc_name_list[index]), sensor['hostname']))
		except Exception as e:
			ERROR_MSG += "%s: %s\n" % (ioc_name_list[index], (str(e)))
			log.warn("Exception occured \033[37mERROR:\033[33m %s \033[37mFILE:\033[33m %s \033[37mHOST:\033[33m %s" % (str(e), str(ioc_name_list[index]), sensor['hostname']))
	if FOUND_FILE == 0:
		OUTPUT_MSG = ("Given IOCs are not found.")

	return OUTPUT_MSG, FOUND_FILE, ERROR_MSG, CBLR_ERROR_MSG 
