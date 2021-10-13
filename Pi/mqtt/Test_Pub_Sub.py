##Script to test publish and subscribe scripts
##Imports
import Publish as p
import Subscribe as s
import time

##Send two strings (An invalid string then a valid string)
p.send("ignore this")
p.send("pi: Testing")

##Wait 5s
time.sleep(5)

##Start listening
x = s.sub_loop()
##Print the output
print(x)
