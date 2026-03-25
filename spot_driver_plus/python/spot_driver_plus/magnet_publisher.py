#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import serial

THRESHOLD_CENTER = 530
THRESHOLD_OFFSET = 20

class MagnetPublisher(Node):
    def __init__(self):
        super().__init__('magnet_publisher')

        self.publisher = self.create_publisher(Bool, '/magnet_present', 10)

        self.ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)
        print("Serial name:", self.ser.name)

        self.timer = self.create_timer(0.1, self.poll_serial)

    def poll_serial(self):
        line = self.ser.readline().decode('utf-8').strip()
        if not line:
            return

        try:
            # Arduino sends "D:x A:y" format
            parts = line.split()
            analog_val = int(parts[1].split(':')[1])
        except (ValueError, IndexError):
            return

        magnet_detected = analog_val < (THRESHOLD_CENTER - THRESHOLD_OFFSET) or \
                          analog_val > (THRESHOLD_CENTER + THRESHOLD_OFFSET)

        print(f"Analog: {analog_val} | Magnet detected: {magnet_detected}")

        msg = Bool()
        msg.data = magnet_detected
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MagnetPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
