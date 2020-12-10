from cb_utils import *
import time

logo_raw="""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!$$$$$$$#!!!!!!!!!! !!!!!!!!!!!!!!!!!#####!##!##!######!#####!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!$$$$$$$#!!!!!!!!!!!! !!!!!!!!!!!!!!!!!##!##!##!##!!!##!!!##!##!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!$$$$$$#!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!#####!##!##!!!##!!!##!##!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!$$$$$$#!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!##!##!##!##!!!##!!!##!##!!!!!!!!!!!!!!!!!!!
!!!!!!!!!$$$$$$$$$$$$#!!!!!!!!!! !!!!!!!!!!!!!!!!!##!##!#####!!!##!!!#####!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!$$$$$$#!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!$$$$$$#!!!!!!!!!!!!! !!!!!#####!####!####!#####!#####!#####!####!!####!#####!!!!!
!!!!!!!!!!!$$$$$$#!!!!!!!!!!!!!! !!!!!##!##!##!!!##!!!##!##!##!##!##!##!##!##!##!!!##!##!!!!!
!!!!!!!!!!$$$$$$#!!!!!!!!!!!!!!! !!!!!####!!####!####!#####!##!##!##!##!##!##!####!####!!!!!!
!!!!!!!!!$$$$$$$$$$#!!!!!!!!!!!! !!!!!##!##!##!!!!!##!##!!!!##!##!##!##!##!##!##!!!##!##!!!!!
!!!!!!!!!!!!!!$$$#!!!!!!!!!!!!!! !!!!!##!##!####!####!##!!!!#####!##!##!####!!####!##!##!!!!!
!!!!!!!!!!!!!$$$#!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!$$#!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!\033[2m\033[47m\033[30mCarbon Black Response IR tool!!!!!!!!!!!!!!!!
!!!!!!!!!!!$$#!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!\033[2m\033[47m\033[30mADEO DFIR!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!$$#!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!\033[2m\033[47m\033[30m@rsh1r1nov!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!$#!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
@click.group()
def main():
	logo_formatted = logo_raw.replace("#", "\033[40m\033[30m \033[0m").replace("!", "\033[1m\033[47m \033[0m").replace("$", "\033[44m\033[34m \033[0m")
	print(logo_formatted)
#########################################################################################################################################################################################################
###########################For Finding Specific Registry Values###########################
@main.command()
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--regkeys", required=True, help='Text file containing registry keys')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def find_regkey(logfile, hosts, regkeys, workers):
	start_time = time.time()
	CBRAPI = connect_to_cb_server()
	INVALID_IOC_LIST=[]
	IOCFILENAME_LIST = read_file(regkeys)
	if len(IOCFILENAME_LIST) == 0:
		log.error("Exiting!")
		sys.exit(0)
	else:
		INVALID_IOC_LIST = getFaultyEntries(IOCFILENAME_LIST, "REGKEY")
		if len(INVALID_IOC_LIST) > 0:		
			log.error("There are invalid registry key values on rows: %s" % ','.join(str(index) for index in INVALID_IOC_LIST))
			sys.exit(0)
	#invoke_function(function, module, command, hosts, logfile, output_path, workers, regkeys)
	invoke_function(CBRAPI, invoke_cbr, GET_REGKEY, hosts, logfile, 0, workers, IOCFILENAME_LIST, "")
#############################################################################################################################################################################################
###########################For Deleting Specific Registry Values###########################
@main.command()
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--regkeys", required=True, help='Text file containing registry keys')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def delete_regkey(logfile, hosts, regkeys, workers):
	CBRAPI = connect_to_cb_server()
	INVALID_IOC_LIST=[]
	IOCFILENAME_LIST = read_file(regkeys)
	if len(IOCFILENAME_LIST) == 0:
		log.error("Exiting!")
		sys.exit(0)
	else:
		INVALID_IOC_LIST = getFaultyEntries(IOCFILENAME_LIST, "REGKEY")
		if len(INVALID_IOC_LIST) > 0:		
			log.error("There are invalid registry key values on rows: %s" % ','.join(str(index) for index in INVALID_IOC_LIST))
			sys.exit(0)
	invoke_function(CBRAPI, invoke_cbr, DELETE_REGKEY, hosts, logfile, 0, workers, IOCFILENAME_LIST, "")
#############################################################################################################################################################################################
###########################For Finding Specific Filenames###########################
@main.command()
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--files", required=True, help='Text file containing filenames')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def find_file(logfile, hosts, files, workers):
	CBRAPI = connect_to_cb_server()
	INVALID_IOC_LIST=[]
	IOCFILENAME_LIST = read_file(files)
	if len(IOCFILENAME_LIST) == 0:
		log.error("Exiting!")
		sys.exit(0)
	else:
		INVALID_IOC_LIST = getFaultyEntries(IOCFILENAME_LIST, "FILE")
		if len(INVALID_IOC_LIST) > 0:		
			log.error("There are invalid filename entries on rows: %s" % ','.join(str(index) for index in INVALID_IOC_LIST))
			sys.exit(0)
	invoke_function(CBRAPI, invoke_cbr, FIND_FILE, hosts, logfile, 0, workers, IOCFILENAME_LIST, "")
#############################################################################################################################################################################################
###########################For Downloading Specific Files from Sensors###########################
@main.command()
@click.option("--output_path", required=True, help='Output path for the files that\'ll be downlaoded from sensors')
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--files", required=True, help='Text file containing filenames')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def get_file(logfile, hosts, files, workers, output_path):
	CBRAPI = connect_to_cb_server()
	INVALID_IOC_LIST=[]
	IOCFILENAME_LIST = read_file(files)
	if len(IOCFILENAME_LIST) == 0:
		log.error("Exiting!")
		sys.exit(0)
	else:
		INVALID_IOC_LIST = getFaultyEntries(IOCFILENAME_LIST, "FILE")
		if len(INVALID_IOC_LIST) > 0:		
			log.error("There are invalid filename entries on rows: %s" % ','.join(str(index) for index in INVALID_IOC_LIST))
			sys.exit(0)
	invoke_function(CBRAPI, invoke_cbr, GET_FILE, hosts, logfile, output_path, workers, IOCFILENAME_LIST, "")
#############################################################################################################################################################################################
###########################For Deleting Specific Files from Sensors###########################
@main.command()
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--files", required=True, help='Text file containing filenames')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def delete_file(logfile, hosts, files, workers):
	CBRAPI = connect_to_cb_server()
	INVALID_IOC_LIST=[]
	IOCFILENAME_LIST = read_file(files)
	if len(IOCFILENAME_LIST) == 0:
		log.error("Exiting!")
		sys.exit(0)
	else:
		INVALID_IOC_LIST = getFaultyEntries(IOCFILENAME_LIST, "FILE")
		if len(INVALID_IOC_LIST) > 0:		
			log.error("There are invalid filename entries on rows: %s" % ','.join(str(index) for index in INVALID_IOC_LIST))
			sys.exit(0)
	invoke_function(CBRAPI, invoke_cbr, DELETE_FILE, hosts, logfile, 0, workers, IOCFILENAME_LIST, "")
#############################################################################################################################################################################################
###########################For Downloading Scheduled Task Entries###########################
@main.command()
@click.option("--output_path", required=True, help='Output path for the files containing scheduled task entries')
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def get_tasks(output_path, hosts, logfile, workers):
	CBRAPI = connect_to_cb_server()
	#invoke_function(function, module, command, hosts, logfile, output_path, workers, iocs)
	invoke_function(CBRAPI, invoke_cbr, GET_TASKS, hosts, logfile, output_path, workers, 0, "")
#############################################################################################################################################################################################
###########################For Deleting Scheduled Task Entries###########################
@main.command()
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--tasks", required=True, help='Text file containing task names')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def delete_tasks(logfile, hosts, tasks, workers):
	CBRAPI = connect_to_cb_server()
	INVALID_IOC_LIST=[]
	IOCFILENAME_LIST = read_file(tasks)
	if len(IOCFILENAME_LIST) == 0:
		log.error("Exiting!")
		sys.exit(0)
	else:
		INVALID_IOC_LIST = getFaultyEntries(IOCFILENAME_LIST, "TASK")
		if len(INVALID_IOC_LIST) > 0:		
			log.error("There are invalid task entries on rows: %s" % ','.join(str(index) for index in INVALID_IOC_LIST))
			sys.exit(0)
	invoke_function(CBRAPI, invoke_cbr, DELETE_TASKS, hosts, logfile, 0, workers, IOCFILENAME_LIST, "")
#############################################################################################################################################################################################
###########################For Downloading WMI Entries###########################
@main.command()
@click.option("--output_path", required=True, help='Output path for the files containing WMI subscription entries')
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def get_wmi_entries(output_path, hosts, logfile, workers):
	CBRAPI = connect_to_cb_server()
	#invoke_function(function, module, command, hosts, logfile, output_path, workers, iocs)
	invoke_function(CBRAPI, invoke_cbr, GET_WMI_PERSISTENCE, hosts, logfile, output_path, workers, 0, "")
#############################################################################################################################################################################################
###########################For Downloading Service Entries###########################
@main.command()
@click.option("--output_path", required=True, help='Output path for the files containing service entries')
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def get_services(output_path, hosts, logfile, workers):
	CBRAPI = connect_to_cb_server()
	#invoke_function(function, module, command, hosts, logfile, output_path, workers, iocs)
	invoke_function(CBRAPI, invoke_cbr, GET_SERVICES, hosts, logfile, output_path, workers, 0, "")
#############################################################################################################################################################################################
###########################For Fetching Guest Account Statuses###########################
@main.command()
@click.option("--output_path", required=True, help='Output path for the files containing guest account statutes')
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def get_guest_status(output_path, hosts, logfile, workers):
	CBRAPI = connect_to_cb_server()
	#invoke_function(function, module, command, hosts, logfile, output_path, workers, iocs)
	invoke_function(CBRAPI, invoke_cbr, GET_GUEST_STATUS, hosts, logfile, output_path, workers, 0, "")
#############################################################################################################################################################################################
###########################For Deleting Service Entries from Sensors###########################
@main.command()
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--services", required=True, help='Text file containing service names')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def delete_services(logfile, hosts, services, workers):
	CBRAPI = connect_to_cb_server()
	INVALID_IOC_LIST=[]
	IOCFILENAME_LIST = read_file(services)
	if len(IOCFILENAME_LIST) == 0:
		log.error("Exiting!")
		sys.exit(0)
	else:
		INVALID_IOC_LIST = getFaultyEntries(IOCFILENAME_LIST, "SERVICE")
		if len(INVALID_IOC_LIST) > 0:		
			log.error("There are invalid service entries on rows: %s" % ','.join(str(index) for index in INVALID_IOC_LIST))
			sys.exit(0)
	invoke_function(CBRAPI, invoke_cbr, DELETE_SERVICES, hosts, logfile, 0, workers, IOCFILENAME_LIST, "")
#############################################################################################################################################################################################
###########################For Killing Running Processes###########################
@main.command()
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--pids", required=True, help='Text file containing process pids')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def kill_process(logfile, hosts, pids, workers):
	CBRAPI = connect_to_cb_server()
	INVALID_IOC_LIST=[]
	IOCFILENAME_LIST = read_file(pids)
	if len(IOCFILENAME_LIST) == 0:
		log.error("Exiting!")
		sys.exit(0)
	else:
		INVALID_IOC_LIST = getFaultyEntries(IOCFILENAME_LIST, "PID")
		if len(INVALID_IOC_LIST) > 0:		
			log.error("There are invalid process id entries on rows: %s" % ','.join(str(index) for index in INVALID_IOC_LIST))
			sys.exit(0)
	invoke_function(CBRAPI, invoke_cbr, KILL_PROCESS, hosts, logfile, 0, workers, IOCFILENAME_LIST, "")
#############################################################################################################################################################################################
###########################For Exporting The Sensor list###########################
@main.command()
@click.option("--export_file", required=True, help='Export file for the sensors')
def export_sensors(export_file):
	CBRAPI = connect_to_cb_server()
	try:
		sensors=list(CBRAPI.select(Sensor))
		try:
			if createOutputPath(os.path.dirname(str(export_file))) == False:
				log.error("Exiting!")
				sys.exit(0)
			else:
				EXPORT_FILE = createLogFile(export_file)
				if EXPORT_FILE == None:
					log.error("Exiting!")
					sys.exit(0)
			csvwriter = csv.writer(EXPORT_FILE)
			csvwriter.writerow(["ID","GROUP NAME","HOSTNAME","STATUS","POWER STATE","NETWOR INTERFACES","OS ENVIRONMENT","BUILD VERSION","ISOLATED","LAST CHECKIN TIME","REGISTRATION TIME",])
			for sensor in sensors:
				Power_state_str = "Unknown"
				Group_Name = "Unknown"
				if sensor.power_state == 0 : Power_state_str = "Running"
				elif sensor.power_state == 1 : Power_state_str = "Suspended"
				elif sensor.power_state == 2 : Power_state_str = "Shutdown"
				else: Power_state_str = "Unknown"
				Group_Name=get_group_by_id(CBRAPI, sensor.group_id)
				csvwriter.writerow([str(sensor.id),str(Group_Name), str(sensor.hostname), str(sensor.status),Power_state_str,"\n".join([str(prop.macaddr)+" -> "+str(prop.ipaddr) for prop in sensor.network_interfaces]), str(sensor.os_environment_display_string).replace(',', ''), str(sensor.build_version_string), str(sensor.network_isolation_enabled), str(sensor.last_checkin_time.strftime("%d/%m/%y %H:%M:%S")),str(sensor.registration_time.strftime("%d/%m/%y %H:%M:%S")),])
			log.log(SUCCESS, "Successfully exported sensor list.")
			EXPORT_FILE.close()
		except Exception as e:
			log.error("Exception Occured: "+str(e))
			sys.exit(0)
	except Exception as e:
		log.error("Exception Occured: "+str(e))
		sys.exit(0)
#############################################################################################################################################################################################
###########################For Executing Commands on Sensors###########################
@main.command()
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--command", required=True, help='The command to execute')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def execute_cmd(logfile, hosts, command, workers):
	CBRAPI = connect_to_cb_server()
	invoke_function(CBRAPI, invoke_cbr, EXECUTE_CMD, hosts, logfile, 0, workers, 0, command)
#############################################################################################################################################################################################

###########################For Isolating Sensors###########################
@main.command()
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def isolate(logfile, hosts, workers):
	CBRAPI = connect_to_cb_server()
	invoke_function(CBRAPI, invoke_cbr, ISOLATE_SENSORS, hosts, logfile, 0, workers, 0, "")
#############################################################################################################################################################################################
###########################For Removing Sensors From Isolation###########################
@main.command()
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def unisolate(logfile, hosts, workers):
	CBRAPI = connect_to_cb_server()
	invoke_function(CBRAPI, invoke_cbr, UNISOLATE_SENSORS, hosts, logfile, 0, workers, 0, "")
#############################################################################################################################################################################################
###########################For Restarting Sensors###########################
@main.command()
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def restart_sensors(logfile, hosts, workers):
	CBRAPI = connect_to_cb_server()
	invoke_function(CBRAPI, invoke_cbr, RESTART_SENSORS, hosts, logfile, 0, workers, 0, "")
#############################################################################################################################################################################################
###########################For Restarting Endpoints###########################
@main.command()
@click.option("--logfile", required=True, help='CSV file for the output')
@click.option("--hosts", required=True, help='Text file containing sensor hostnames')
@click.option("--workers", default=4, required=True, help='Threads to initiate (Should not be more than the CBLRMaxSession count)')
def restart_endpoints(logfile, hosts, workers):
	CBRAPI = connect_to_cb_server()
	invoke_function(CBRAPI, invoke_cbr, RESTART_ENDPOINTS, hosts, logfile, 0, workers, 0, "")
#############################################################################################################################################################################################
##########################For searching for MD5/SHA256 hash values###################################################
@main.command()
@click.option("--logfile", required=True,help = 'CSV file for the output')
@click.option("--hashes",required=True,help ='Text file containing hashes')
def find_hash(logfile, hashes):
	CBRAPI = connect_to_cb_server()
	INVALID_IOC_LIST=[]
	IOCHASH_LIST = read_file(hashes)
	md5hash_list = []
	sha256hash_list = []
	binary_list = []
	if len(IOCHASH_LIST) == 0:
		log.error("Exiting!")
		sys.exit(0)
	
	INVALID_HASH_LIST = getFaultyEntries(IOCHASH_LIST, "HASH")
	if len(INVALID_HASH_LIST) > 0:		
		log.error("There are invalid hash entries on rows: %s" % ','.join(str(index) for index in INVALID_HASH_LIST))
		sys.exit(0)
	if createOutputPath(os.path.dirname(str(logfile))) == False:
		log.error("Exiting!")
		sys.exit(0)
	else:
		LOGFILE = createLogFile(logfile)
		if LOGFILE == None:
			log.error("Exiting!")
			sys.exit(0)
	CSV_WRITER = csv.writer(LOGFILE)
	CSV_WRITER.writerow(["HASH", "FILENAME", "DESCRIPTION", "COMPANY NAME", "SIGNED", "FOUND ON ENDPOINT", "ENDPOINTS"])

	for hash in IOCHASH_LIST:
		query=""
		if len(hash) == 32:
			query="md5:"
		else:
			query="sha256:"
		query+=str(hash)
		binary = (CBRAPI.select(Binary).where(query).first())
		if binary != None:
			log.log(SUCCESS, "Hash is Found \033[37mHASH:\033[32m %s \033[37mFILE:\033[32m %s \033[37mDESCRIPTION:\033[32m %s \033[37mSIGNED:\033[32m %s \033[37mFOUND ON ENDPOINT:\033[32m %s" % ((hash, binary.original_filename, binary.file_desc, binary.signed, len(binary.endpoint))))
			endpoint_list = [ e.split('|')[0] for e in binary.endpoint]
			CSV_WRITER.writerow([hash, str(binary.original_filename), str(binary.file_desc), binary.company_name, str(binary.signed), len(binary.endpoint), "\n".join(endpoint_list)])

	LOGFILE.close()
#############################################################################################################################################################################################
###########################For Restarting Sensors###########################
@main.command()
@click.option("--hostname", required=True, help='On a single CBR environment please provide the Master CBR server\'s address\nOn a clustered environment please provide the address of the Minion CBR server that you\'d like to scan')
@click.option("--thor-dir", required=True, help='Remote THOR directory on the CBR server')
@click.option("--username", required=True, help='SSH username for the CBR server')
#@click.option("--password", required=True, help='SSH password for the CBR server')
@click.option("--port", default=22, required=True, help='SSH password for the CBR server')
def run_thor(hostname, thor_dir, username, port):
	CBRAPI = connect_to_cb_server()
	cbr_run_thor(CBRAPI, hostname, thor_dir, username, port)
#############################################################################################################################################################################################
if __name__ == '__main__':
	main()
