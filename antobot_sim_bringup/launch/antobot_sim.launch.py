import os
import xacro

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, GroupAction
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node



########################################################################

# Launch gazebo
def gazebo_launch(context, *args, **kwargs):

    # Path

    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_antobot_sim_gazebo = get_package_share_directory('antobot_sim_gazebo')

    # Setup to launch the simulator and Gazebo world
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': PathJoinSubstitution([
            pkg_antobot_sim_gazebo,
            'worlds',
            'lboro_nfl.sdf'
        ])}.items(),
    )

    return [gz_sim]



########################################################################





########################################################################

def generate_launch_description():
    
    # Configure ROS nodes for launch
    ld = LaunchDescription()


    # Setup project paths
    pkg_antobot_sim_bringup = get_package_share_directory('antobot_sim_bringup')




    ## Simulation Robot Launch -------------------------------------------------------------
    #parseAntobotLaunch = PathJoinSubstitution([pkg_antobot_sim_bringup, 'launch', 'parseAntobot.launch.py'])
    #antobotParse = IncludeLaunchDescription(PythonLaunchDescriptionSource([parseAntobotLaunch]))

    pkg_antobot_sim_description = get_package_share_directory('antobot_sim_description')


    # Locate your Xacro file
    xacro_file = os.path.join(pkg_antobot_sim_description,'urdf','ant_v4.urdf.xacro')

    # Process Xacro to URDF
    doc = xacro.process_file(xacro_file)
    urdf_content = doc.toxml()

    # Takes the description and joint angles as inputs and publishes the 3D poses of the robot links
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': urdf_content},
        ]
    )






    # Load the SDF file from "description" package
    #sdf_file  =  os.path.join(pkg_antobot_sim_description, 'models', 'diff_drive', 'model.sdf')
    #with open(sdf_file, 'r') as infp:
    #    robot_desc = infp.read()




    # Visualize in RViz
    rviz = Node(
       package='rviz2',
       executable='rviz2',
       arguments=['-d', os.path.join(pkg_antobot_sim_bringup, 'config', 'diff_drive.rviz')],
       condition=IfCondition(LaunchConfiguration('rviz'))
    )

    # Bridge ROS topics and Gazebo messages for establishing communication
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(pkg_antobot_sim_bringup, 'config', 'antobot_gazebo_bridge.yaml'),
            'qos_overrides./tf_static.publisher.durability': 'transient_local',
        }],
        output='screen',
    )

        



    ld.add_action(DeclareLaunchArgument('use_sim_time', default_value='true',choices=['true', 'false'],description='use_sim_time'))
    ld.add_action(OpaqueFunction(function=gazebo_launch))
    ld.add_action(robot_state_publisher)
    ld.add_action(bridge)
    ld.add_action(DeclareLaunchArgument('rviz', default_value='true',description='Open RViz.'))
    ld.add_action(rviz)



    parseAntobotLaunch = PathJoinSubstitution([pkg_antobot_sim_bringup, 'launch', 'parseAntobot.launch.py'])

    antobotParse = IncludeLaunchDescription(PythonLaunchDescriptionSource([parseAntobotLaunch]))

    ld.add_action(antobotParse)


    return ld