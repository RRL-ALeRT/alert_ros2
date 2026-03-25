#!/usr/bin/env python3

# pip3 install pupil-apriltags

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from world_info_msgs.msg import BoundingBox, BoundingBoxArray
from copy import deepcopy
from pupil_apriltags import Detector

IMAGE_TOPICS = {
    "camera_color_frame": "/kinova_color",
    "rs_front_color_optical_frame": "/rs_front/camera/color/image_raw",
    "rs_left_color_optical_frame": "/rs_left/camera/color/image_raw",
    "rs_right_color_optical_frame": "/rs_right/camera/color/image_raw",
}
DEPTH_IMAGE_TOPICS = {
    "camera_color_frame": "/depth_registered/image_rect",
    "rs_front_color_optical_frame": "/rs_front/camera/aligned_depth_to_color/image_raw",
    "rs_left_color_optical_frame": "/rs_left/camera/aligned_depth_to_color/image_raw",
    "rs_right_color_optical_frame": "/rs_right/camera/aligned_depth_to_color/image_raw",
}


class AprilTagProcessor(Node):
    def __init__(self):
        super().__init__('apriltag_processor')

        self.bounding_box_pubs_dict = {}
        self.image_subscriptions = []
        for frame_name, image_topic in IMAGE_TOPICS.items():
            pub = self.create_publisher(BoundingBoxArray, f'{image_topic}/bb', 1)
            self.bounding_box_pubs_dict[frame_name] = pub

            sub = self.create_subscription(Image, image_topic, self.listener_callback, 1)
            self.image_subscriptions.append(sub)

        self.depth_bounding_box_pubs_dict = {}
        for frame_name, depth_image_topic in DEPTH_IMAGE_TOPICS.items():
            depth_pub = self.create_publisher(BoundingBoxArray, f'{depth_image_topic}/bb', 1)
            self.depth_bounding_box_pubs_dict[frame_name] = depth_pub

        self.br = CvBridge()
        self.at_detector = Detector(
            families='tagStandard41h12',
            nthreads=1,
            quad_decimate=1.0,
            quad_sigma=0.0,
            refine_edges=1,
            decode_sharpening=0.25,
            debug=0,
        )

    def listener_callback(self, msg):
        cv_image = deepcopy(self.br.imgmsg_to_cv2(msg, desired_encoding='bgr8'))
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        tags = self.at_detector.detect(gray, estimate_tag_pose=False)

        bb_array_msg = BoundingBoxArray()
        bb_array_msg.header = msg.header
        bb_array_msg.type = "ar_tag"

        for tag in tags:
            corners = tag.corners  # shape (4, 2): bottom-left, bottom-right, top-right, top-left
            xs = corners[:, 0]
            ys = corners[:, 1]

            cx = float((xs.min() + xs.max()) / 2.0)
            cy = float((ys.min() + ys.max()) / 2.0)
            width = float(xs.max() - xs.min())
            height = float(ys.max() - ys.min())

            bb_msg = BoundingBox()
            bb_msg.name = str(tag.tag_id)
            bb_msg.width = width
            bb_msg.height = height
            bb_msg.cx = cx
            bb_msg.cy = cy

            bb_array_msg.array.append(bb_msg)

        self.bounding_box_pubs_dict[msg.header.frame_id].publish(bb_array_msg)
        self.depth_bounding_box_pubs_dict[msg.header.frame_id].publish(bb_array_msg)


def main(args=None):
    rclpy.init(args=args)
    apriltag_processor = AprilTagProcessor()
    rclpy.spin(apriltag_processor)
    apriltag_processor.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
