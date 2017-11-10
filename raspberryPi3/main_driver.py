from motor import Motor
from video_stream import VideoStream


video_stream = VideoStream('192.168.43.50', 8000)
video_stream.stream_camera_feed()
