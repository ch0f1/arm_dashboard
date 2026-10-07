import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'arm_dashboard'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='chof1',
    maintainer_email='jisragz@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sim_arm = arm_dashboard.brazo_virtual:main',
            'viewer = arm_dashboard.viewer:main',
            'keys_controller = arm_dashboard.keys:main',
            'coords_controller = arm_dashboard.teleop_coords:main',
        ],
    },
)
