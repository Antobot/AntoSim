import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Locate your Xacro file
    xacro_file = os.path.join(
        get_package_share_directory('antobot_sim_description'),
        'urdf',
        'ant_v4.urdf.xacro'
    )

    # Process Xacro to URDF
    doc = xacro.process_file(xacro_file)
    urdf_content = doc.toxml()

    return LaunchDescription([
        
        Node( package='ros_gz_sim', executable='create', arguments=[
                    '-name', 'antobot_ant',
                    '-topic', 'robot_description',
                    '-x', '0.0',
                    '-z', '0.3',
                    '-y', '0.0',
                    ],
                output='screen'),
    ])


