import os
import xacro
import yaml

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from antobot_com_postgresql.db_config_loader import get_robot_config

def dict_to_xacro_args(data_dict, prefix=""):
    args = {}
    for key, value in data_dict.items():
        full_key = f"{prefix}{key}" if prefix else key
        
        if isinstance(value, dict):
            args.update(dict_to_xacro_args(value, prefix=f"{full_key}_"))
        elif isinstance(value, bool):
            args[full_key] = str(value).lower()
        elif value is None:
            continue
        else:
            args[full_key] = str(value)
    
    return args

def generate_launch_description():
    
    packagePath = get_package_share_directory('antobot_description')
    platform_config_path = os.path.join(packagePath, 'config', 'platform_config.yaml')
    data = get_robot_config("platform_config", platform_config_path)

    robot_platform = data['robot_platform']
    if robot_platform == "ant":
        model_xacro = 'ant_v4.urdf.xacro'
        starting_height = '0.3'
    elif robot_platform == "allWheel":
        model_xacro = 'allWheel.urdf.xacro'
        starting_height = '1.5'
    
    # Locate your Xacro file
    xacro_file = os.path.join(packagePath,'urdf', model_xacro)

    # Convert database config to xacro arguments
    xacro_args = dict_to_xacro_args(data)
    
    # Process Xacro to URDF with database parameters
    doc = xacro.process_file(xacro_file, mappings=xacro_args)
    urdf_content = doc.toxml()

    return LaunchDescription([
        
        Node( package='ros_gz_sim', executable='create', arguments=[
                    '-name', 'antobot_ant',
                    '-topic', 'robot_description',
                    '-x', '0.0',
                    '-z', starting_height,
                    '-y', '0.0',
                    '-R', '0.0',
                    '-P', '0.0',
                    '-Y', '3.1416'
                    ],
                output='screen'),
    ])


