# Spot Driver Plus Package

Enhanced Boston Dynamics Spot robot driver with additional perception features, manipulation capabilities, and advanced autonomy functions.

## Features

- **Extended Spot Control**: Enhanced robot control with additional safety features
- **YOLO Object Detection**: Real-time object detection with YOLOv8 and OpenVINO acceleration
- **Kinova Arm Integration**: Manipulator control and coordination with Spot platform
- **Point Cloud Processing**: Advanced 3D perception and mapping capabilities
- **Emergency Stop**: Comprehensive safety system with multiple stop mechanisms
- **Path Planning**: 3D path planning for complex navigation scenarios
- **Magnetic Sensor Integration**: Specialized sensors for inspection tasks

## Nodes

### C++ Nodes

#### battery_screen
Displays Spot's battery status and system information.

```bash
ros2 run spot_driver_plus battery_screen
```

#### depth_to_pcl
Converts depth images to point clouds for 3D perception.

**Subscribed Topics:**
- `/depth/image_rect` (sensor_msgs/Image): Input depth image

**Published Topics:**
- `/pointcloud` (sensor_msgs/PointCloud2): Generated point cloud

#### spot_marker
Creates interactive markers for Spot visualization and control.

**Published Topics:**
- `/spot_markers` (visualization_msgs/MarkerArray): Interactive markers

#### spot_kinova_controller
Controls the Kinova manipulator mounted on Spot.

**Services:**
- `/kinova/move_to_pose` (geometry_msgs/PoseStamped): Move arm to target pose
- `/kinova/grasp` (std_srvs/Trigger): Execute grasp action

#### map_vision
Integrates mapping data with visual perception for enhanced SLAM.

**Subscribed Topics:**
- `/map` (nav_msgs/OccupancyGrid): SLAM map data
- `/camera/image` (sensor_msgs/Image): Visual input

### Python Nodes

#### kinova_yolov8_openvino.py
Real-time object detection using YOLOv8 with OpenVINO acceleration.

```bash
ros2 run spot_driver_plus kinova_yolov8_openvino.py
```

**Parameters:**
- `model_type` (string, default: "hazmat"): YOLO model type
- `confidence_threshold` (double, default: 0.4): Detection threshold

**Subscribed Topics:**
- `/kinova_color` (sensor_msgs/Image): Kinova camera color image
- `/kinova_depth` (sensor_msgs/Image): Kinova camera depth image

**Published Topics:**
- `/detected_objects` (world_info_msgs/BoundingBoxArray): Object detections

#### spot_estop.py
Emergency stop functionality with multiple trigger mechanisms.

```bash
ros2 run spot_driver_plus spot_estop.py
```

**Services:**
- `/emergency_stop` (std_srvs/Trigger): Trigger emergency stop

#### get_pcl.py
Point cloud acquisition and processing utilities.

#### goal_pose_to_trajectory.py
Converts navigation goals to detailed trajectory plans.

**Subscribed Topics:**
- `/goal_pose` (geometry_msgs/PoseStamped): Target pose
- `/map` (nav_msgs/OccupancyGrid): Navigation map

**Published Topics:**
- `/trajectory` (nav_msgs/Path): Planned trajectory

#### motion_detection.py
Detects motion in camera feeds for security and monitoring.

**Subscribed Topics:**
- `/camera/image` (sensor_msgs/Image): Input camera feed

**Published Topics:**
- `/motion_detected` (std_msgs/Bool): Motion detection status

#### plan_3d_path.py
Advanced 3D path planning considering robot constraints.

**Services:**
- `/plan_3d_path` (geometry_msgs/PoseStamped): Plan 3D path to goal

#### rrl_qreader.py
QR code reading with multi-camera support.

**Subscribed Topics:**
- `/rs_*/color/image_raw` (sensor_msgs/Image): Camera feeds
- `/rs_*/aligned_depth_to_color/image_raw` (sensor_msgs/Image): Depth data

**Published Topics:**
- `/qr_codes` (world_info_msgs/BoundingBoxArray): QR code detections

