import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
from rclpy.serialization import deserialize_message
from std_msgs.msg import Float64


# Location of our ROS Bag recording
bag_folder = Path.home() / "ros2_ws/recordings/bonus1_trial"

# Find the SQLite database
db_files = list(bag_folder.glob("*.db3"))

if not db_files:
    raise FileNotFoundError("No .db3 recording found!")

connection = sqlite3.connect(db_files[0])

# Retrieve topic IDs
topics = dict(
    connection.execute("SELECT name, id FROM topics")
)

imu_id = topics["/imu_radius"]
odom_id = topics["/odom_radius"]

# Read the recorded measurements
rows = connection.execute(
    "SELECT topic_id, timestamp, data "
    "FROM messages ORDER BY timestamp"
).fetchall()

connection.close()

if not rows:
    raise ValueError("The recording contains no messages.")

start_time = rows[0][1]

imu_time = []
imu_radius = []

odom_time = []
odom_radius = []

for topic_id, timestamp, data in rows:

    time = (timestamp - start_time) / 1e9

    msg = deserialize_message(data, Float64)

    if topic_id == imu_id:
        imu_time.append(time)
        imu_radius.append(msg.data)

    elif topic_id == odom_id:
        odom_time.append(time)
        odom_radius.append(msg.data)


# Find when the IMU estimate first reaches 10 m
stop_time = None

for t, r in zip(imu_time, imu_radius):
    if r >= 10.0:
        stop_time = t
        break

if stop_time is None:
    raise ValueError("IMU radius never reached 10 m.")


# Create the graph
plt.figure(figsize=(11, 6))

plt.plot(
    imu_time,
    imu_radius,
    label="IMU-estimated radius"
)

plt.plot(
    odom_time,
    odom_radius,
    label="Odometry-based radius"
)

plt.axhline(
    y=10,
    color="red",
    linestyle="--",
    label="10 m stopping threshold"
)

plt.axvline(
    x=stop_time,
    color="gray",
    linestyle=":",
    label="Stopping instant"
)

plt.xlabel("Time elapsed (s)")
plt.ylabel("Radial distance (m)")

plt.title("IMU vs Odometry: Radial Distance Estimation")

plt.xlim(0, stop_time + 1)
plt.ylim(0, 12)

plt.legend()
plt.grid(True)
plt.tight_layout()

# Save our graph
output = Path(__file__).resolve().parent / "imu_vs_odom.png"

plt.savefig(output, dpi=300)

plt.show()

print(f"Graph saved to: {output}")