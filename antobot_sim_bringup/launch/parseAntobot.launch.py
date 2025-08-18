import os
import xacro
import yaml

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    pkg_antobot_description = get_package_share_directory('antobot_description')
    platform_config_path = str(pkg_antobot_description) + "/config/platform_config.yaml"

    with open(platform_config_path, 'r') as yamlfile:
        data = yaml.safe_load(yamlfile)

        robot_platform = data['robot_platform']
        if robot_platform == "ant":
            model_xacro = 'ant_v4.urdf.xacro'
            starting_height = '0.3'
        elif robot_platform == "allWheel":
            model_xacro = 'allWheel.urdf.xacro'
            starting_height = '1.5'
    
    # Locate your Xacro file
    xacro_file = os.path.join(pkg_antobot_description,'urdf', model_xacro)

    # Process Xacro to URDF
    doc = xacro.process_file(xacro_file)
    urdf_content = doc.toxml()

    return LaunchDescription([
        
        Node( package='ros_gz_sim', executable='create', arguments=[
                    '-name', 'antobot_ant',
                    '-topic', 'robot_description',
                    '-x', '0.0',
                    '-z', starting_height,
                    '-y', '0.0',
                    ],
                output='screen'),
    ])


