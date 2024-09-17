from alignment import Alignment
#MAIN
filename = "test_recording"
record = True
playback = False

if record:
    alignment = Alignment(filename, record, playback)
    streaming = True

    alignment.getRGB()
    ds = alignment.getDepth()
    cd = alignment.clip(ds)
    align = alignment.align()
    alignment.stream(align, cd, HSV=True)
    alignment.cleanup()
    
if playback:
    alignment = Alignment(filename, record, playback)
    alignment.getRGB()
    ds = alignment.getDepth()
    cd = alignment.clip(ds)
    align = alignment.align()
    alignment.stream(align, cd)
    alignment.cleanup()
