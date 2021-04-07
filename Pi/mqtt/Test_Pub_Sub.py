import Publish as p
import Subscribe as s
import time

#p.send("ignore this")
#p.send("pi: Testing")

#time.sleep(5)

x = s.sub_loop()
print(x)
