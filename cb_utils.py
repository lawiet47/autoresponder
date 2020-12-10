from live_response_utils import *
import paramiko
import getpass
#####Method Constants######
GET_TASKS = 0
GET_WMI_PERSISTENCE = 1
GET_SERVICES = 2
GET_FILE = 3
FIND_FILE = 4
DELETE_FILE = 5
GET_REGKEY = 6
DELETE_REGKEY = 7
DELETE_TASKS = 8
DELETE_SERVICES = 9
KILL_PROCESS = 10
EXPORT_SENSORS = 11
ISOLATE_SENSORS = 12
UNISOLATE_SENSORS = 13
RESTART_SENSORS = 14
RESTART_ENDPOINTS = 15
EXECUTE_CMD = 16
GET_GUEST_STATUS = 17

def connect_to_cb_server():
	log.info("Trying to connect to Carbon Black Response Server")
	CBRAPI = None
	try:
		CBRAPI=CbResponseAPI()
		log.log(SUCCESS, "Connected to %s" % CBRAPI.credentials['url'])
		log.info("Carbon Black Response Server version: %s" % CBRAPI.info()['version'])
		if CBRAPI.info()['cblrEnabled'] is False:
			log.error("Live Response is not Enabled on this server")
			sys.exit(0)
		else:
			log.info("Live Response is enabled")
	except Exception as e:
		log.error("Could not Initialize CBAPI: "+str(e))
		sys.exit(0)
	except KeyboardInterrupt:
		log.error("User Interrupted session")
		sys.exit(0)
	return CBRAPI

def get_group_by_id(CBRAPI, id):
	query = "id:"+str(id)
	group = CBRAPI.select(SensorGroup).where(query).first()
	if group is None:
		return "Unknown"
	return group.name


def get_online_sensors(CBRAPI, hostname_list):
	ONLINE_SENSOR_LIST=[]
	INVALID_HOSTNAME_LIST=[]
	OFFLINE_SENSOR_LIST=[]
	UNINSTALLED_SENSOR_LIST=[]
	for hostname in hostname_list:
		query='hostname:'+str(hostname)
		try:
			sensor=CBRAPI.select(Sensor).where(query).first()
			if sensor is not None :
				if "Online" in sensor.status:
					ONLINE_SENSOR_LIST.append(sensor.hostname)
				elif "Offline" in sensor.status:
					OFFLINE_SENSOR_LIST.append(sensor.hostname)
				elif "uninstall" in str(sensor.status).lower():
					UNINSTALLED_SENSOR_LIST.append(sensor.hostname)
			else:
				INVALID_HOSTNAME_LIST.append(hostname)
		except Exception as e:
			log.error("CBAPI Error occured: "+str(e))
	return ONLINE_SENSOR_LIST, OFFLINE_SENSOR_LIST, INVALID_HOSTNAME_LIST, UNINSTALLED_SENSOR_LIST

