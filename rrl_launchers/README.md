# RRL Launchers Package

Launch file configurations for SLAM, navigation, mapping, and perception systems. This package provides pre-configured launch files for various robotics scenarios including support for multiple camera setups and different SLAM algorithms.

## Features

- **Multiple SLAM Configurations**: Support for SLAM Toolbox, Cartographer, RTAB-Map, and Hector SLAM
- **Navigation Integration**: Complete navigation stack with path planning and obstacle avoidance
- **Multi-Camera Support**: Synchronized launch configurations for multiple Intel RealSense cameras
- **Spot Robot Integration**: Specialized launch files for Boston Dynamics Spot platform
- **Flexible Configuration**: Parameterized launch files for easy customization

## Launch Files

### SLAM and Mapping

#### slam_launch.py
Complete SLAM system with mapping and perception capabilities.

```bash
ros2 launch rrl_launchers slam_launch.py
```

**Parameters:**
- `use_sim_time` (bool, default: false): Use simulation time
- `slam_params_file` (string): Path to SLAM parameters file

**Launched Nodes:**
- `slam_toolbox` (async_slam_toolbox_node): Main SLAM processing
- `map_vision`: Visual-inertial mapping integration
- `geotiff`: Real-time map export functionality

#### cartographer2d_launch.py
Google Cartographer 2D SLAM configuration.

```bash
ros2 launch rrl_launchers cartographer2d_launch.py
```

**Features:**
- Real-time 2D mapping
- Loop closure detection
- Multi-sensor fusion

#### rtabmap_launch.py
RTAB-Map RGB-D SLAM for visual-inertial mapping.

```bash
ros2 launch rrl_launchers rtabmap_launch.py
```

**Features:**
- Visual-inertial SLAM
- Dense 3D mapping
- Long-term memory management

### Navigation

#### nav2_launch.py
Complete Navigation2 stack with path planning.

```bash
ros2 launch rrl_launchers nav2_launch.py
```

**Launched Components:**
- Navigation2 stack
- Path planning
- Obstacle avoidance
- Recovery behaviors

### Perception and Sensors

#### realsenses_launch.py
Multi-camera Intel RealSense configuration.

```bash
ros2 launch rrl_launchers realsenses_launch.py
```

**Launched Cameras:**
- Front RealSense camera
- Left RealSense camera  
- Right RealSense camera
- Synchronized data streams

#### velodyne-all-nodes-VLP16-launch.py
Velodyne VLP-16 LiDAR sensor launch.

```bash
ros2 launch rrl_launchers velodyne-all-nodes-VLP16-launch.py
```

#### velodyne-all-nodes-VLP16-composed-launch.py
Composed Velodyne nodes for improved performance.

```bash
ros2 launch rrl_launchers velodyne-all-nodes-VLP16-composed-launch.py
```

### Robot Platforms

#### spot_driver_launch.py
Boston Dynamics Spot robot platform integration.

```bash
ros2 launch rrl_launchers spot_driver_launch.py
```

**Parameters:**
- `frame_prefix` (string): Frame prefix for robot state publisher

**Launched Nodes:**
- `spot_ros2`: Main Spot driver
- `robot_state_publisher`: Robot model visualization

#### exp_mapping_launch.py
Experimental mapping configurations for research and development.

```bash
ros2 launch rrl_launchers exp_mapping_launch.py
```

#### occupancy_grid_launch.py
Occupancy grid mapping from sensor data.

```bash
ros2 launch rrl_launchers occupancy_grid_launch.py
```

## Configuration Files

### config/mapper_params_online_async.yaml
SLAM Toolbox configuration for real-time mapping:

```yaml
slam_toolbox:
  ros__parameters:
    # General Parameters
    solver_plugin: solver_plugins::CeresSolver
    ceres_linear_solver: SPARSE_NORMAL_CHOLESKY
    ceres_preconditioner: SCHUR_JACOBI
    ceres_trust_strategy: LEVENBERG_MARQUARDT
    ceres_dogleg_type: TRADITIONAL_DOGLEG
    ceres_loss_function: None
    
    # SLAM Parameters
    mode: mapping
    map_file_name: test_steve
    map_start_pose: [0.0, 0.0, 0.0]
    map_start_at_dock: true
```

### Parameter Customization

Most launch files accept parameters for customization:

