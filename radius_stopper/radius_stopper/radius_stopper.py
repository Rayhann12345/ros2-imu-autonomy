import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from rclpy.qos import qos_profile_sensor_data
import math
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64


class RadiusStopper(Node):
    def __init__(self):
        super().__init__('radius_stopper')

        self.imu_sub = self.create_subscription(
            Imu,
            '/imu',
            self.imu_callback,
            qos_profile_sensor_data
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry, 
            '/odom', 
            self.odom_callback, 
            10
        )

        self.imu_radius_pub = self.create_publisher(
            Float64, 
            '/imu_radius', 
            10
        )

        self.odom_radius_pub = self.create_publisher(
            Float64, 
            '/odom_radius', 
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        self.vx = 0.0
        self.vy = 0.0

        self.x = 0.0
        self.y = 0.0

        self.odom_x0 = None
        self.odom_y0 = None
        self.odom_radius = None

        self.last_time = None

        self.stopped = False

        self.declare_parameter('stop_radius',10.0)
        self.stop_radius = self.get_parameter('stop_radius').value

    def imu_callback(self, msg):
        ax = msg.linear_acceleration.x
        ay = msg.linear_acceleration.y
        az = msg.linear_acceleration.z

       #self.get_logger().info(
        #    f'Acceleration: x={ax:.3f}, y={ay:.3f}, z={az:.3f}'
        #)

        current_time = (msg.header.stamp.sec +
                        msg.header.stamp.nanosec * 1e-9
        )

        if self.last_time is None:
            self.last_time = current_time
            return

        dt = current_time - self.last_time
        self.last_time = current_time

        if dt <= 0:
            return

        self.x += self.vx * dt + 0.5 * ax * (dt ** 2)
        self.y += self.vy * dt + 0.5 * ay * (dt ** 2)

        self.vx += ax * dt
        self.vy += ay * dt

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        if self.odom_x0 is None:
            self.odom_x0 = x
            self.odom_y0 = y

        self.odom_radius = math.hypot(
            x - self.odom_x0,
            y - self.odom_y0
        )

    def control_loop(self):

        r = math.hypot(self.x, self.y)

        imu_msg = Float64()
        imu_msg.data = r
        self.imu_radius_pub.publish(imu_msg)

        if self.odom_radius is not None:
            odom_msg = Float64()
            odom_msg.data = self.odom_radius
            self.odom_radius_pub.publish(odom_msg)

        if not self.stopped and r >= self.stop_radius:
            self.stopped = True
            self.get_logger().info(
                f'STOP TRIGGERED! Estimated radius = {r:.3f} m'
            )

        cmd = Twist()

        if self.stopped:
            cmd.linear.x = 0.0
        else:
            cmd.linear.x = 0.2

        cmd.angular.z = 0.0

        self.cmd_pub.publish(cmd)

        self.get_logger().info(
            f'x={self.x:.3f}, y={self.y:.3f}, '
            f'vx={self.vx:.3f}, vy={self.vy:.3f}, '
            f'r={r:.3f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = RadiusStopper()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()