#!/usr/bin/env python
# @author Connor Lange
# A simple Python script that takes a newly created 24-bit .bmp file 
# and performs the correct hex edits, and at the user's option, puts it 
# into a flashable .zip for them  
from subprocess import call
from sys import platform
from subprocess import Popen
from subprocess import PIPE
from os import system
import Image

if platform[:3] == 'win':
   ret = system('cls')
else: 
   ret = system('clear')
print("\n\nBootLogo Auto Creator (Droid X and Droid2 Only) V 1.1...")
print("Created by Connor Lange\n\n")
print("Drag your boot logo .bmp file into this window to proceed.")
response = raw_input("File: ")
if response == '' or response[-4:] != '.bmp':
   print("Invalid boot logo. The boot logo MUST be created from a 24-bit .bmp image")
   raw_input("Press ENTER to continue: ")
   exit()
Image.open(response).transpose(Image.FLIP_LEFT_RIGHT).save(response[:-4]+"flip.bmp")
logoFile = open(response[:-4]+"flip.bmp", 'rb').read() # read the entire image file

# More error checking 
# ALWAYS 262134 since the image library used above outputs this size after flipping the 
# image regardless of the program that was used to create the image (even Photoshop)
if len(logoFile) == 262134:  
   print("Removing the first 54 bytes from your image...")
   logoImg = logoFile[54:] # Remove first 54 bytes
else:
   print("The file you supplied is not of the correct size.")
   print("After flipping the image, your file size should have been 262134 bytes.")
   print("However, your file size was: "+str(len(logoFile))+" bytes")
   raw_input("Press ENTER to continue: ")
   exit()
print("Reversing the bytes in your image...")   
logoImg = logoImg[::-1] # Reverse the bytes
finishedLogo = open('logo.bin', 'wb') # create a logo.bin in this directory
finishedLogo.write(logoImg) # Write out the modified image to logo.bin 
finishedLogo.close()
print("\nYour new boot logo has been created!!")
print("It has been named logo.bin and is located in the same folder as ")
print("this script. You'll need to put it into the TBH LogoReplacer.zip ")
print("before flashing. Would you like to do that now?")
decision = raw_input("y/n?: ")
if decision == 'y':
   process = Popen(['7za', 'u', 'BootLogo.zip', 'logo.bin'], stderr=PIPE)
   process.wait()
   errors = process.stderr.read()
   if errors: 
      print("The follow errors occured in 7-zip:")
      print(errors)
      print("\nNote that yout boot logo has still been created as logo.bin")
   else:
      print("\nYour flashable boot logo replacer has been created as 'BootLogo.zip'")
      print("You will need to move this zip to your SDcard. Then you'll need to reboot into")
      print("Clockwork and flash it. Would you like to copy the .zip to the root of your SDcard?")
      response = raw_input("y/n?: ")
      if response == 'y':
         while True:
            print("Pushing BootLogo.zip to /sdcard/\n")
            process = Popen(['adb','push','BootLogo.zip','/sdcard/'])
            process.wait()
            if process.returncode != 0:
               print("\nLooks like an error occurred... Please fix it.")
               print("Make sure that you have USB debugging turned on and your")
               print("phone isn't in USB storage (or something that mounts the SD card")
               response = raw_input("Would you like to try again? (y/n): ")
               if response == 'y': 
                  continue
               else: 
                  print("Your flashable BootLogo.zip has still been created.")
                  print("Manually copy that to your SD card and boot into Clockwork")
                  print("and you'll be good to go!")
                  break
            else:
               print("\nSuccess! Now reboot into Clockwork and do the following:")
               print("1: install zip from sdcard")
               print("2: choose zip from sdcard")
               print("3: find and select BootLogo.zip")
               print("4: Yes - install BootLogo.zip")
               print("5: reboot system now -- Enjoy!")
               break
raw_input("\nPress ENTER to quit: ") 