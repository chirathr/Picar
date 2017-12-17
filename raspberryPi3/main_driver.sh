python -m motor.motor_controller 192.168.43.49 8000 &
python -m camera.video_stream 192.168.43.49 8001 &
python -m ultrasonic.ultrasonic_stream_client 192.168.43.49 8002;
fg; fg;
