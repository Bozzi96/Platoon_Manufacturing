# -*- coding: utf-8 -*-
"""
potential_field_controller.py

This module implements a potential field controller for path planning. It provides functions to calculate the attractive and repulsive forces, compute the total force, and convert the force to speed on the x and y axes.

Functions:
    potential_field_controller(target_position, current_position, obstacles):
        Implements a potential field controller and returns the total force and angle.
    
    calculate_attractive_force(target_position, current_position, gain=1):
        Calculates the attractive force towards the target position.
    
    calculate_repulsive_force(current_position, obstacles, gain=100, safe_distance=1):
        Calculates the repulsive force from the obstacles.
    
    convert_force_to_speed(force, mass, time_interval):
        Converts the force to speed on the x and y axes.

"""

import math
tolerance = 0.1  # Small positive tolerance value

def potential_field_controller(target_position, current_position, obstacles, moving_obstacles):
    """
    Implements a potential field controller and returns the total force and angle.

    Args:
        target_position (tuple): The target position (x, y) to navigate towards.
        current_position (tuple): The current position (x, y) of the object.
        obstacles (list): A list of obstacle positions [(x1, y1), (x2, y2), ...].

    Returns:
        tuple: A tuple containing the total force (force_x, force_y) and the angle (in radians).
    """
    attractive_force = calculate_attractive_force(target_position, current_position, gain=2)
    repulsive_force = calculate_repulsive_force_moving_obstacles(current_position, obstacles, moving_obstacles, \
																 safe_distance=50, static_gain=500, dynamic_gain=150)
    total_force = ((attractive_force[0] + repulsive_force[0]), (attractive_force[1] + repulsive_force[1]))
    angle = math.atan2(total_force[1], total_force[0])

    return total_force[0], total_force[1]


def calculate_attractive_force(target_position, current_position, gain=1):
    """
    Calculates the attractive force towards the target position.

    Args:
        target_position (tuple): The target position (x, y) to navigate towards.
        current_position (tuple): The current position (x, y) of the object.
        gain (float, optional): The gain factor for attractive force. Defaults to 1.

    Returns:
        tuple: A tuple containing the attractive force components (force_x, force_y).
    """
    dx = target_position[0] - current_position[0]
    dy = target_position[1] - current_position[1]
    distance = math.sqrt(dx**2 + dy**2)

    force_x = gain * dx / distance
    force_y = gain * dy / distance

    return force_x, force_y


