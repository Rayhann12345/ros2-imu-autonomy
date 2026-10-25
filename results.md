# Experimental Results

## IMU-Based Autonomous Stopping at 10 m

The robot was commanded to move at 0.2 m/s and stop
when its IMU-estimated radial distance reached 10 m.

| Trial | IMU Estimate (m) | Odometry Distance (m) | Stopping Error (m) |
|-------|------------------|----------------------|--------------------|
| 1     | 10.072           | 4.617                | -5.383             |
| 2     | 10.065           | 4.658                | -5.342             |
| 3     | 10.082           | 4.638                | -5.362             |

## Average Results

- Mean IMU-estimated radius: 10.073 m
- Mean odometry-based distance: 4.638 m
- Mean stopping error: -5.362 m
- Mean percentage shortfall: 53.62%

## Observations

1. The robot successfully stopped automatically in all three trials.
2. The IMU consistently overestimated displacement.
3. The stationary IMU reported an approximately -0.06 m/s²
   acceleration offset along the x-axis.
4. The estimated x-velocity exhibited negative drift.
5. The results suggest a significant systematic error component,
   potentially caused by sensor bias or gravitational projection.
6. Odometry was used only for evaluation, not for stopping decisions.

## Limitations

The estimator integrates raw IMU acceleration without
bias compensation or orientation correction.

Wheel odometry is used as an independent reference,
not as exact ground truth.