##Brightness Sensor Script
##blmvxer/quegmeister
##copyright 2020

import subprocess, signal, os, re, datetime

print ("Running bSense 0.2\n")
log = open("../log/sensor.dat", 'w')
sensorList = os.system("termux-sensor -l > ../log/sensor.lst")
print ("[*]Starting light sensor...")

try:
  sensor = subprocess.Popen(["termux-sensor","-s","TCS3407"], universal_newlines=True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  print ("[!]Light sensor running...")
  data = sensor.stdout
  for line in data:
    for i in line.split(','):
      topLux = (re.findall('\d+', i))
      for p in topLux:
        if int(p) == 3407:
          continue
        elif int(p) > 80000:
          nowdt = datetime.datetime.now()
          print ("Lux: %s [limit detected]" % p)
          log.write("Lux: %s [limit detected] - %s\n" % (p, nowdt))
          os.system("termux-brightness 255")
        else:
          nowdt = datetime.datetime.now()
          log.write("Lux: %s - %s\n" % (p, nowdt))
          print ("Lux: %s" % p)

except KeyboardInterrupt:
  print ("\n[!]Keyboard Interrupt...\n[*]Killing bSense...\n")
  sensor.send_signal(signal.SIGINT)
  os.system("termux-sensor -c")
  print ("[!]sensor unhooked ... bSense killed.")
  exit()

except FileNotFoundError:
  print ("Make sure Termux:Api is installed via PlayStore and Permissions Granted...")
except:
  print ("\n[!]Error Detected...\n[*]Killing bSense...\n")
  sensor.send_signal(signal.SIGINT)
  os.system("termux-sensor -c")
  print ("[!] %s" % sys.exc_info()[0])
  exit()

