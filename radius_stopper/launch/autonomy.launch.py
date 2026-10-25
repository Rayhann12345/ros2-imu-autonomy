import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    turtlebot3_gazebo_dir = get_package_share_directory(
        'turtlebot3_gazebo'
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                turtlebot3_gazebo_dir,
                'launch',
                'empty_world.launch.py'
            )
        )
    )

    radius_stopper_node = Node(
        package='radius_stopper',
        executable='radius_stopper',
        name='radius_stopper',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        SetEnvironmentVariable(
            name='TURTLEBOT3_MODEL',
            value='burger'
        ),
        gazebo_launch,
        radius_stopper_node
    ])