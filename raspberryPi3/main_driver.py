from camera.video_stream import VideoStream

vs = VideoStream('192.168.43.49', 8001)
vs.start()
vs.join()