def calculate_repulsive_force(current_position, obstacles, gain=100, safe_distance=1):
    """
    Calculates the repulsive force from the obstacles.

    Args:
        current_position (tuple): The current position (x, y) of the object.
        obstacles (list): A list of obstacle positions [(x1, y1), (x2, y2), ...].
        gain (float, optional): The gain factor for repulsive force. Defaults to 100.
        safe_distance (float, optional): The safe distance to maintain from obstacles. Defaults to 1.

    Returns:
        tuple: A tuple containing the repulsive force components (force_x, force_y).
    """
    force_x = 0
    force_y = 0

    for obstacle in obstacles:
        dx = obstacle[0] - current_position[0]
        dy = obstacle[1] - current_position[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance < safe_distance:
            force_x += -gain * (1/distance - 1/safe_distance) * (dx/distance**3)
            force_y += -gain * (1/distance - 1/safe_distance) * (dy/distance**3)

    return force_x, force_y

def calculate_repulsive_force_with_borders(current_position, obstacles, gain=100, safe_distance=1, boundary_x_min=30, boundary_x_max=260, boundary_y_min=10, boundary_y_max=110):
    """
    Calculates the repulsive force from the obstacles and rectangular environment borders.

    Args:
        current_position (tuple): The current position (x, y) of the object.
        obstacles (list): A list of obstacle positions [(x1, y1), (x2, y2), ...].
        gain (float, optional): The gain factor for repulsive force. Defaults to 100.
        safe_distance (float, optional): The safe distance to maintain from obstacles. Defaults to 1.
        boundary_x_min (float, optional): The minimum x-coordinate of the environment boundary. Defaults to 30.
        boundary_x_max (float, optional): The maximum x-coordinate of the environment boundary. Defaults to 260.
        boundary_y_min (float, optional): The minimum y-coordinate of the environment boundary. Defaults to 10.
        boundary_y_max (float, optional): The maximum y-coordinate of the environment boundary. Defaults to 110.

    Returns:
        tuple: A tuple containing the repulsive force components (force_x, force_y).
    """
    force_x = 0
    force_y = 0

    # Calculate repulsive forces from obstacles
    for obstacle in obstacles:
        dx = obstacle[0] - current_position[0]
        dy = obstacle[1] - current_position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < safe_distance:
            force_x += -gain * (1 / distance - 1 / safe_distance) * (dx / distance ** 3)
            force_y += -gain * (1 / distance - 1 / safe_distance) * (dy / distance ** 3)

    # Calculate repulsive forces from rectangular environment borders
    boundary_force_x = 0
    boundary_force_y = 0

    if current_position[0] < boundary_x_min:
        boundary_force_x += gain / (current_position[0] - boundary_x_min)
    elif current_position[0] > boundary_x_max:
        boundary_force_x += -gain / (current_position[0] - boundary_x_max)

    if current_position[1] < boundary_y_min:
        boundary_force_y += gain / (current_position[1] - boundary_y_min)
    elif current_position[1] > boundary_y_max:
        boundary_force_y += -gain / (current_position[1] - boundary_y_max)

    force_x += boundary_force_x
    force_y += boundary_force_y

    return force_x, force_y

def calculate_repulsive_force_moving_obstacles1(current_position, obstacles, moving_obstacles, static_gain=100, dynamic_gain=100, safe_distance=1, boundary_x_min=30, boundary_x_max=260, boundary_y_min=10, boundary_y_max=110):
    """
    Calculates the repulsive force from the obstacles, moving obstacles, and rectangular environment borders.

    Args:
        current_position (tuple): The current position (x, y) of the object.
        obstacles (list): A list of obstacle positions [(x1, y1), (x2, y2), ...].
        moving_obstacles (list): A list of moving obstacle positions [(x1, y1), (x2, y2), ...].
        static_gain (float, optional): The gain factor for repulsive force from static obstacles. Defaults to 100.
		  dynamic_gain (float, optional): The gain factor for repulsive force from dynamic obstacles. Defaults to 100.
        safe_distance (float, optional): The safe distance to maintain from obstacles. Defaults to 1.
        boundary_x_min (float, optional): The minimum x-coordinate of the environment boundary. Defaults to 30.
        boundary_x_max (float, optional): The maximum x-coordinate of the environment boundary. Defaults to 260.
        boundary_y_min (float, optional): The minimum y-coordinate of the environment boundary. Defaults to 10.
        boundary_y_max (float, optional): The maximum y-coordinate of the environment boundary. Defaults to 110.

    Returns:
        tuple: A tuple containing the repulsive force components (force_x, force_y).
    """
    force_x = 0
    force_y = 0

    # Calculate repulsive forces from obstacles
    for obstacle in obstacles:
        dx = obstacle[0] - current_position[0]
        dy = obstacle[1] - current_position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < tolerance:
            distance = tolerance

        if distance < safe_distance:
            force_x += -static_gain * (1 / distance - 1 / safe_distance) * (dx / distance ** 3)
            force_y += -static_gain * (1 / distance - 1 / safe_distance) * (dy / distance ** 3)

    # Calculate repulsive forces from moving obstacles
    for moving_obstacle in moving_obstacles:
        dx = moving_obstacle[0] - current_position[0]
        dy = moving_obstacle[1] - current_position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < tolerance:
            distance = tolerance

        if distance < safe_distance:
            force_x += -dynamic_gain * (1 / distance - 1 / safe_distance) * (dx / distance ** 3)
            force_y += -dynamic_gain * (1 / distance - 1 / safe_distance) * (dy / distance ** 3)

    # Calculate repulsive forces from rectangular environment borders
    boundary_force_x = 0
    boundary_force_y = 0

    if current_position[0] < boundary_x_min:
        boundary_force_x += static_gain / (current_position[0] - boundary_x_min)
    elif current_position[0] > boundary_x_max:
        boundary_force_x += -static_gain / (current_position[0] - boundary_x_max)

    if current_position[1] < boundary_y_min:
        boundary_force_y += static_gain / (current_position[1] - boundary_y_min)
    elif current_position[1] > boundary_y_max:
        boundary_force_y += -static_gain / (current_position[1] - boundary_y_max)

    force_x += boundary_force_x
    force_y += boundary_force_y

    return force_x, force_y


def calculate_repulsive_force_moving_obstacles(current_position, obstacles, moving_obstacles, static_gain=100, dynamic_gain=100, safe_distance=1,
                                               boundary_x_min=30, boundary_x_max=260, boundary_y_min=10, boundary_y_max=110):
    """
    Calculates the repulsive force from the obstacles, moving obstacles, and rectangular environment borders.

    Args:
        current_position (tuple): The current position (x, y) of the object.
        obstacles (list): A list of obstacle positions [(x1, y1), (x2, y2), ...].
        moving_obstacles (list): A list of moving obstacle positions [(x1, y1), (x2, y2), ...].
        static_gain (float, optional): The gain factor for repulsive force from static obstacles. Defaults to 100.
        dynamic_gain (float, optional): The gain factor for repulsive force from dynamic obstacles. Defaults to 100.
        safe_distance (float, optional): The safe distance to maintain from obstacles. Defaults to 1.
        boundary_x_min (float, optional): The minimum x-coordinate of the environment boundary. Defaults to 30.
        boundary_x_max (float, optional): The maximum x-coordinate of the environment boundary. Defaults to 260.
        boundary_y_min (float, optional): The minimum y-coordinate of the environment boundary. Defaults to 10.
        boundary_y_max (float, optional): The maximum y-coordinate of the environment boundary. Defaults to 110.

    Returns:
        tuple: A tuple containing the repulsive force components (force_x, force_y).
    """
    force_x = 0
    force_y = 0

    # Calculate repulsive forces from obstacles
    for obstacle in obstacles:
        dx = obstacle[0] - current_position[0]
        dy = obstacle[1] - current_position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < tolerance:
            distance = tolerance

        # Calculate the size of the square obstacle for repulsion consideration
        obstacle_size = 10  # Size of fixed obstacles (10x10)

        if distance < safe_distance + obstacle_size:
            force_x += -static_gain * (1 / distance - 1 / (safe_distance + obstacle_size)) * (dx / distance ** 3)
            force_y += -static_gain * (1 / distance - 1 / (safe_distance + obstacle_size)) * (dy / distance ** 3)

    # Calculate repulsive forces from moving obstacles
    for moving_obstacle in moving_obstacles:
        dx = moving_obstacle[0] - current_position[0]
        dy = moving_obstacle[1] - current_position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < tolerance:
            distance = tolerance
        # Calculate the size of the square obstacle for repulsion consideration
        obstacle_size = 10  # Size of moving obstacles (5x5)

        if distance < safe_distance + obstacle_size:
            force_x += -dynamic_gain * (1 / distance - 1 / (safe_distance + obstacle_size)) * (dx / distance ** 3)
            force_y += -dynamic_gain * (1 / distance - 1 / (safe_distance + obstacle_size)) * (dy / distance ** 3)

    # Calculate repulsive forces from rectangular environment borders
    boundary_force_x = 0
    boundary_force_y = 0

    if current_position[0] < boundary_x_min:
        boundary_force_x += static_gain / (current_position[0] - boundary_x_min)
    elif current_position[0] > boundary_x_max:
        boundary_force_x += -static_gain / (current_position[0] - boundary_x_max)

    if current_position[1] < boundary_y_min:
        boundary_force_y += static_gain / (current_position[1] - boundary_y_min)
    elif current_position[1] > boundary_y_max:
        boundary_force_y += -static_gain / (current_position[1] - boundary_y_max)

    force_x += boundary_force_x
    force_y += boundary_force_y

    return force_x, force_y


MAX_SPEED_PAYLOAD = 0.5
MAX_SPEED_NO_PAYLOAD = 0.8
def convert_force_to_speed(force, mass, time_interval, payload):
    """
    Converts the force to speed on the x and y axes.

    Args:
        force (tuple): A tuple containing the force components (force_x, force_y).
        mass (float): The mass of the object.
        time_interval (float): The time interval for which the force is applied.

    Returns:
        tuple: A tuple containing the speed components (speed_x, speed_y) on the x and y axes.
    """
    acceleration_x = force[0] / mass
    acceleration_y = force[1] / mass

    speed_x = acceleration_x * time_interval
    speed_y = acceleration_y * time_interval
    total_speed = math.sqrt(speed_x**2 + speed_y**2)
    if total_speed > MAX_SPEED_PAYLOAD and payload > 0: #Speed exceeds the maximum speed for AGV with payload
        scaling_factor = MAX_SPEED_PAYLOAD/total_speed
        speed_x = speed_x * scaling_factor
        speed_y = speed_y * scaling_factor
    if total_speed > MAX_SPEED_NO_PAYLOAD and payload == 0: #Speed exceeds the maximum speed for AGV without payload
        scaling_factor = MAX_SPEED_NO_PAYLOAD/total_speed
        speed_x = speed_x * scaling_factor
        speed_y = speed_y * scaling_factor

    return speed_x, speed_y