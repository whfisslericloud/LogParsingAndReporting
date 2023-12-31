"""
William Fissler 2023

LogParser.py

A program that parses all logs in a given path, and outputs results (into csv files) for the following:
- Machine (system) information (Work in progress)
- Memory usage statistics
- LogSpam (Work in progress)
- Hitch occurances and statistics 
- Error ocurrances and callstacks (Work in progress)
- Unit test results for the parsing operations (Work in progress)

Uses log files generated by CreateArbitraryLog.py as data source/s.

Identified areas for future extenstion:
- Develop logic to assess for duplicate log statements to be considered for log spam
- Allow users to pass arguments for preferred input directory
- Allow users to pass arguments for preferred output directory
- Allow users to pass arguments for what criteria to parse for
- Allow users to pass arguments for what file formats to store the results in
- Develop functionality to convert .log files to interactive HTML files 
- Refactor for improved performance and algorithm design

""" 

import logging, os, datetime, platform, glob, re, csv, time

startTime = time.time()

def createLogFile():
    """Creates log file with time stamped naming convention. 
        Configures logging encoding format, level, and statement format.
        Create "Logs" directory if one does not exist."""
    try:  
        createLogFileTime = round(time.time(),5)          
        timestamp = str(datetime.datetime.now())
        timestamp = timestamp.replace(" ","_")
        timestamp = timestamp.replace(":",".")
        logPath = '' 
        logName = "LogParser_"+timestamp+".log"          
        fileDupeNum = 0 
        
        if not os.path.exists("Logs"):
            os.makedirs("Logs")
                            
        while os.path.isfile(logName):
            logging.info(logName + "already exists")
            fileDupeNum += 1
            logName = logName+"("+str(fileDupeNum)+".csv"
            
        if platform.system() == "Windows":
            logPath = 'Logs"\"'
        else:
            logPath = "Logs/"   
            
        logging.basicConfig(filename=logPath + logName, 
                            encoding='utf-8', 
                            level=logging.DEBUG, 
                            format='[%(asctime)s.%(msecs)03d] - %(levelname)s - %(message)s', 
                            datefmt='%d%b%y_%H:%M:%S')
         
        createLogFileTime = round(time.time()-createLogFileTime,5)
        logging.info("Time to execute createLogFile: " + str(createLogFileTime) + " seconds")                
    except Exception as e:
        createLogFileTime = round(time.time()-createLogFileTime,5)
        logging.info("Time to execute createLogFile: " + str(createLogFileTime) + " seconds")
        logging.exception(e)                

