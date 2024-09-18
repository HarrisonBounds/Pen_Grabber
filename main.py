from alignment import Alignment
from control import Robot

#MAIN
filename = "test_recording"
record = True
playback = False
streaming = True
moved = False

alignment = Alignment(filename, record, playback)
robot = Robot()

alignment.getRGB()
ds = alignment.getDepth()
cd = alignment.clip(ds)
align = alignment.align()

while streaming:
    streaming = alignment.stream(align, cd, ds)
    

robot.shutdown()
    
alignment.cleanup()