def invoke_cbr(CBRAPI, hostname, module, ioc_name_list, output_path, command):
	ERROR_MSG=""
	CBLR_ERROR_MSG=""
	OUTPUT_MSG=""
	STATE="Unknown"
	CURRENT_SENSOR={}
	filename=""
	query='hostname:'+hostname
	try:
		sensor = None
		sensorquery=CBRAPI.select(Sensor).where(query).all()
		for x in sensorquery:
			if x.hostname == hostname:
				sensor = x
		if sensor is None:
			OUTPUT_MSG=""
			ERROR_MSG="No Such Host"
			log.warn("Invalid Hostname \033[37mHOST:\033[33m %s" % (hostname))
			CURRENT_SENSOR['hostname'] = hostname
			CURRENT_SENSOR['os'] = "Invalid"
			CURRENT_SENSOR['output_content'] = ""
		else:
			CURRENT_SENSOR['hostname'] = sensor.hostname
			CURRENT_SENSOR['os'] = sensor.os
			CURRENT_SENSOR['output_content'] = ""
			if "Off" in sensor.status:
				STATE="Offline"
				OUTPUT_MSG=""
				ERROR_MSG=""
				CURRENT_SENSOR['output_content'] = ""
			elif "uninstall" in str(sensor.status).lower():
				STATE="Uninstall Pending"
				OUTPUT_MSG=""
				ERROR_MSG=""
				CURRENT_SENSOR['output_content'] = ""
			else:
				STATE="Online"
				try:
					with sensor.lr_session() as session:
						if module == FIND_FILE:
							
							OUTPUT_MSG, FOUND_FILE, ERROR_MSG, CBLR_ERROR_MSG = cbr_find_file(session, CURRENT_SENSOR, ioc_name_list)
						elif module == GET_TASKS:
							
							filename, OUTPUT_MSG, ERROR_MSG, CBLR_ERROR_MSG = cbr_get_tasks(session, CURRENT_SENSOR, output_path)
						elif module == GET_WMI_PERSISTENCE:
							
							filename, OUTPUT_MSG, ERROR_MSG, CBLR_ERROR_MSG = cbr_get_wmi_persistence(session, CURRENT_SENSOR, output_path)
						elif module == GET_SERVICES:
						
							filename, OUTPUT_MSG, ERROR_MSG, CBLR_ERROR_MSG = cbr_get_services(session, CURRENT_SENSOR, output_path)

						elif module == GET_GUEST_STATUS:
							filename, OUTPUT_MSG, ERROR_MSG, CBLR_ERROR_MSG = cbr_get_guest_status(session, CURRENT_SENSOR, output_path)
							
						elif module == DELETE_FILE:

							OUTPUT_MSG, FOUND_FILE, ERROR_MSG, CBLR_ERROR_MSG = cbr_delete_file(session, CURRENT_SENSOR, ioc_name_list)
						elif module == DELETE_TASKS:

							OUTPUT_MSG, FOUND_TASK, ERROR_MSG, CBLR_ERROR_MSG = cbr_delete_task(session, CURRENT_SENSOR, ioc_name_list)
						elif module == GET_REGKEY:

							OUTPUT_MSG, FOUND_REGKEY, ERROR_MSG, CBLR_ERROR_MSG = cbr_find_regkey(session, CURRENT_SENSOR, ioc_name_list)
						elif module == DELETE_REGKEY:

							OUTPUT_MSG, FOUND_REGKEY, ERROR_MSG, CBLR_ERROR_MSG = cbr_delete_regkey(session, CURRENT_SENSOR, ioc_name_list)
						elif module == DELETE_SERVICES:

							OUTPUT_MSG, FOUND_SERVICE, ERROR_MSG, CBLR_ERROR_MSG = cbr_delete_service(session, CURRENT_SENSOR, ioc_name_list)
						elif module == KILL_PROCESS:

							OUTPUT_MSG, FOUND_PROCESS, ERROR_MSG, CBLR_ERROR_MSG = cbr_kill_process(session, CURRENT_SENSOR, ioc_name_list)
						elif module == GET_FILE:

							OUTPUT_MSG, FOUND_FILE, ERROR_MSG, CBLR_ERROR_MSG = cbr_get_file(session, CURRENT_SENSOR, ioc_name_list, output_path)

						elif module == EXECUTE_CMD:

							OUTPUT_MSG, ERROR_MSG, CBLR_ERROR_MSG = cbr_execute_command(session, CURRENT_SENSOR, command)
						elif module == RESTART_ENDPOINTS:

							OUTPUT_MSG, ERROR_MSG, CBLR_ERROR_MSG = cbr_restart_endpoints(session, CURRENT_SENSOR)
						elif module == ISOLATE_SENSORS:

							if sensor.network_isolation_enabled == True:
								log.warn("The host is already isolated \033[37mHOST:\033[33m %s" % CURRENT_SENSOR['hostname'])
								OUTPUT_MSG += "The host is already Isolated\n"
								pass
							else:
								try:
									sensor.network_isolation_enabled = True
									sensor.save()
									log.log(SUCCESS, "Isolation complete \033[37mHOST:\033[32m %s" % CURRENT_SENSOR['hostname'])
									OUTPUT_MSG += "Isolation complete\n"
								except Exception as e:
									log.warn("Could not isolate host \033[37mHOST:\033[33m %s" % CURRENT_SENSOR['hostname'])
									ERROR_MSG += str(e)+"\n"
						elif module == UNISOLATE_SENSORS:

							if sensor.network_isolation_enabled == False:
								log.warn("The host is already in unisolated state \033[37mHOST:\033[33m %s" % CURRENT_SENSOR['hostname'])
								OUTPUT_MSG += "The host is already in unisolated state\n"
								pass
							else:
								try:
									sensor.network_isolation_enabled = False
									sensor.save()
									log.log(SUCCESS, "Removed from isolation \033[37mHOST:\033[32m %s" % CURRENT_SENSOR['hostname'])
									OUTPUT_MSG += "Removed from isolation\n"
								except Exception as e:
									log.warn("Could not remove host from isolation \033[37mHOST:\033[33m %s" % CURRENT_SENSOR['hostname'])
									ERROR_MSG += str(e)+"\n"
						elif module == RESTART_SENSORS:
							try:
								sensor.restart_sensor()
								log.info("A sensor restart was issued for the host \033[37mHOST:\033[36m %s" % CURRENT_SENSOR['hostname'])
								OUTPUT_MSG += "A sensor restart was issued for the host\n"
							except Exception as e:
								log.warn("Could not restart the sensor \033[37mHOST:\033[33m %s" % CURRENT_SENSOR['hostname'])
								ERROR_MSG += str(e)+"\n"

				except Exception as e:
					log.warn("Error Occured while connecting to a sensor \033[37mERROR:\033[33m %s \033[37mHOST:\033[33m %s" %(str(e), CURRENT_SENSOR['hostname']))
			if len(CURRENT_SENSOR['output_content']) > 0:
				SENSOR_LOGFILE = createSensorLogFile(filename)
				if SENSOR_LOGFILE == None:
					log.warn("Error Occured while writing to output_path \033[37mERROR:\033[33m %s \033[37mFILE:\033[33m %s \033[37mHOST:\033[33m %s" %(str(e), filename, CURRENT_SENSOR['hostname']))
				else:
					SENSOR_LOGFILE.write(CURRENT_SENSOR['output_content'])
	except Exception as e:
		log.warn("Error Occured while establishing connection with CBR server \033[37mERROR:\033[33m %s \033[37mHOST:\033[33m %s" %(str(e), hostname))
	return CURRENT_SENSOR, STATE, OUTPUT_MSG, ERROR_MSG, CBLR_ERROR_MSG

