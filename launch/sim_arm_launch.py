import launch
import launch_ros.actions
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        Node(
            package='arm_dashboard',
            executable='sim_arm',
            name='sim_arm'
            ),
        Node(
            package='arm_dashboard',
            executable='viewer',
            name='viewer'
            )

        ])
