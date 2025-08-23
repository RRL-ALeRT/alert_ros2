# World Info Package

The `world_info` package provides comprehensive perception capabilities for robotic systems, including object detection, QR code reading, ArUco marker detection, and hazmat detection.

## Features

- **QR Code Detection**: Real-time QR code detection and decoding with OpenVINO acceleration
- **ArUco Marker Detection**: Precise pose estimation using ArUco markers
- **Hazmat Detection**: AI-powered hazardous material detection using YOLO models
- **Multi-Camera Support**: Synchronized processing across multiple Intel RealSense cameras
- **GPU Acceleration**: OpenVINO GPU acceleration for improved performance

## Nodes

### world_info
Main world understanding node that aggregates and processes detection results.

**Published Topics:**
- `/world_objects` (world_info_msgs/BoundingBoxArray): Detected objects with spatial information

### DetectQR (Component)
QR code detection component with OpenVINO acceleration.

**Parameters:**
- `frame_id` (string): Camera frame identifier
- `confidence_threshold` (double, default: 0.7): Minimum detection confidence

**Subscribed Topics:**
- `/camera/color/image_raw` (sensor_msgs/Image): Input color image
- `/camera/aligned_depth_to_color/image_raw` (sensor_msgs/Image): Aligned depth image
- `/camera/color/camera_info` (sensor_msgs/CameraInfo): Camera calibration

**Published Topics:**
- `/qr_detections` (world_info_msgs/BoundingBoxArray): QR code detections

### DetectAruco (Component)
ArUco marker detection for precise localization.

**Parameters:**
- `aruco_square_length` (double, default: 0.3): ArUco marker size in meters

**Subscribed Topics:**
- `/image_rect` (sensor_msgs/Image): Rectified input image

**Published Topics:**
- `/aruco_detections` (world_info_msgs/BoundingBoxArray): ArUco marker detections

### DetectHazmat (Component)
Hazardous material detection using YOLO models.

**Parameters:**
- `hazmat_confidence_threshold` (double, default: 0.9): Detection confidence threshold
- `inference_mode` (string, default: "GPU"): Inference device ("CPU" or "GPU")
- `frame_id` (string): Camera frame identifier

**Subscribed Topics:**
- `/camera/color/image_raw` (sensor_msgs/Image): Input color image
- `/camera/aligned_depth_to_color/image_raw` (sensor_msgs/Image): Aligned depth image
- `/camera/color/camera_info` (sensor_msgs/CameraInfo): Camera calibration

**Published Topics:**
- `/hazmat_detections` (world_info_msgs/BoundingBoxArray): Hazmat detections

## Launch Files

### tag_detectors_launch.py
Comprehensive launch file that starts multiple detection components.

```bash
ros2 launch world_info tag_detectors_launch.py
```

**Launched Components:**
- QR detection for front, left, and right cameras
- Hazmat detection for all cameras
- ArUco detection (commented out by default)

## Usage Examples

### Basic QR Code Detection
```bash
# Launch QR detection for all cameras
ros2 launch world_info tag_detectors_launch.py

# View detections
ros2 topic echo /qr_detections
```

### Hazmat Detection with Custom Threshold
```bash
# Launch with custom confidence threshold
ros2 launch world_info tag_detectors_launch.py hazmat_confidence_threshold:=0.8
```

### Single Camera Setup
```bash
# Launch individual detection component
ros2 run world_info aruco_node --ros-args -p aruco_square_length:=0.2
```

## Configuration

### Camera Frame IDs
The package supports multiple camera configurations:
- `rs_front`: Front-facing camera
- `rs_left`: Left-side camera  
- `rs_right`: Right-side camera

### Detection Thresholds
Adjust confidence thresholds based on your environment:
- **QR Codes**: 0.7 (default) - increase for noisy environments
- **Hazmat**: 0.9 (default) - decrease for better recall
- **ArUco**: Fixed threshold based on marker detection algorithm

## Dependencies

### System Dependencies
```bash
sudo apt install libzbar-dev libeigen3-dev libopencv-dev
```

### ROS 2 Dependencies
- `rclcpp`
- `rclcpp_components`
- `world_info_msgs`
- `sensor_msgs`
- `cv_bridge`
- `image_transport`
- `tf2_ros`

### Python Dependencies
```bash
pip3 install ultralytics qreader-openvino
```

## Performance Optimization

### GPU Acceleration
Enable GPU inference for better performance:
```bash
ros2 launch world_info tag_detectors_launch.py inference_mode:=GPU
```

### Camera Resolution
Reduce camera resolution for improved performance:
- 640x480 for basic detection
- 1280x720 for detailed analysis
- 1920x1080 for maximum accuracy

## Troubleshooting

### Common Issues

1. **QR codes not detected**: Check lighting conditions and QR code size
2. **GPU inference fails**: Verify OpenVINO GPU drivers are installed
3. **High CPU usage**: Switch to GPU inference mode
4. **Camera sync issues**: Check camera timestamps and frame rates

### Debug Commands
```bash
# Check detection topics
ros2 topic list | grep detection

# Monitor detection rates
ros2 topic hz /qr_detections

# View camera feeds
ros2 run rqt_image_view rqt_image_view /rs_front/color/image_raw
```