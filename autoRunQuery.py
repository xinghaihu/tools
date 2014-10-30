# automatically run query and store results in files
# @author: xinghai

import os
import string
import time
import datetime
import subprocess

# configuration
dir = os.getcwd()
ispec_file_name = dir + "/ispec_sports.txt"
startdateInput = "2014-10-13"
duration = 3
aday = 3600*24*1000
spaceidList = ["25664825"]
pos = "lrec"
outputfilename = dir + "/trend"
cmdLine = "run_query.sh list_ispec " +  ispec_file_name + " unadj_count 1000"

def generateTimeStamp ( date ):
   datet = datetime.datetime.strptime(date, "%Y-%m-%d")
   timestamp = time.mktime(datet.timetuple())
   return int(timestamp*1000) 

def generateIspec( spaceid, pos, starttimestamp, endtimestamp ):
   print "the ispec is:"
   ispec  = ""
   ispec += "<v>6113</v><t>yspaceid="
   ispec += str(spaceid)
   ispec += "ypos="
   ispec += pos
   ispec += "</t><d><s>"
   ispec += str(starttimestamp)
   ispec += "</s><e>"
   ispec += str(endtimestamp)
   ispec += "</e></d><id>-1</id><sl></sl>"
   print ispec
   return ispec

def runCommand (spaceid, daygap):
   print "run query for "+spaceid
   startdateUnixTimestamp = generateTimeStamp(startdateInput)
   starttimestamp = startdateUnixTimestamp + daygap*aday
   startDateStr = datetime.datetime.fromtimestamp(starttimestamp/1000).strftime('%Y%m%d')
   # print (starttimestamp)
   # print (  )
   endtimestamp = starttimestamp + aday
   ispec = generateIspec( spaceid, pos, starttimestamp, endtimestamp )
   f = open(ispec_file_name, 'w')
   f.write(ispec)
   f.close()
   # print(cmdLine)
   # tmpQuery = os.system(cmdLine)
   proc = subprocess.Popen([cmdLine], stdout=subprocess.PIPE, shell=True)
   (tempQuery, err) = proc.communicate()
   # print tempQuery   
   parts = tempQuery.split("\t") 
   predict = startDateStr + "," + parts[0]
   print predict
   return predict


def main():
   for spaceid in spaceidList:
      predictionList = []
      for daygap in list(xrange(duration)):
         predictionList.append(runCommand(spaceid, daygap))

      filename = outputfilename + "." + spaceid + ".csv"
      if os.path.isfile(filename):
         os.remove(filename)     
      f = open(filename, "a+")
      for line in predictionList:
         f.write(line)
      f.close()

if __name__ == "__main__":
    main()
