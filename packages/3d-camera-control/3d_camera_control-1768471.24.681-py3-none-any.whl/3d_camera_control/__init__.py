"""
3D Camera Control Package

This package provides functionalities for controlling and manipulating virtual 3D cameras.
It includes features for camera positioning, orientation, and perspective manipulation.
"""

import math

OFFICIAL_SITE = "https://supermaker.ai/blog/qwen-image-multiple-angles-3d-camera-alibabas-breakthrough-in-ai-camera-control/"


def get_official_site() -> str:
    """
    Returns the official website URL for the 3D Camera Control project.

    Returns:
        str: The official website URL.
    """
    return OFFICIAL_SITE


class Camera:
    """
    A class representing a 3D camera with position, rotation, and field of view.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0,
                 pitch: float = 0.0, yaw: float = 0.0, roll: float = 0.0,
                 fov: float = 60.0) -> None:
        """
        Initializes a Camera object.

        Args:
            x (float): The x-coordinate of the camera's position.
            y (float): The y-coordinate of the camera's position.
            z (float): The z-coordinate of the camera's position.
            pitch (float): The pitch angle of the camera in degrees.
            yaw (float): The yaw angle of the camera in degrees.
            roll (float): The roll angle of the camera in degrees.
            fov (float): The field of view of the camera in degrees.
        """
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.fov = fov

    def rotate(self, pitch_delta: float = 0.0, yaw_delta: float = 0.0, roll_delta: float = 0.0) -> None:
        """
        Rotates the camera by the given angles.

        Args:
            pitch_delta (float): The change in pitch angle in degrees.
            yaw_delta (float): The change in yaw angle in degrees.
            roll_delta (float): The change in roll angle in degrees.
        """
        self.pitch += pitch_delta
        self.yaw += yaw_delta
        self.roll += roll_delta

    def translate(self, x_delta: float = 0.0, y_delta: float = 0.0, z_delta: float = 0.0) -> None:
        """
        Translates the camera by the given amounts.

        Args:
            x_delta (float): The change in x-coordinate.
            y_delta (float): The change in y-coordinate.
            z_delta (float): The change in z-coordinate.
        """
        self.x += x_delta
        self.y += y_delta
        self.z += z_delta

    def get_view_matrix(self) -> list[list[float]]:
        """
        Calculates the view matrix for the camera.

        Returns:
            list[list[float]]: The 4x4 view matrix as a list of lists.
        """
        # Convert angles to radians
        pitch_rad = math.radians(self.pitch)
        yaw_rad = math.radians(self.yaw)
        roll_rad = math.radians(self.roll)

        # Calculate rotation matrix (Z * Y * X order)
        cos_pitch = math.cos(pitch_rad)
        sin_pitch = math.sin(pitch_rad)
        cos_yaw = math.cos(yaw_rad)
        sin_yaw = math.sin(yaw_rad)
        cos_roll = math.cos(roll_rad)
        sin_roll = math.sin(roll_rad)

        x_rotation = [[1, 0, 0],
                      [0, cos_pitch, -sin_pitch],
                      [0, sin_pitch, cos_pitch]]

        y_rotation = [[cos_yaw, 0, sin_yaw],
                      [0, 1, 0],
                      [-sin_yaw, 0, cos_yaw]]

        z_rotation = [[cos_roll, -sin_roll, 0],
                      [sin_roll, cos_roll, 0],
                      [0, 0, 1]]

        # Concatenate rotations (Z * Y * X) - rudimentary matrix multiplication
        rotation_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    rotation_matrix[i][j] += z_rotation[i][k] * (y_rotation[k][j] if k < 3 else 0)

        rotation_matrix_final = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    rotation_matrix_final[i][j] += rotation_matrix[i][k] * (x_rotation[k][j] if k < 3 else 0)


        # Translation vector
        translation_vector = [-self.x, -self.y, -self.z]

        # View matrix (combining rotation and translation)
        view_matrix = [
            [rotation_matrix_final[0][0], rotation_matrix_final[0][1], rotation_matrix_final[0][2], translation_vector[0]],
            [rotation_matrix_final[1][0], rotation_matrix_final[1][1], rotation_matrix_final[1][2], translation_vector[1]],
            [rotation_matrix_final[2][0], rotation_matrix_final[2][1], rotation_matrix_final[2][2], translation_vector[2]],
            [0, 0, 0, 1]
        ]

        return view_matrix


def calculate_distance(camera1: Camera, camera2: Camera) -> float:
    """
    Calculates the Euclidean distance between two cameras.

    Args:
        camera1 (Camera): The first camera.
        camera2 (Camera): The second camera.

    Returns:
        float: The distance between the two cameras.
    """
    dx = camera2.x - camera1.x
    dy = camera2.y - camera1.y
    dz = camera2.z - camera1.z
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def adjust_fov_for_distance(initial_fov: float, distance: float, reference_distance: float = 10.0) -> float:
    """
    Adjusts the field of view based on the distance to a subject.

    Args:
        initial_fov (float): The initial field of view in degrees.
        distance (float): The distance to the subject.
        reference_distance (float): A reference distance at which the initial FOV is optimal. Defaults to 10.0.

    Returns:
        float: The adjusted field of view in degrees.
    """
    # Simple linear adjustment.  More sophisticated models could be used.
    fov_adjustment_factor = distance / reference_distance
    adjusted_fov = initial_fov * fov_adjustment_factor
    return adjusted_fov