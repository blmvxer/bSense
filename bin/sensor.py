##Brightness Sensor Script
##blmvxer/quegmeister
##copyright 2020

import subprocess, signal, os, re, datetime

print ("Running bSense 0.2\n")
log = open("../logs/sensor.dat", 'w')
sensorList = os.system("termux-sensor -l > ../logs/sensor.lst")
print ("[*]Starting light sensor...")

def getSensor():
  proc = subprocess.Popen(["getprop ro.product.device"], stdout=subprocess.PIPE, shell=True)
  (model, err) = proc.communicate()
  fp = open("../devices/sensor.dev", 'r')
  for line in fp.readlines():
    device = line.split('-')
    if device[0] == model.rstrip().decode():
      fp.close()
      return device[1].rstrip()
    else:
      print ("Device not in list")
      fp.close()
      exit()

try:
  sensor = subprocess.Popen(["termux-sensor","-s",getSensor()], universal_newlines=True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  print ("[!]Light sensor running...")
  data = sensor.stdout
  for line in data:
    for i in line.split(','):
      topLux = (re.findall('\d+', i))
      for p in topLux:
        if int(p) == 3407:
          continue
        elif int(p) < 10000:
          nowdt = datetime.datetime.now()
          log.write("Lux: %s - %s\n" % (p, nowdt))
          print ("Lux: %s" % p)
          os.system("termux-brightness 120")
        elif int(p) > 10000:
          nowdt = datetime.datetime.now()
          print ("Lux: %s [limit detected]" % p)
          log.write("Lux: %s [limit detected] - %s\n" % (p, nowdt))
          os.system("termux-brightness 180")
        elif int(p) > 30000:
          nowdt = datetime.datetime.now()
          print ("Lux: %s [limit detected]" % p)
          log.write("Lux: %s [limit detected] - %s\n" % (p, nowdt))
          os.system("termux-brightness 230")
        elif int(p) > 50000:
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
  print ("[!] %s" % sys.exc_info()[0])
  print ("Make sure Termux:Api is installed via PlayStore and Permissions Granted...")
  print (command)
except:
  print ("\n[!]Error Detected...\n[*]Killing bSense...\n")
  sensor.send_signal(signal.SIGINT)
  os.system("termux-sensor -c")
  print ("[!] %s" % sys.exc_info()[0])
  exit()

