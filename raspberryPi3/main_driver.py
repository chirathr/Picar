from camera.video_stream import VideoStream
from motor.motor_controller import MotorController

vs = VideoStream('192.168.43.49', 8001)
mc = MotorController('192.168.43.49', 8000)
vs.start()
mc.start()
vs.join()
mc.join()
