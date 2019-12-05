import psutil
PROCNAMES = ["chrome.exe","chromedriver.exe","iexplorer.exe"] #"iexplorer.exe"
def KillProcesses(*procnames):
 """Killing predefined processes """
 #procnames = ["chrome.exe","chromedriver.exe"]
 count=0
 procCount=0
 for proc in psutil.process_iter():
    procCount +=1
    # check whether the process name matches
    if proc.name() in PROCNAMES:
       try:
        proc.kill()
       except:
        continue
       #print(proc.name())
       count+=1
 print("Total processs killed="+str(count)+" Total="+str(procCount))
if __name__ == '__main__':
    KillProcesses()