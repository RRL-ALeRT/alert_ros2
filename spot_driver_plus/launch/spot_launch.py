import launch
import launch_ros
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
import os
from launch.actions import ExecuteProcess


def generate_launch_description():
    spot_plus = LaunchDescription()

    # Declare the 'config_file' argument
    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=os.path.join(get_package_share_directory('spot_driver_plus'), 'config', 'spot_params.yaml'),
        description='Path to the config file'
    )
    spot_plus.add_action(config_file_arg)

    # os.environ["SPOT_URDF_EXTRAS"] = os.path.join(get_package_share_directory('spot_driver_plus'), 'urdf', 'gen3.urdf.xacro')
    # Include and launch the child launch file
    child_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('spot_driver'), 'launch', 'spot_driver.launch.py')),
        launch_arguments={'config_file': launch.substitutions.LaunchConfiguration('config_file'), 'stitch_front_images': 'True'}.items(),
    )
    spot_plus.add_action(child_launch)

    map_vision_node = launch_ros.actions.Node(
        package='spot_driver_plus',
        executable='map_vision',
        output='screen',
    )
    spot_plus.add_action(map_vision_node)

    goal_pose_to_trajectory = launch_ros.actions.Node(
       package='spot_driver_plus',
       executable='goal_pose_to_trajectory.py',
       output='screen',
    )
    spot_plus.add_action(goal_pose_to_trajectory)

    arduino_lights = launch_ros.actions.Node(
       package='spot_driver_plus',
       executable='arduino_lights.py',
       output='screen',
    )
    # spot_plus.add_action(arduino_lights)

    livox_tf = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        output='screen',
        arguments=['--x', '0.39', '--y', '0', '--z', '0.14',
                '--yaw', '1.56', '--pitch', '3.14', '--roll',
                '2.35', '--frame-id', 'body', '--child-frame-id', '/livox_frame'],
    )

    spot_plus.add_action(livox_tf)

    body_world = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'body', 'world'],
        output='screen',
    )
    spot_plus.add_action(body_world)

    return spot_plus