```bash
# Custom SLAM parameters
ros2 launch rrl_launchers slam_launch.py slam_params_file:=/path/to/custom/params.yaml

# Simulation mode
ros2 launch rrl_launchers slam_launch.py use_sim_time:=true

# Custom robot prefix
ros2 launch rrl_launchers spot_driver_launch.py frame_prefix:=spot/
```

## Usage Examples

### Complete Mapping System
```bash
# Terminal 1: Launch SLAM
ros2 launch rrl_launchers slam_launch.py

# Terminal 2: Launch cameras
ros2 launch rrl_launchers realsenses_launch.py

# Terminal 3: Launch perception
ros2 launch world_info tag_detectors_launch.py
```

### Navigation Setup
```bash
# Terminal 1: Launch SLAM
ros2 launch rrl_launchers slam_launch.py

# Terminal 2: Launch navigation
ros2 launch rrl_launchers nav2_launch.py

# Terminal 3: Set navigation goal
ros2 topic pub /goal_pose geometry_msgs/PoseStamped "..."
```

### Spot Robot Deployment
```bash
# Terminal 1: Launch Spot driver
ros2 launch rrl_launchers spot_driver_launch.py

# Terminal 2: Launch SLAM
ros2 launch rrl_launchers slam_launch.py

# Terminal 3: Launch perception
ros2 launch world_info tag_detectors_launch.py
```

### Multi-Sensor Setup
```bash
# Launch with LiDAR and cameras
ros2 launch rrl_launchers realsenses_launch.py &
ros2 launch rrl_launchers velodyne-all-nodes-VLP16-launch.py &
ros2 launch rrl_launchers slam_launch.py
```

## Hardware Configurations

### Supported Sensors
- **Intel RealSense D435/D455**: RGB-D cameras
- **Velodyne VLP-16**: 3D LiDAR
- **Boston Dynamics Spot**: Mobile robot platform
- **Kinova Gen3**: Manipulator arm

### Network Configuration
Ensure proper network setup for multi-device systems:

```bash
# Set ROS domain ID
export ROS_DOMAIN_ID=42

# Configure network interface
export RMW_IMPLEMENTATION=rmw_cyclone_dx
```

## Dependencies

### ROS 2 Packages
```bash
sudo apt install -y \
    ros-humble-slam-toolbox \
    ros-humble-cartographer \
    ros-humble-rtabmap-ros \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-realsense2-camera \
    ros-humble-velodyne \
    ros-humble-spot-driver
```

### Additional Dependencies
- `hector_geotiff`: Map export functionality
- `world_info`: Perception capabilities
- `spot_driver_plus`: Enhanced Spot integration

## Performance Tuning

### CPU Optimization
```bash
# Set CPU governor for performance
sudo cpufreq-set -g performance

# Increase process priority
sudo renice -10 $(pgrep slam_toolbox)
```

### Memory Management
```bash
# Increase shared memory for large point clouds
echo 'kernel.shmmax = 1073741824' | sudo tee -a /etc/sysctl.conf
```

### Network Optimization
```bash
# Increase network buffer sizes
echo 'net.core.rmem_max = 134217728' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max = 134217728' | sudo tee -a /etc/sysctl.conf
```

## Troubleshooting

### Common Issues

1. **Nodes fail to start**: Check all dependencies are installed
2. **TF transform errors**: Verify sensor frame configurations
3. **High CPU usage**: Reduce sensor data rates or map resolution
4. **Network timeouts**: Check ROS domain ID and network configuration

### Debug Commands

```bash
# Check launched nodes
ros2 node list

# Monitor resource usage
htop
ros2 node info /slam_toolbox

# Verify transforms
ros2 run tf2_tools view_frames.py
ros2 run tf2_ros tf2_echo base_link map

# Check topic rates
ros2 topic hz /scan
ros2 topic hz /camera/image_raw
```

### Log Analysis

```bash
# View launch logs
ros2 launch rrl_launchers slam_launch.py --ros-args --log-level DEBUG

# Monitor system logs
journalctl -u ros2-launch -f

# Check specific node logs
ros2 node info /slam_toolbox
```

## Contributing

When adding new launch files:

1. Follow existing naming conventions
2. Include parameter documentation
3. Test with relevant hardware
4. Update this README with new configurations
5. Provide usage examples

For more information, see the main [CONTRIBUTING.md](../CONTRIBUTING.md) file.