"""
William Fissler 2023

CreateArbitraryLog.py

A program that generates and populates a log file with various statements.
To be used as LogParser.py's data source.

Generates logging for:
- System information
- Arbitrary log spam
- Arbitrary hitch data
- Application memory consumption
- "is not defined" logic error

Identified areas for future extenstion:
- Allow users to pass arguments for how many logs to create
- Allow users to pass arguments for preferred output directory

""" 
import platform, logging, random, psutil, os, datetime, time, threading, socket, sys
    
class LogCreator:
    """ 
    Class that contains all functionality for creating a log file with arbitrary content, 
    to be used as a data source for parsing and reporting applications.
       
    Attributes
    ----------
    startTime: float
        for tracking when the application starts, and can be diffed when all executions are complete,
        to provide a "total run time".
        
    Methods
    -------    
    __init__()
        Constructor.
        Initalizes startTime attribute.
        Initalizes seed for RNG.
        
    createLogFile()
        Creates log file with time stamped naming convention. 
        Configures logging encoding format, level, and statement format.
        Create "Logs" directory if one does not exist.
        
    getSystemInfo()
        Writes Python, OS, CPU and memory specs to the log file.
        
    populateLog()
        Iterates 10K times to populate the log file, based on log choice passed into chooseLoggingType(choice).
        Prints iteration progress to the terminal window.
        
    printFinalStats()
        Prints to terminal window, and writes to the log file, the total execution time of the application.
        
    printMemoryUsage()
        Writes application's current memory footprint, at the time (since start) of the call, to the log file.
        
    printLogSpam()
        Writes an arbitrary message to the log file.
        
    printHitchLog()
        Writes an arbitrary hitch message to the log file. 
        Thread info is gotten from the application.
        Duration information is arbitrary and is the result of RNG.
        
    printErrorLog()
        Forces an undefined variable error, and writes the messages and callstack to the log file.
        
    chooseLoggingType(choice:int)
        Assess parameter value and decides which log print method to use, as the result of a modulus operation.
        Message type likelihood is ordered as (most likely -> least likely): Log Spam, Memory Usage, Hitch, Error.

    """
    
    def __init__(self) -> None:
        self.startTime = time.time() 
        random.seed() #set seed for RNG            

    def createLogFile(self):
        try: 
            
            timestamp = str(datetime.datetime.now())
            timestamp = timestamp.replace(" ","_")
            timestamp = timestamp.replace(":",".")
            logPath = '' 
            logName = "CreateArbitraryLog_"+timestamp+".log"           
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
                
            logging.basicConfig(filename=logPath + logName, encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s.%(msecs)03d] - %(levelname)s - %(message)s', datefmt='%d%b%y_%H:%M:%S')
                 
        except Exception as e:
                logging.exception(e)
        
    def getSystemInfo(self):
        try: 
            logging.info("\n Python Version: " + sys.version + "\n User: " + socket.gethostname() + "\n Operating System: " + platform.platform() + "\n CPU: " + platform.processor() + " " + str(psutil.cpu_count(logical=False)) + " Physical Cores " + str(psutil.cpu_count(logical=True)) + " Logical Cores \n Total Virtual Memory: " + str(round(psutil.virtual_memory().total/1024.0**2)) + "MB")          
        except Exception as e:
            logging.exception(e)
            
    def populateLog(self):
        for prints in range(10000): #print 10K lines (error will increase actual line count due to callstack)
            try:
                self.chooseLoggingType(random.randint(1,100))
                if prints % 99 == 0: # print terminal update every 100th line printed to log, as the cls/clear functions are very expensive. Clearing terminal each iteration increases execution time >10x 
                    os.system('cls' if os.name == 'nt' else 'clear') 
                    print("Printing lines: " + str(round((prints/100)+.01,2)) + "%") 
            except Exception as e:
                logging.exception(e)
                break  
            
    def printFinalStats(self):
        try: 
            elapsedTime = str(round(time.time()-self.startTime,2))
            print("Total Execution Time: " + elapsedTime + " seconds")
            logging.info("Total Execution Time: " + elapsedTime + " seconds")
        except Exception as e:
                logging.exception(e)    
      
    def printMemoryUsage(self):
        try:
            logging.info("Current virtual memory footprint: " + str(round(psutil.Process(os.getpid()).memory_info().rss /   1024**2,2)) + " MiB at run time: " + str(round(time.time()-self.startTime,5)))
        except Exception as e:
            logging.exception(e)
    
    def printLogSpam(self):
        try: 
            logging.info("this is an arbitrary log") 
        except Exception as e:
            logging.exception(e)  
        
    def printHitchLog(self):
        try:
            logging.warning("Hitch reported on thread: [" + str(threading.current_thread().name) + "] with a duration of: " + str(round(random.uniform(30.0, 3000.0),2)) + "ms")
        except Exception as e:
            logging.exception(e)
        
    def printErrorLog(self):
        try: 
            #force an error
            value = x * 1
        except Exception as e:
            logging.exception(e)
     
    def chooseLoggingType(self,choice):
        try: 
            # low chance to print hitch or error
            # higher chance to print memory usage (future, should do this on a tick instead of RNG)
            # highest chance to print log spam
            if choice % 7 == 0: 
                self.printMemoryUsage()
            elif choice % 25 == 0: 
                self.printHitchLog()
            elif choice % 99 == 0:
                self.printErrorLog()
            else:
                self.printLogSpam()
        except Exception as e:
            logging.exception(e)

def main():
    """
    Defines order of execution for the application.
    """
    objLogCreator = LogCreator()
    objLogCreator.createLogFile()
    objLogCreator.getSystemInfo()
    objLogCreator.populateLog()
    objLogCreator.printFinalStats()

# Execute!    
if __name__ == "__main__":
    main()    

