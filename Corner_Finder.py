import Read_Sensors as sensor
import motor_controller as motor

def identify_corner():
	motor.slow_turn()
	values = []
	while True:
		values.append(sensor.getTFminiData())
		if values.size > 5:
			if (values[0] / 2 + values[1] / 2) < values[3] < (values[4] / 2 + values[5] / 2):
				print("Corner Identified")
				break
			values.pop(0)
	print("Function continuing")

identify_corner()


