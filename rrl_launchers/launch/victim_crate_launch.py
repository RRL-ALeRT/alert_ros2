from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    launch_list = []

    # Magnet Publisher Node
    magnet_publisher = Node(
        package='spot_driver_plus',
        executable='magnet_publisher.py',
        output='screen'
    )
    launch_list.append(magnet_publisher)

    # Olive Magnetic Node
    olive_magnetic = Node(
        package='spot_driver_plus',
        executable='olive_magnetic.py',
        output='screen'
    )
    launch_list.append(olive_magnetic)

    # RRL QReader Kinova Node
    qreader_kinova = Node(
        package='spot_driver_plus',
        executable='rrl_qreader_kinova.py',
        output='screen'
    )
    launch_list.append(qreader_kinova)

    # RRL YOLOv8 OpenVINO Node
    yolov8_openvino = Node(
        package='spot_driver_plus',
        executable='rrl_yolov8_openvino.py',
        output='screen'
    )
    launch_list.append(yolov8_openvino)

    return LaunchDescription(launch_list)