def invoke_function(CBRAPI, function, module, hosts, logfile, output_path, workers, iocs, command):
	SENSOR_LIST = read_file(hosts)
	LOGFILE = 0
	CSV_WRITER = 0
	INVALID_HOSTNAME_INDEXLIST = []
	if len(SENSOR_LIST) == 0:
		log.error("Exiting!")
		sys.exit(0)
	else:
		INVALID_HOSTNAME_INDEXLIST = getFaultyEntries(SENSOR_LIST, "SENSOR")
		if len(INVALID_HOSTNAME_INDEXLIST) > 0:		
			log.error("There are invalid hostname entries on rows: %s" % ','.join(str(index) for index in INVALID_HOSTNAME_INDEXLIST))
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
	if output_path != 0:
		if createOutputPath(str(output_path)) == False:
			log.error("Exiting!")
			sys.exit(0)

	ONLINE_SENSOR_LIST, OFFLINE_SENSOR_LIST, INVALID_HOSTNAME_LIST, UNINSTALLED_SENSOR_LIST = get_online_sensors(CBRAPI, SENSOR_LIST)
	if len(ONLINE_SENSOR_LIST) == 0:
		log.error("No online sensors were detected")
		sys.exit(0)
	log.info("\033[37mONLINE:\033[32m %d \033[37mOFFLINE:\033[33m %d \033[37mINVALID:\033[33m %d \033[37mUNINSTALLED:\033[33m %d \033[37mTOTAL:\033[36m %d" % (len(ONLINE_SENSOR_LIST), len(OFFLINE_SENSOR_LIST), len(INVALID_HOSTNAME_LIST), len(UNINSTALLED_SENSOR_LIST),len(SENSOR_LIST)))
	PROCESSING_RESULT=[]
	ERROR_LIST=[]
	CBLR_ERROR_LIST=[]
	FINISHED_SENSOR_COUNT=0
	CSV_WRITER.writerow(["HOSTNAME","OS", "STATE","RESULT", "ERRORS", "CBLR ERRORS"])

	executor = ThreadPoolExecutor(max_workers = workers)
	futures = [executor.submit(function, CBRAPI, SENSOR, module, iocs, output_path, command) for SENSOR in SENSOR_LIST]
	temp_list=[]
	for i in range(0, len(futures)):
		temp_list.append(futures[i])
	try:	
		while (not all(future.done() for future in futures)):
			time.sleep(1)
		for future in futures:
			PROCESSING_RESULT.append(future.result())
			SENSOR = future.result()[0]
			STATE = future.result()[1]
			OUTPUT_MSG = future.result()[2]
			ERROR_MSG = future.result()[3]
			CBLR_ERROR_MSG = future.result()[4]
			if ERROR_MSG != "" or CBLR_ERROR_MSG != "":
				ERROR_LIST.append(ERROR_MSG)
				#ERROR_LIST.append(CBLR_ERROR_MSG)
			CSV_WRITER.writerow([str(SENSOR['hostname']),str(SENSOR['os']).replace(',',''),str(STATE),str(OUTPUT_MSG).replace(',',''), str(ERROR_MSG).replace(',',''),str(CBLR_ERROR_MSG).replace(',','')])
			#FINISHED_SENSOR_COUNT+=1
	except (KeyboardInterrupt,SystemExit):
		CSV_WRITER.writerow(["Interrupted",])
		log.error("User Interrupted session")
		for future in futures:
			future.cancel()
		executor.shutdown(False)
		LOGFILE.close()
		os._exit(1)
	finally:
		executor.shutdown(True)
	LOGFILE.close()
	########################################################################################################################################################################################################################
	log.info("\033[37mTOTAL:\033[36m %d \033[37mONLINE:\033[32m %d \033[37mOFFLINE:\033[33m %d \033[37mUNINSTALLED:\033[33m %d \033[37mERRORS:\033[31m %d" % (len(SENSOR_LIST), len(ONLINE_SENSOR_LIST), len(OFFLINE_SENSOR_LIST), len(UNINSTALLED_SENSOR_LIST),len(ERROR_LIST)))


