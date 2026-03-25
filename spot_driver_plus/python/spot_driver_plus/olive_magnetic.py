#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from visualization_msgs.msg import Marker
import math
from scipy.spatial.transform import Rotation as R

from rviz_2d_overlay_msgs.msg import OverlayText


class MagnetometerNode(Node):
    def __init__(self):
        super().__init__('magnetometer_node')

       
        self.subscription_mag = self.create_subscription(
            Bool,
            '/magnet_present',
            self.magnetometer_callback,
            1)

        self.deck_pub = self.create_publisher(OverlayText, '/deck_text', 1)

        self.callback_timer = self.create_timer(0.2, self.timer_callback)


    def magnetometer_callback(self, msg):
        self.mag_field = "DETECTED" if msg.data else "not detected"
        if not hasattr(self, "previous_mag_field"):
            self.previous_mag_field = self.mag_field
        
    def timer_callback(self):
        if not hasattr(self, "mag_field"):
            return

        deck_msg = OverlayText()
        deck_msg.horizontal_alignment = 0
        deck_msg.vertical_alignment = 3
        deck_msg.width = 500
        deck_msg.height = 50
        deck_msg.line_width = 2
        deck_msg.text_size = 20.0
        deck_msg.fg_color.r = 0.0
        deck_msg.fg_color.g = 0.69
        deck_msg.fg_color.b = 0.67
        deck_msg.fg_color.a = 0.6

        if self.previous_mag_field != self.mag_field:
            self.previous_mag_field = self.mag_field
            deck_msg.text = f"Magnet detected: {self.mag_field}"
            self.deck_pub.publish(deck_msg)

def main(args=None):
    rclpy.init(args=args)
    magnetometer_node = MagnetometerNode()
    try:
        rclpy.spin(magnetometer_node)
    except KeyboardInterrupt:
        pass  

    magnetometer_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