class LogParser:
    """
    Class for handling all parsing of criteria from log files and caching it for future use.
    
    Attributes
    ----------
    hitchList[] : str
        Stores a list of strings (log lines) matching hitchCriteria to be stored for sub string extraction, 
        prior to being written to csv file.
    memoryList[] : str
        Stores a list of strings (log lines) matching memoryCriteria to be stored for sub string extraction, 
        prior to being written to csv file.
    errorList[] : str
        Stores a list of strings (log lines) matching errorCriteria (including associated callstack) to be stored for sub string extraction, 
        prior to being written to csv file. 
    logSpamList[] : str
        Stores a list of strings (log lines) that have been identified as repeated entries greater than or equal to logSpamCriteria, 
        prior to being written to csv file.
    systemInfoList[] : str
        Stores a list of strings (log lines) matching systemInfoCriteria to be stored for sub string extraction, 
        prior to being written to csv file.
    hitchCriteria : str
        Defaults to "Hitch".
    memoryCriteria : str
        Defaults to "memory footprint".
    errorCriteria : str
        Defaults to "Error".
    systemInfoCriteria : str
        Defaults to "System Information - ".
    logSpamCriteria : int 
        Defaults to 100 (represents number of times encountered).
        
    Methods
    -------
    __init__
        Constructor.
        Initializes the following attributes: 
        hitchList, memoryList, errorList, logSpamList, systemInfoList, hitchCriteria, memoryCriteria, 
        systemInfoCriteria, logSpamCriteria, startTime.
    
    printFinalStats()
        Prints to terminal window, and writes to the log file, the total execution time of the application.
        
    cacheLogs() -> list
        Verifies working directory for files to be processed.
        Finds all files of .log extension, stores them in the logCache, and returns the logCache list.
        :returns: logCache - list of strings representing .log file names found.
        :rtype: list  
        
    interateLogs(logCache:list)
        Verifies logCache has contents prior to processing.
        Iterate through each line of each log file in logCache and evaluates for the established criteria, 
        and appends the appropriate list with the log line containing the matched criteria.
        :param logCache: list of strings representing .log file names cached by cacheLogs().
        :type logCache: list
    """
    def __init__(self) -> None:
        """Constructor.
        Initializes the following attributes: 
        hitchList, memoryList, errorList, logSpamList, systemInfoList, hitchCriteria, memoryCriteria, 
        systemInfoCriteria, logSpamCriteria, startTime."""
        self.hitchList = []
        self.memoryList = []
        self.errorList = []
        self.logSpamList = []
        self.systemInfoList = []
        self.hitchCriteria = "Hitch"
        self.memoryCriteria = "memory footprint"
        self.errorCriteria = "ERROR"
        self.systemInfoCriteria = "System Information - "
        self.logSpamCriteria = 100 
    
    def printFinalStats(self):
        """Prints to terminal window, and writes to the log file, the total execution time of the application."""
        try: 
            elapsedTime = str(round(time.time()-startTime,2))
            print("Total Execution Time: " + elapsedTime + " seconds")
            logging.info(f"Lines matching: \n Hitch Criteria: " + str(len(self.hitchList)) + 
                         "\n Memory Criteria: " + str(len(self.memoryList)) + 
                         "\n Error Criteria: " + str(len(self.errorList)) + 
                         "\n Log Spam Criteria:  " + str(len(self.logSpamList)))
            logging.info("Total Execution Time: " + elapsedTime + " seconds")
        except Exception as e:
            logging.exception(e)

    def cacheLogs(self) -> list:
        """Verifies working directory for files to be processed.
        Finds all files of .log extension, stores them in the logCache, and returns the logCache list.
        
        :returns: logCache - list of strings representing .log file names found.
        :rtype: list """
        try:
            cacheLogsTime = time.time()
            logCache = []
            logging.info("Current working directory is: " + os.getcwd())
            
            if os.path.exists("Logs"):  
                          
                os.chdir("Logs") #set working directory to log storage location before caching logs
                logging.info("Current working is set to: " + os.getcwd())
                
                for file in glob.glob('CreateArbitraryLog*.log'):
                    index = 0
                    logCache.append(file) 
                    logging.info("Found Log: " + file)
                    index += 1
                    
            cacheLogsTime = round(time.time()-cacheLogsTime,5)
            logging.info("Time to execute createLogFile: " + str(cacheLogsTime) + "ms")
            
            return logCache
        
        except Exception as e:
            cacheLogsTime = round(time.time()-cacheLogsTime,5)
            logging.info("Time to execute cacheLogs: " + str(cacheLogsTime) + "ms")
            logging.exception(e)

    def iterateLogs(self,logCache):
        """Verifies logCache has contents prior to processing.
        Iterate through each line of each log file in logCache and evaluates for the established criteria, 
        and appends the appropriate list with the log line containing the matched criteria.
        
        :param logCache: list of strings representing .log file names cached by cacheLogs().
        :type logCache: list"""
        try:
            iterateLogsTime = time.time()
                       
            if len(logCache) != 0: # check to see if cache is empty 
                                
                logCount = 0 # to track how many logs have been iterated through   
                                                
                for log in logCache:      
                                  
                    lineNumber = 1 # current to track line number being parsed       
                                
                    with open(log) as cachedLog:  
                        while True:
                               
                            line = cachedLog.readline()
                            
                            if not line: # check if end of file
                                logging.info("Finished processing file: " + str(logCount+1) + "/" + str(len(logCache)) + " : " + log)
                                lineNumber = 0 # reset line number at end of file
                                break
                            else:
                                if re.search(self.hitchCriteria, line) is not None:
                                    line = log + " - " + line + " at line number: " + str(lineNumber)
                                    self.hitchList.append(line)
                                    logging.info("Hitch data found on line " + str(lineNumber))                                
                                elif re.search(self.memoryCriteria, line) is not None:
                                    line = log + " - " + line + " at line number: " + str(lineNumber)
                                    self.memoryList.append(line)
                                    logging.info("Memory data found on line " + str(lineNumber))
                                elif re.search(self.errorCriteria, line) is not None:
                                    line = log + " - " + line
                                    tempLine = cachedLog.readline()
                                    while tempLine[0] != '[':
                                        line += "\n" + tempLine
                                        lineNumber += 1 # increment line number due to the extra callstack lines
                                        tempLine = cachedLog.readline()
                                    line += " at line number: " + str(lineNumber)
                                    self.errorList.append(line)
                                    logging.info("Error data found on line " + str(lineNumber))                                        
                                else:
                                    logging.info("No reportable criteria found in " + log + " on line " + str(lineNumber)) 
                                    
                            lineNumber += 1 # increment line number before evaluating next log line
                    logCount += 1 # increment number of files processed before evaluating next log file
            else:
                logging.warning("Log Cache is Empty!")
                
            iterateLogsTime = round(time.time()-iterateLogsTime,5)
            logging.info("Time to execute iterateLogs: " + str(iterateLogsTime) + " seconds")
        except Exception as e:
            cacheLogsTime = round(time.time()-cacheLogsTime,5)
            logging.info("Time to execute iterateLogs: " + str(iterateLogsTime) + " seconds")
            logging.exception(e)
    
    # WIP placeholder 
    # def sortForLogSpam(self, logCache):
    #     try: 
    #         while True:
    #             for log in range(len(logCache)):
    #                 tempLogCache = []
                    
    # #     except Exception as e:
    #             logging.exception(e)
            
