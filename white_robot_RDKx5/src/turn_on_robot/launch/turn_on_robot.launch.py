import os
from pathlib import Path
import launch
from launch.actions import SetEnvironmentVariable
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, GroupAction,
                            IncludeLaunchDescription, SetEnvironmentVariable)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import PushRosNamespace
import launch_ros.actions
from launch.conditions import UnlessCondition

def generate_launch_description():
    # Get the launch directory
    bringup_dir = get_package_share_directory('turn_on_robot') #get_package_share_directory：获取功能包的绝对路径（如turn_on_wheeltec_robot）
    launch_dir = os.path.join(bringup_dir, 'launch')
    ekf_config = Path(get_package_share_directory('turn_on_robot'), 'config', 'ekf.yaml')

    
    carto_slam = LaunchConfiguration('carto_slam', default='false')#LaunchConfiguration：动态获取参数值（如条件判断）
    carto_slam_dec = DeclareLaunchArgument('carto_slam',default_value='false')#DeclareLaunchArgument：声明可在命令行覆盖的启动参数（如carto_slam）


    #启动其他launch文件——使用如下函数 
    #IncludeLaunchDescription：嵌套其他launch文件（模块化启动配置）         
    wheeltec_robot = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'base_serial.launch.py')),
            launch_arguments={'akmcar': 'false'}.items(),
    )    

    #choose your car,the default car is mini_mec 
    choose_car = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'robot_mode_description.launch.py')),
    )

    
    base_to_link = launch_ros.actions.Node(
            package='tf2_ros', 
            executable='static_transform_publisher', 
            name='base_to_link',
            arguments=['0', '0', '0','0', '0','0','base_footprint','base_link'],
    )
    base_to_gyro = launch_ros.actions.Node(
            package='tf2_ros', 
            executable='static_transform_publisher', 
            name='base_to_gyro',
            arguments=['0', '0', '0','0', '0','0','base_footprint','gyro_link'],
    )

    robot_ekf = launch_ros.actions.Node(
            condition=UnlessCondition(carto_slam),  #UnlessCondition：条件触发器（当条件为False时执行）
            package='robot_localization', 
            executable='ekf_node', 
            parameters=[ekf_config],
            remappings=[("odometry/filtered", "odom_combined")]  #话题重映射​​：将输出话题从/odometry/filtered改为/odom_combined（适配现有系统）
            )
                              
    joint_state_publisher_node = launch_ros.actions.Node(
            package='joint_state_publisher', 
            executable='joint_state_publisher', 
            name='joint_state_publisher',
    )

    ld = LaunchDescription()

    ld.add_action(carto_slam_dec)   # 参数声明
    ld.add_action(wheeltec_robot)    # 底盘驱动
    ld.add_action(base_to_link)    # TF: base_footprint → base_link
    ld.add_action(base_to_gyro)    # TF: base_footprint → gyro_link
    ld.add_action(joint_state_publisher_node)    # 关节状态
    ld.add_action(choose_car)      # 机器人模型
    ld.add_action(robot_ekf)      # EKF定位（条件启动）

    return ld

