from machine import Pin, I2C
import time

# Initializing  the rotary encoder pins
clk = Pin(16, Pin.IN, Pin.PULL_UP)
dt = Pin(17, Pin.IN, Pin.PULL_UP)

# Initializing the I2C bus for the MP6050

i2c = I2C(1,scl=Pin(22), sda=Pin(21), freq=10000

# Read the rotary encoder
def read_rotary_encoder():
    clk_state = clk.value()
    dt_state = dt.value()
    if clk_state != clk_last_state:
        if dt_state != clk_state:
            return 1
        else:
            return -1
    return 0

# Reading the distance from the ultrasonic sensor
def read_ultrasonic_sensor(trig, echo):
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    while echo.value() == 0:
        pass
    t1 = time.ticks_us()
    while echo.value() == 1:
        pass
    t2 = time.ticks_us()
    distance = (t2 - t1) / 58
    return distance

# Reading the MP6050 accelerometer and gyroscope
def read_mp6050():
    # Wake up the MP6050
    i2c.writeto_mem(0x68, 0x6b, b'\x00')
    # Reading the accelerometer and gyroscope data
    accel_data = i2c.readfrom_mem(0x68, 0x3b, 14)
    accel_x = (accel_data[0] << 8) | accel_data[1]
    accel_y = (accel_data[2] << 8) | accel_data[3]
    accel_z = (accel_data[4] << 8) | accel_data[5]
    gyro_x = (accel_data[8] << 8) | accel_data[9]
    gyro_y = (accel_data[10] << 8) | accel_data[11]
    gyro_z = (accel_data[12] << 8) | accel_data[13]
    return (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)

# Main loop
while True:
    # Read the rotary encoder
    rotary_encoder_position = read_rotary_encoder()
    print("Rotary Encoder Position: ", rotary_encoder_position)
    # Read the ultrasonic sensor
    distance = read_ultrasonic_sensor(Pin(5), Pin(4))
    print("Distance: ", distance, " cm")
    # Read the MP6050
    print("MP6050 data: ", data)
    time.sleep(0.5)
   

import network
import time

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")