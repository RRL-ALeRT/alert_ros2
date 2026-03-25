# Contributing to ALeRT ROS2

We welcome contributions to the ALeRT ROS2 project! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bug fix
4. Make your changes
5. Test your changes thoroughly
6. Submit a pull request

## Development Setup

### Prerequisites

- Ubuntu 20.04/22.04
- ROS 2 Humble
- All dependencies listed in the main README.md

### Environment Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/alert_ros2.git
cd alert_ros2

# Source ROS 2
source /opt/ros/humble/setup.bash

# Build the workspace
colcon build --symlink-install

# Source the workspace
source install/setup.bash
```

## Code Style Guidelines

### C++

- Follow ROS 2 C++ style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Include proper header documentation

### Python

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Include docstrings for functions and classes
- Add comments for complex logic

### Launch Files

- Use descriptive parameter names
- Include comments explaining configuration options
- Group related nodes logically

## Testing

### Before Submitting

1. Build the entire workspace: `colcon build`
2. Test your changes with relevant launch files
3. Verify no new warnings or errors are introduced
4. Test on actual hardware when possible

### Testing Checklist

- [ ] Code builds without errors or warnings
- [ ] Launch files work as expected
- [ ] No regressions in existing functionality
- [ ] New features work as documented
- [ ] Performance impact is acceptable

## Commit Guidelines

### Commit Messages

Use clear, descriptive commit messages following this format:

```
[package_name]: Brief description of change

Longer description explaining what changed and why,
if necessary.

Fixes #issue_number (if applicable)
```

Examples:
```
world_info: Add hazmat detection confidence threshold parameter

Added configurable confidence threshold for hazmat detection to allow
tuning for different environments and use cases.

spot_driver_plus: Fix depth image processing for Kinova arm

Resolved issue where depth images were not properly synchronized
with color images during object manipulation tasks.
```

### Branch Naming

Use descriptive branch names:
- `feature/add-new-detection-algorithm`
- `bugfix/fix-camera-calibration`
- `improvement/optimize-slam-performance`

## Pull Request Process

1. **Create a Pull Request** with a clear title and description
2. **Link related issues** using "Fixes #issue_number"
3. **Describe your changes** including what was changed and why
4. **Add testing information** describing how you tested the changes
5. **Request review** from maintainers

### Pull Request Template

When creating a pull request, include:

```
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Performance improvement
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tested with simulation
- [ ] Tested with real hardware
- [ ] All existing tests pass
- [ ] New tests added (if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated (if applicable)
- [ ] No new warnings introduced

## Related Issues
Fixes #(issue number)
```

## Package-Specific Guidelines

### world_info
- Ensure new detection algorithms are properly parameterized
- Test with various confidence thresholds
- Verify performance on both CPU and GPU inference

### spot_driver_plus
- Test integration with Boston Dynamics Spot hardware
- Ensure emergency stop functionality is maintained
- Verify manipulation tasks work correctly

### rrl_launchers
- Test new launch files thoroughly
- Ensure parameter documentation is complete
- Verify compatibility with different hardware configurations

## Documentation

### When to Update Documentation

- Adding new features or capabilities
- Changing existing APIs or parameters
- Adding new dependencies or requirements
- Modifying installation procedures

### Documentation Standards

- Update README.md for major changes
- Include inline code comments
- Update launch file parameter documentation
- Add examples for new features

## Getting Help

If you need help or have questions:

1. Check existing issues and documentation
2. Open a new issue with the "question" label
3. Contact maintainers directly:
   - Max Kirsch: m.kirsch@fh-aachen.de
   - Sanket Pawar: skpawar1305@gmail.com

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and improve
- Maintain a positive community environment

Thank you for contributing to ALeRT ROS2!