def cbr_run_thor(CBAPI, hostname, thor_dir, username, port):
	s = paramiko.SSHClient()
	log.log(SUCCESS, "Going to ssh into {0}:{1}".format(hostname,str(port)))
	s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		THOR_BINARY_NAME=""
		log.info("Enter the password for the CBR server")
		password = getpass.getpass()
		s.connect(hostname, port, username, password)
		log.info("Looking for binary named \"thor\" under {0}".format(thor_dir))
		command = 'cd {0} && ls thor'.format(thor_dir)
		(stdin, stdout, stderr) = s.exec_command(command)
		for line in stdout.readlines():
			THOR_BINARY_NAME = line.strip("\r\n")
			log.log(SUCCESS,"Found THOR linux binary in {0}".format(THOR_BINARY_NAME))
		for line in stderr.readlines():
			log.error("Returned Error from the remote ssh session ERROR: %s", line)
			sys.exit(0)

		CBR_BINARY_DATA_LOCATION = "/var/cb/data/modulestore/"
		THOR_CMD_LINE = "--cpulimit 70 --minmem 1024 --yara-timeout 20 --nothordb --max_runtime 24  --noatjobs --noautoruns --nodnscache --noenv --noeventlog --noevents --nofirewall --nohosts --nohotfixes --nologons --nolsasessions --nomft --nomutex --nonetworksessions --nonetworkshares --noopenfiles --noprocs --noprofiles --noreg --norootkits --noservices --noshimcache --notasks --nousers --nowmi --nowmistartup --noamcache --noc2 --nodoublepulsar --noevtx --noexedecompress --nogroupsxml --noknowledgedb --nologscan --noprefetch --noprocconnections --noprochandles --noregistryhive --noregwalk --nostix --nothordb --novulnerabilitycheck --nowebdirscan --nower --nowmipersistence -p {0}".format(CBR_BINARY_DATA_LOCATION)

		log.info("Default Location for binary storage will be scanned: {0}".format(CBR_BINARY_DATA_LOCATION))

		try:
			command = 'cd {0} && ./{1} {2}'.format(thor_dir, THOR_BINARY_NAME, THOR_CMD_LINE)
			(stdin, stdout, stderr) = s.exec_command(command, get_pty=True)

			log.log(SUCCESS,"Returned output from the remote ssh session:")
			for line in iter(stdout.readline, ""):
	   			print(line, end="")
			for line in stderr.readlines():
				log.error("Returned Error from the remote ssh session ERROR: %s", line)
				sys.exit(0)
		except (KeyboardInterrupt,SystemExit):
			log.error("User closed the connection")
		s.close()
	except Exception as e:
		log.error("Could not connect to %s ERROR: %s" % (hostname,str(e)))
		sys.exit(0)