#### olive_magnetic.py
Interface for magnetic sensors used in inspection tasks.

**Published Topics:**
- `/magnetic_field` (sensor_msgs/MagneticField): Magnetic sensor data

#### arduino_lights.py
Controls LED lighting systems via Arduino interface.

**Services:**
- `/set_lights` (std_srvs/SetBool): Control light state

## Launch Files

The package uses launch files from the `rrl_launchers` package:

```bash
# Full Spot system launch
ros2 launch rrl_launchers spot_driver_launch.py

# SLAM with Spot integration
ros2 launch rrl_launchers slam_launch.py
```

## Dependencies

### Hardware Requirements
- Boston Dynamics Spot robot
- Kinova Gen3 manipulator (optional)
- Intel RealSense cameras
- Arduino-compatible lighting system (optional)

### Software Dependencies

#### System Packages
```bash
sudo apt install -y \
    libpcl-dev \
    pcl-tools \
    ros-humble-pcl-ros \
    ros-humble-spot-msgs \
    ros-humble-moveit2 \
    ros-humble-control-msgs
```

#### Python Packages
```bash
pip3 install \
    ultralytics \
    opencv-python \
    numpy \
    pyserial
```

## Configuration

### YOLO Models
Place YOLO models in the `yolov8n/` directory:
```
yolov8n/
├── hazmat_openvino_model/
├── general_openvino_model/
└── custom_openvino_model/
```

### Camera Configuration
Configure camera topics in Python nodes:
```python
IMAGE_TOPICS = {
    "camera_color_frame": "/kinova_color",
}
DEPTH_IMAGE_TOPICS = {
    "camera_color_frame": "/kinova_depth",
}
```

## Usage Examples

### Object Detection with Kinova Camera
```bash
# Launch object detection
ros2 run spot_driver_plus kinova_yolov8_openvino.py

# View detections
ros2 topic echo /detected_objects
```

### Emergency Stop System
```bash
# Run emergency stop node
ros2 run spot_driver_plus spot_estop.py

# Trigger emergency stop
ros2 service call /emergency_stop std_srvs/srv/Trigger "{}"
```

### 3D Path Planning
```bash
# Launch path planner
ros2 run spot_driver_plus plan_3d_path.py

# Request path plan
ros2 service call /plan_3d_path geometry_msgs/srv/PoseStamped "{
  pose: {
    position: {x: 2.0, y: 1.0, z: 0.0},
    orientation: {w: 1.0}
  }
}"
```

### Point Cloud Processing
```bash
# Convert depth to point cloud
ros2 run spot_driver_plus depth_to_pcl

# Visualize in RViz
ros2 run rviz2 rviz2 -d config/spot_visualization.rviz
```

## Safety Features

### Emergency Stop Mechanisms
- Software emergency stop via ROS service
- Hardware emergency stop integration
- Automatic collision detection
- Battery level monitoring

### Fail-Safe Operations
- Graceful degradation on sensor failure
- Automatic recovery procedures
- Redundant safety systems

## Performance Optimization

### GPU Acceleration
Enable OpenVINO GPU acceleration:
```bash
# Check GPU availability
clinfo

# Set GPU device
export OPENVINO_DEVICE=GPU
```

### Resource Management
- Adjust detection frequency based on computational load
- Use image downsampling for improved performance
- Implement region-of-interest detection

## Troubleshooting

### Common Issues

1. **Spot connection failed**: Check network configuration and robot power
2. **YOLO model not found**: Verify model files in `yolov8n/` directory
3. **Kinova arm not responding**: Check manipulator power and calibration
4. **High CPU usage**: Enable GPU acceleration for YOLO inference

### Debug Commands
```bash
# Check Spot status
ros2 topic echo /spot/status

# Monitor detection performance
ros2 topic hz /detected_objects

# View camera feeds
ros2 run rqt_image_view rqt_image_view /kinova_color
```

### Log Analysis
```bash
# View node logs
ros2 node info /kinova_yolov8_node

# Check system resources
htop
nvidia-smi  # If using GPU
```