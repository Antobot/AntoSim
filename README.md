# ROS 2 Gazebo simulator


Designed for use with Gazebo Fortress (6.16) and ROS2 Humble.

### Install

 
1. Install dependencies

    ```bash
    sudo apt install python3-vcstool python3-colcon-common-extensions git wget
    cd ~
    mkdir anto_ws
    cd ~/anto_ws
    source /opt/ros/humble/setup.bash
    sudo rosdep init
    rosdep update
    rosdep install --from-paths src --ignore-src -r -i -y --rosdistro <ROS_DISTRO>
    ```

1. Build the project

    ```bash
    colcon build --cmake-args -DBUILD_TESTING=ON
    ```

1. Source the workspace

    ```bash
    . ~/anto_ws/install/setup.sh
    ```

1. Launch the simulation

    ```bash
    ros2 launch antobot_sim_bringup antobot_sim.launch.py
    ```

1. For teleop:

    ```bash
        ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/antobot_ant/cmd_vel
    ```



Based on the gazebo sim [example project](https://github.com/gazebosim/ros_gz_project_template/tree/fortress).
