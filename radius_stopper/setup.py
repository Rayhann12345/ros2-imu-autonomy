from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'radius_stopper'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Rayhann12345',
    maintainer_email='rehansharief258@gmail.com',
    description='ROS 2 node for autonomous robot stopping using IMU-based position estimation',
    license='All rights reserved',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'radius_stopper = radius_stopper.radius_stopper:main',
        ],
    },
)
