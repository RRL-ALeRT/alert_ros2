# ALeRT ROS2 - Autonomous Robot Perception and Navigation System

A comprehensive ROS 2 workspace for autonomous robotics applications featuring SLAM, object detection, and Boston Dynamics Spot robot integration. This system provides advanced perception capabilities including QR code detection, hazmat detection, ArUco markers, and real-time mapping for autonomous navigation.

## Overview

This repository contains several ROS 2 packages that work together to provide:

- **SLAM and Mapping**: Real-time simultaneous localization and mapping using Hector SLAM and SLAM Toolbox
- **Object Detection**: YOLOv8/YOLOv5 with OpenVINO acceleration for hazmat detection and general object recognition
- **Marker Detection**: QR codes and ArUco markers for localization and navigation waypoints
- **Robot Integration**: Boston Dynamics Spot robot driver with additional features
- **Geotiff Generation**: Automated map export functionality for GIS applications
- **Multi-Camera Support**: Intel RealSense camera integration with synchronized data processing

## Packages

### Core Packages

- **`world_info`**: Object detection, QR code reading, ArUco markers, and world understanding
- **`spot_driver_plus`**: Enhanced Boston Dynamics Spot robot driver with additional perception features
- **`rrl_launchers`**: Launch configurations for various SLAM, mapping, and navigation scenarios

### Mapping and SLAM Packages (Modified from Hector SLAM)

- **`hector_geotiff`**: Geotiff map generation and export functionality
- **`hector_map_tools`**: Map processing utilities and tools
- **`hector_marker_drawing`**: Visualization and marker drawing capabilities

## Installation

### Prerequisites

- **Ubuntu 20.04/22.04**
- **ROS 2 Humble** (recommended) or Galactic
- **Python 3.8+**

### System Dependencies

```bash
# Essential dependencies
sudo apt update
sudo apt install -y \
    libzbar-dev \
    libeigen3-dev \
    libopencv-dev \
    ros-humble-cv-bridge \
    ros-humble-image-transport \
    ros-humble-tf2-ros \
    ros-humble-slam-toolbox \
    ros-humble-navigation2 \
    ros-humble-realsense2-camera

# For QR code detection
sudo apt install libzbar-dev
```

### Intel RealSense SDK (Required for camera support)

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main"
sudo apt update
sudo apt install librealsense2-dkms librealsense2-utils librealsense2-dev
```

### Intel OpenVINO (For GPU-accelerated object detection)

**Why OpenVINO?** Provides significant performance improvements for object detection on Intel integrated GPUs. See: [Running OpenVINO on Intel GPU](https://learnopencv.com/running-openvino-models-on-intel-integrated-gpu)

#### Intel GPU Setup
Follow the [Intel GPU installation guide](https://dgpu-docs.intel.com/installation-guides/ubuntu/ubuntu-jammy-arc.html) for GPU compute support.

#### OpenVINO Installation
```bash
cd ~
wget https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3/linux/l_openvino_toolkit_ubuntu20_2022.3.0.9052.9752fafe8eb_x86_64.tgz
tar -xvzf l_openvino_toolkit_ubuntu20_2022.3.0.9052.9752fafe8eb_x86_64.tgz
rm l_openvino_toolkit_ubuntu20_2022.3.0.9052.9752fafe8eb_x86_64.tgz
mv l_openvino_toolkit_ubuntu20_2022.3.0.9052.9752fafe8eb_x86_64 openvino2022.3
. ~/openvino2022.3/setupvars.sh
echo '
#OpenVINO
. ~/openvino2022.3/setupvars.sh > /dev/null' >> ~/.bashrc
```

### Python Dependencies

```bash
# Install ultralytics for YOLO models
pip3 install ultralytics

# Install QReader for QR code detection with OpenVINO acceleration
git clone https://github.com/RRL-ALeRT/QReader_openvino
cd QReader_openvino
pip3 install -e .
```

### Building the Workspace

```bash
# Clone the repository
git clone https://github.com/RRL-ALeRT/alert_ros2.git
cd alert_ros2

# Source ROS 2
source /opt/ros/humble/setup.bash

# Build the workspace
colcon build --symlink-install

# Source the workspace
source install/setup.bash
```

## Usage

### Quick Start - SLAM and Mapping

```bash
# Terminal 1: Launch SLAM system
ros2 launch rrl_launchers slam_launch.py

# Terminal 2: Launch perception system
ros2 launch world_info tag_detectors_launch.py

# Terminal 3: Launch trajectory server (optional)
ros2 run hector_trajectory_server hector_trajectory_server
```

### Object Detection and Perception

```bash
# Launch hazmat detection with multiple cameras
ros2 launch world_info tag_detectors_launch.py

# Run YOLOv8 object detection with OpenVINO
ros2 run spot_driver_plus kinova_yolov8_openvino.py
```

### Geotiff Map Generation

```bash
# Real-time geotiff generation with SLAM
ros2 run hector_geotiff geotiff_node

# One-time map saving with SLAM Toolbox
ros2 run hector_geotiff geotiff_saver
```

### Boston Dynamics Spot Integration

```bash
# Launch Spot driver
ros2 launch rrl_launchers spot_driver_launch.py

# Emergency stop functionality
ros2 run spot_driver_plus spot_estop.py
```

### Available Launch Configurations

- **`slam_launch.py`**: Complete SLAM system with mapping and perception
- **`nav2_launch.py`**: Navigation stack with autonomous path planning
- **`realsenses_launch.py`**: Multi-camera RealSense configuration
- **`cartographer2d_launch.py`**: Google Cartographer 2D SLAM
- **`rtabmap_launch.py`**: RTAB-Map RGB-D SLAM
- **`occupancy_grid_launch.py`**: Occupancy grid mapping

## Topics and Services

### Key Topics

- **Camera Feeds**: `/rs_front/color/image_raw`, `/rs_left/color/image_raw`, `/rs_right/color/image_raw`
- **Depth Data**: `/rs_*/aligned_depth_to_color/image_raw`
- **Object Detection**: `/detected_objects`, `/hazmat_detections`
- **QR Codes**: `/qr_detections`
- **Map Data**: `/map`, `/geotiff_map`

### Services

- **Map Saving**: `/save_map`
- **Emergency Stop**: `/spot/emergency_stop`
- **Path Planning**: `/plan_path`

## Configuration

Configuration files are located in the `config/` directories of each package:

- **SLAM Parameters**: `rrl_launchers/config/mapper_params_online_async.yaml`
- **Camera Calibration**: Individual camera parameter files
- **Detection Thresholds**: Configurable confidence thresholds for object detection

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.

## Maintainers

- **Max Kirsch** - m.kirsch@fh-aachen.de
- **Sanket Pawar** - skpawar1305@gmail.com

## Related Projects

- [Hector SLAM](http://wiki.ros.org/hector_slam) - Original SLAM implementation
- [QReader OpenVINO](https://github.com/RRL-ALeRT/QReader_openvino) - Accelerated QR code detection

## Troubleshooting

### Common Issues

1. **OpenVINO not found**: Ensure OpenVINO environment is sourced in `~/.bashrc`
2. **Camera not detected**: Check RealSense installation and USB permissions
3. **Build failures**: Verify all ROS 2 dependencies are installed

### Performance Optimization

- Use GPU inference mode for object detection when available
- Adjust confidence thresholds based on your use case
- Consider reducing image resolution for improved performance
