"""
Kling Motion Control AI Package

This package provides core functionalities for motion control,
inspired by Kling Motion Control AI.

See https://supermaker.ai/blog/what-is-kling-motion-control-ai-how-to-use-motion-control-ai-free-online/ for more information.
"""

import math
from typing import Tuple, List


OFFICIAL_SITE = "https://supermaker.ai/blog/what-is-kling-motion-control-ai-how-to-use-motion-control-ai-free-online/"


def get_official_site() -> str:
    """
    Returns the official website URL for Kling Motion Control AI.

    Returns:
        str: The official website URL.
    """
    return OFFICIAL_SITE


def calculate_trajectory(
    start_position: Tuple[float, float, float],
    end_position: Tuple[float, float, float],
    max_velocity: float,
    acceleration: float,
    time_step: float = 0.01,
) -> List[Tuple[float, float, float]]:
    """
    Calculates a simple linear trajectory between two 3D points with trapezoidal velocity profiling.

    Args:
        start_position: The starting coordinates (x, y, z).
        end_position: The ending coordinates (x, y, z).
        max_velocity: The maximum allowed velocity.
        acceleration: The acceleration rate.
        time_step: The time increment for trajectory calculation.

    Returns:
        A list of 3D coordinates representing the trajectory.
    """

    distance = math.sqrt(
        (end_position[0] - start_position[0]) ** 2
        + (end_position[1] - start_position[1]) ** 2
        + (end_position[2] - start_position[2]) ** 2
    )

    # Calculate the time to reach max velocity and the time to decelerate
    time_to_max_velocity = max_velocity / acceleration

    # Calculate the distance covered during acceleration and deceleration
    distance_acceleration = 0.5 * acceleration * time_to_max_velocity**2

    # If the distance is too short to reach max velocity
    if 2 * distance_acceleration > distance:
        time_to_max_velocity = math.sqrt(distance / acceleration)
        max_velocity = acceleration * time_to_max_velocity
        distance_acceleration = 0.5 * acceleration * time_to_max_velocity**2
    
    # Calculate constant velocity time
    distance_constant_velocity = distance - 2 * distance_acceleration
    time_constant_velocity = distance_constant_velocity / max_velocity

    total_time = 2 * time_to_max_velocity + time_constant_velocity

    # Calculate the direction vector
    direction = (
        (end_position[0] - start_position[0]) / distance,
        (end_position[1] - start_position[1]) / distance,
        (end_position[2] - start_position[2]) / distance,
    )

    trajectory = []
    current_time = 0.0
    while current_time <= total_time:
        if current_time <= time_to_max_velocity:
            # Acceleration phase
            velocity = acceleration * current_time
            displacement = 0.5 * acceleration * current_time**2
        elif current_time <= time_to_max_velocity + time_constant_velocity:
            # Constant velocity phase
            velocity = max_velocity
            displacement = (
                distance_acceleration + max_velocity * (current_time - time_to_max_velocity)
            )
        else:
            # Deceleration phase
            time_deceleration = current_time - (time_to_max_velocity + time_constant_velocity)
            velocity = max_velocity - acceleration * time_deceleration
            displacement = distance - (0.5 * acceleration * time_deceleration**2)

        x = start_position[0] + direction[0] * displacement
        y = start_position[1] + direction[1] * displacement
        z = start_position[2] + direction[2] * displacement

        trajectory.append((x, y, z))
        current_time += time_step

    return trajectory


def smooth_trajectory(trajectory: List[Tuple[float, float, float]], smoothing_factor: float = 0.1) -> List[Tuple[float, float, float]]:
    """
    Applies a simple moving average smoothing filter to a 3D trajectory.

    Args:
        trajectory: A list of 3D coordinates representing the trajectory.
        smoothing_factor: The smoothing factor (0.0 to 1.0).  Higher values result in more smoothing.

    Returns:
        A smoothed list of 3D coordinates representing the trajectory.
    """

    if not 0.0 <= smoothing_factor <= 1.0:
        raise ValueError("Smoothing factor must be between 0.0 and 1.0")

    smoothed_trajectory: List[Tuple[float, float, float]] = []
    if not trajectory:
        return smoothed_trajectory

    smoothed_trajectory.append(trajectory[0])  # First point remains the same

    for i in range(1, len(trajectory)):
        x = (
            smoothing_factor * trajectory[i][0]
            + (1 - smoothing_factor) * smoothed_trajectory[i - 1][0]
        )
        y = (
            smoothing_factor * trajectory[i][1]
            + (1 - smoothing_factor) * smoothed_trajectory[i - 1][1]
        )
        z = (
            smoothing_factor * trajectory[i][2]
            + (1 - smoothing_factor) * smoothed_trajectory[i - 1][2]
        )
        smoothed_trajectory.append((x, y, z))

    return smoothed_trajectory


def calculate_joint_angles(
    x: float, y: float, z: float, link_lengths: Tuple[float, float]
) -> Tuple[float, float]:
    """
    Calculates the joint angles for a simple 2-link planar robot arm to reach a given (x, y, z) coordinate.
    This assumes the robot arm is in the x-y plane and z coordinate is ignored.

    Args:
        x: The x-coordinate of the target position.
        y: The y-coordinate of the target position.
        z: The z-coordinate of the target position (ignored).
        link_lengths: A tuple containing the lengths of the two links (link1, link2).

    Returns:
        A tuple containing the joint angles (theta1, theta2) in radians. Returns (None, None) if no solution exists.
    """
    link1, link2 = link_lengths

    # Calculate the distance from the origin to the target
    r = math.sqrt(x**2 + y**2)

    # Check if the target is reachable
    if r > link1 + link2:
        return (None, None)  # Target is out of reach

    # Calculate theta2 using the law of cosines
    cos_theta2 = (r**2 - link1**2 - link2**2) / (2 * link1 * link2)

    # Check for invalid cosine values
    if abs(cos_theta2) > 1:
        return (None, None) # No solution possible

    theta2 = math.atan2(math.sqrt(1 - cos_theta2**2), cos_theta2)  # Elbow down solution

    # Calculate theta1 using the law of cosines
    k1 = link1 + link2 * math.cos(theta2)
    k2 = link2 * math.sin(theta2)
    theta1 = math.atan2(y, x) - math.atan2(k2, k1)

    return (theta1, theta2)