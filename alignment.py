import pyrealsense2 as rs
import numpy as np
import cv2

class Alignment:
    def __init__(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        
        self.pipeline_wrapper = rs.config()
        
        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        self.device_product_line = str(self.device.get_info(rs.camera_info.product_line))
        self.clipping_distance_meters = 1 #In meters
        
    def getRGB(self):
        found_rgb = False
        for s in self.device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        
    def getDepth(self):
        # Start streaming
        profile = self.pipeline.start(self.config)

        # Getting the depth sensor's depth scale (see rs-align example for explanation)
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale is: " , depth_scale)
        
        return depth_scale
        
    def clip(self, depth_scale):
        clipping_distance = self.clipping_distance_meters / depth_scale
        return clipping_distance
    
    def align(self):
        align_to = rs.stream.color
        align = rs.align(align_to)
        return align
    
    def stream(self, align, clipping_distance):
        # Streaming loop
        try:
            while True:
                # Get frameset of color and depth
                frames = self.pipeline.wait_for_frames()
                # frames.get_depth_frame() is a 640x360 depth image

                # Align the depth frame to color frame
                aligned_frames = align.process(frames)

                # Get aligned frames
                aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
                color_frame = aligned_frames.get_color_frame()

                # Validate that both frames are valid
                if not aligned_depth_frame or not color_frame:
                    continue

                depth_image = np.asanyarray(aligned_depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                # Remove background - Set pixels further than clipping_distance to grey
                grey_color = 153
                depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
                bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

                # Render images:
                #   depth align to color on left
                #   depth on right
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
                images = np.hstack((bg_removed, depth_colormap))

                cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
                cv2.imshow('Align Example', images)
                key = cv2.waitKey(1)
                # Press esc or 'q' to close the image window
                if key & 0xFF == ord('q') or key == 27:
                    cv2.destroyAllWindows()
                    break
        finally:
            self.pipeline.stop()

#MAIN
alignment = Alignment()
alignment.getRGB()
ds = alignment.getDepth()
cd = alignment.clip(ds)
align = alignment.align()
alignment.stream(align, cd)