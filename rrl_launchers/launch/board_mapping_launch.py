from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

# pkg_dir = get_package_share_directory("spot_gen3_moveit")
# linear_board_launch = os.path.join(pkg_dir, "launch", "linear_board.launch.py")


def generate_launch_description():
    launch_list = []

    child_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('spot_gen3_moveit'), 'launch', 'linear_board.launch.py')),
    )
    launch_list.append(child_launch)

    world_info = Node(
        package="world_info",
        executable="world_info",
        output="screen",
        parameters=[{"single_object_of_each_type": True}],
    )
    launch_list.append(world_info)

    qr_detector = Node(
        package="spot_driver_plus",
        executable="rrl_apriltag.py",
        output="screen",
    )
    # launch_list.append(qr_detector)

    hazmat_node = Node(
        package="spot_driver_plus",
        executable="rrl_yolov8_openvino.py",
        output="screen",
        parameters=[{"model": "hazmat"}],
    )
    # launch_list.append(hazmat_node)

    object_node = Node(
        package="spot_driver_plus",
        executable="kinova_yolov8_openvino.py",
        output="screen",
        parameters=[{"model": "board"}],
    )
    launch_list.append(object_node)

    kinova = ExecuteProcess(
                        cmd=['ros2', 'run', 'world_info', 'tf2_object_detection_yolov5', '/kinova_color', '/depth_registered/camera_info'],
                        output='screen'
                    )
    launch_list.append(kinova)
    tf2_rs_front = ExecuteProcess(
                        cmd=['ros2', 'run', 'world_info', 'tf2_object_detection_yolov5', '/rs_front/camera/aligned_depth_to_color/image_raw', '/rs_front/camera/aligned_depth_to_color/camera_info'],
                        output='screen'
                    )
    launch_list.append(tf2_rs_front)
    tf2_rs_left = ExecuteProcess(
                        cmd=['ros2', 'run', 'world_info', 'tf2_object_detection_yolov5', '/rs_left/camera/aligned_depth_to_color/image_raw', '/rs_left/camera/aligned_depth_to_color/camera_info'],
                        output='screen'
                    )
    launch_list.append(tf2_rs_left)
    tf2_rs_right = ExecuteProcess(
                        cmd=['ros2', 'run', 'world_info', 'tf2_object_detection_yolov5', '/rs_right/camera/aligned_depth_to_color/image_raw', '/rs_right/camera/aligned_depth_to_color/camera_info'],
                        output='screen'
                    )
    launch_list.append(tf2_rs_right)

    return LaunchDescription(launch_list)