class CSVWriter:
    """
    Class for handling all CSV file related operations.
    
    Attributes
    ----------
    none
    
    Methods
    -------
    def checkForExistingFile(fileName:str) -> str
        Evaluates path for existing file of name to avoid overwriting.
        If file of name exists, increments duplicate number and reevaluates until a match does not exist.
        
        :param fileName: desired file name to be created
        :type fileName: str
        :returns: fileName - either fileName appended with (n) duplicate value, or same value that was initially passed
        :rtype: str
    
    writeMemoryFootprintToCSV(memoryList:list)
        Creates .csv file, applies header, iterates through each line in memoryList parsing for:
        log file name, the line number the match occured in the respective log file, the footprint size, 
        and at what run time the record occured, then applies the stats to the .csv's row.
        
        :param memoryList: list of log lines matched to memoryCriteria
        :type memoryList: list 
        
    writeHitchToCSV(hitchList:list)
        Creates .csv file, applies header, iterates through each line in hitchList parsing for:
        log file name, the line number the match occured in the respective log file, the thread name, 
        and the hitch duration, then applies the stats to the .csv's row.
        
        :param hitchList: list of log lines matched to memoryCriteria
        :type hitchList: list 
    """
    
    def __init__(self) -> None:
        pass #placeholder until properties are established
    
    def checkForExistingFile(self, fileName) -> str:
        """Evaluates path for existing file of name to avoid overwriting.
        If file of name exists, increments duplicate number and reevaluates until a match does not exist.
        
        :param fileName: desired file name to be created
        :type fileName: str
        :returns: fileName - either fileName appended with (n) duplicate value, or same value that was initially passed
        :rtype: str"""
        try:
            
            checkForExistingFileTime = time.time()   
            fileDupeNum = 0 
            
            if fileName == "HitchReport.csv":                        
                while os.path.isfile(fileName):
                    logging.info(fileName + " already exists")
                    fileDupeNum += 1
                    fileName = "HitchReport("+str(fileDupeNum)+").csv"
            elif fileName == "MemoryReport.csv":
                while os.path.isfile(fileName):
                    logging.info(fileName + " already exists")
                    fileDupeNum += 1
                    fileName = "MemoryReport("+str(fileDupeNum)+").csv"
            elif fileName == "ErrorReport.csv":
                while os.path.isfile(fileName):
                    logging.info(fileName + " already exists")
                    fileDupeNum += 1
                    fileName = "ErrorReport("+str(fileDupeNum)+").csv"
            else:
                print(fileName + " is and invalid file name for csv creation")
                logging.error(fileName + " is and invalid file name for csv creation")
                                    
            logging.info("Creating CSV file: " + fileName)
            checkForExistingFileTime = round(time.time()-checkForExistingFileTime,5)
            logging.info("Time to execute checkForExistingFile: " + str(checkForExistingFileTime) + " seconds")
            return fileName

        except Exception as e:
            checkForExistingFileTime = round(time.time()-checkForExistingFileTime,5)
            logging.info("Time to execute checkForExistingFile: " + str(checkForExistingFileTime) + " seconds")
            logging.exception(e)

    def writeMemoryFootprintToCSV(self, memoryList):
        """Creates .csv file, applies header, iterates through each line in memoryList parsing for:
        log file name, the line number the match occured in the respective log file, the footprint size, 
        and at what run time the record occured, then applies the stats to the .csv's row."""
        try:
            writeMemoryFootprintToCSVTime = time.time()
             
            if len(memoryList) != 0:
                 with open(self.checkForExistingFile("MemoryReport.csv"), 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    header = ["Log Name", "Log Line", "Footprint (MiB)", "Time Recorded"]
                    writer.writerow(header)
                    
                    for line in range(len(memoryList)):
                        logName = (re.search(r"([^\s]+)", memoryList[line])).group()     
                        lineNumber = (re.search(r"\d+$", memoryList[line])).group()                   
                        footprint = (re.search(r"footprint:\s(\d+\.\d+)",memoryList[line])).group().strip("footprint: ")               
                        timeRecorded = (re.search(r"run time:\s(\d+\.\d+)",memoryList[line])).group().strip("run time: ")              
                        row = [logName, lineNumber, footprint, timeRecorded]
                        writer.writerow(row)
            else:
                logging.warning("Failure to write Memory Report. Memory List is empty") 
            
            writeMemoryFootprintToCSVTime = round(time.time()-writeMemoryFootprintToCSVTime,5)
            logging.info("Time to execute writeMemoryFootprintToCSV: " + str(writeMemoryFootprintToCSVTime) + " seconds")                        
        except Exception as e:
            writeMemoryFootprintToCSVTime = round(time.time()-writeMemoryFootprintToCSVTime,5)
            logging.info("Time to execute writeMemoryFootprintToCSV: " + str(writeMemoryFootprintToCSVTime) + " seconds")
            logging.exception(e)                   
            
    def writeHitchToCSV(self, hitchList):
        """Creates .csv file, applies header, iterates through each line in hitchList parsing for:
        log file name, the line number the match occured in the respective log file, the thread name, 
        and the hitch duration, then applies the stats to the .csv's row.
        
        :param hitchList: list of log lines matched to memoryCriteria
        :type hitchList: list"""        
        try: 
            writeHitchToCSVTime = time.time()
            
            if len(hitchList) != 0:                
                with open(self.checkForExistingFile("HitchReport.csv"), 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    header = ["Log Name", "Log Line", "Thread", "Duration (ms)"]
                    writer.writerow(header)
                    
                    for line in range(len(hitchList)):
                        logName = (re.search(r"([^\s]+)", hitchList[line])).group()    
                        lineNumber = (re.search(r"at line number:\s(\d+$)", hitchList[line])).group().strip("at line number: ")                   
                        hitchDuration = (re.search(r"duration of:\s(\d+\.\d+)", hitchList[line])).group().strip("duration of: ") #duration require log name to be stripped so that only one set of decimal numbers exist              
                        threadName = (re.search(r'thread:\s\[(.+?)\]', hitchList[line])).group().strip("thread: ").strip("[]")          
                        row = [logName, lineNumber, threadName, hitchDuration]
                        writer.writerow(row)
            else:
                logging.warning("Failure to write Hitch Report: Hitch List is empty")
            
            writeHitchToCSVTime = round(time.time()-writeHitchToCSVTime,5)
            logging.info("Time to execute writeHitchToCSV: " + str(writeHitchToCSVTime) + " seconds")
        except Exception as e:
            writeHitchToCSVTime = round(time.time()-writeHitchToCSVTime,5)
            logging.info("Time to execute writeHitchToCSV: " + str(writeHitchToCSVTime) + " seconds")
            logging.exception(e)
        
    def writeErrorsToCSV(self, errorList):
        """Creates .csv file, applies header, iterates through each line in hitchList parsing for:
        log file name, the line number the match occured in the respective log file, the thread name, 
        and the hitch duration, then applies the stats to the .csv's row.
        
        :param hitchList: list of log lines matched to memoryCriteria
        :type hitchList: list"""        
        try: 
            writeErrorsToCSVTime = time.time()
            
            if len(errorList) != 0:                
                with open(self.checkForExistingFile("ErrorReport.csv"), 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    header = ["Log Name", "Log Line", "Error Type", "Error Message"]
                    writer.writerow(header)
                    
                    for line in range(len(errorList)):
                        logName = (re.search(r"([^\s]+)", errorList[line])).group()       
                        lineNumber = (re.search(r"at line number:\s(\d+$)", errorList[line])).group().strip("at line number: ")             
                        errorMessage = errorList[line].strip(logName).strip("at line number: " + lineNumber)
                        errorMessage = re.sub(r'[\s\S]*?(?=ERROR)', '', errorMessage)
                        errorType = None                  
                        errorType = (re.search(r'[$\w]+(?=:\s)', errorMessage)).group()
                        row = [logName, lineNumber, errorType, errorMessage]
                        writer.writerow(row)
            else:
                logging.warning("Failure to write Error Report: Error List is empty")

            writeErrorsToCSVTime = round(time.time()-writeErrorsToCSVTime,5)
            logging.info("Time to execute writeErrorsToCSV: " + str(writeErrorsToCSVTime) + " seconds")
        except Exception as e:
            writeErrorsToCSVTime = round(time.time()-writeErrorsToCSVTime,5)
            logging.info("Time to execute writeErrorsToCSV: " + str(writeErrorsToCSVTime) + " seconds")
            logging.exception(e)
    
    
    # WIP placeholder         
    # def writeLogSpamToCSV():
    
    # WIP placeholder         
    # def writeSystemInfoToCSV():
    
def main():
    """Defines order of execution for the application"""
    createLogFile()
    
    # instantiate objects
    objCSVWriter = CSVWriter()    
    objLogParser = LogParser()

    # gather data
    objLogParser.iterateLogs(objLogParser.cacheLogs())
    
    # perform write opertations
    objCSVWriter.writeHitchToCSV(objLogParser.hitchList)
    objCSVWriter.writeMemoryFootprintToCSV(objLogParser.memoryList)
    objCSVWriter.writeErrorsToCSV(objLogParser.errorList)

    objLogParser.printFinalStats()

# Execute!    
if __name__ == "__main__":
    main()