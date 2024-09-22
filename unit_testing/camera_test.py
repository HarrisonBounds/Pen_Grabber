from alignment import Alignment

filename = "test_recording"
record = True
playback = False

alignment = Alignment(filename, record, playback)

alignment.getRGB()
ds = alignment.getDepth()
cd = alignment.clip(ds)
align = alignment.align()

while True:
    alignment.stream(align, cd, ds)

alignment.cleanup()