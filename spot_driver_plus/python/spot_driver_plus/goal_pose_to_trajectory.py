#!/usr/bin/env python3

import math
import rclpy
from rclpy.action import ActionClient
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from geometry_msgs.msg import Pose, PoseStamped, TwistStamped, Vector3, Twist
from spot_msgs.action import Trajectory
from spot_msgs.srv import SetVelocity
from tf2_geometry_msgs import do_transform_pose
from rclpy.duration import Duration


class SetMaxVelocityClient(Node):
    def __init__(self):
        super().__init__('set_max_velocity_client')
        self.cli = self.create_client(SetVelocity, '/max_velocity')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = SetVelocity.Request()

    def send_request(self, linear_x, linear_y, angular_z):
        # twist_stamped = TwistStamped()
        twist = Twist()
        # twist.header.frame_id = "body"
        # twist.header.stamp = self.get_clock().now().to_msg()
        twist.linear = Vector3(x=linear_x, y=linear_y, z=0.0)
        twist.angular = Vector3(x=0.0, y=0.0, z=angular_z)
        self.req.velocity_limit = twist
        self.future = self.cli.call_async(self.req)
        return self.future


class GPPTrajectory(Node):
    def __init__(self):
        super().__init__('goal_pose_to_trajectory')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.goal_pose_sub = self.create_subscription(
            PoseStamped, "/goal_pose", self.goal_pose_cb, 1)
        self.trajectory_action_client = ActionClient(self, Trajectory, 'trajectory')
        self.goal_done = True

    def goal_pose_cb(self, msg):
        tf_map_body = None
        start_time = self.get_clock().now().to_msg().sec
        while tf_map_body is None:
            if self.get_clock().now().to_msg().sec - start_time > 5:
                self.get_logger().error('Timeout waiting for transform from map to body')
                return
            rel_frame = "body"
            target_frame = "map"
            try:
                tf_map_body = self.tf_buffer.lookup_transform(
                    rel_frame, target_frame, rclpy.time.Time())
            except TransformException as ex:
                self.get_logger().info(
                    f'Could not transform {rel_frame} to {target_frame}: {ex}')
            self.create_rate(10).sleep()

        pose = Pose()
        pose.position.x = tf_map_body.transform.translation.x
        pose.position.y = tf_map_body.transform.translation.y
        pose.orientation.z = tf_map_body.transform.rotation.z
        pose.orientation.w = tf_map_body.transform.rotation.w

        transformed_pose = do_transform_pose(msg.pose, tf_map_body)

        pose_stamped = PoseStamped()
        pose_stamped.header.frame_id = "body"
        pose_stamped.header.stamp = self.get_clock().now().to_msg()
        pose_stamped.pose = transformed_pose

        duration = Duration(seconds=10, nanoseconds=0).to_msg()
        self.send_trajectory_goal(pose_stamped, duration)

    def send_trajectory_goal(self, target_pose, duration, precise_positioning=False):
        goal_msg = Trajectory.Goal()
        goal_msg.target_pose = target_pose
        goal_msg.duration = duration
        goal_msg.precise_positioning = precise_positioning

        self.trajectory_action_client.wait_for_server()
        self.trajectory_future = self.trajectory_action_client.send_goal_async(goal_msg)


def main():
    rclpy.init()

    max_speed_setter = SetMaxVelocityClient()
    linear_x = 0.5
    linear_y = 0.5
    angular_z = 1.0
    max_speed_setter.send_request(linear_x, linear_y, angular_z)

    gpp_action_server = GPPTrajectory()
    executor = MultiThreadedExecutor()
    rclpy.spin(gpp_action_server, executor=executor)

    gpp_action_server.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
