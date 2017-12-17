from camera.video_stream import VideoStream
from motor.motor_controller import MotorController


mc = MotorController('192.168.43.49', 8000)
vs = VideoStream('192.168.43.49', 8001)

mc.run()
vs.start()

vs.join()
