import numpy as np

def generate_circle_profile(radius=0.5, num_points=12, radius_y=None):
    """Generate a 2D circular (or elliptical) profile in the XY plane, closed."""
    if radius_y is None:
        radius_y = radius  # For a perfect circle, both radii are equal.
    angles = np.linspace(0, 2*np.pi, num_points, endpoint=False)
    points = np.array([[radius * np.cos(a), radius_y * np.sin(a)] for a in angles])
    # Close the loop by appending the first point at the end.
    points = np.vstack([points, points[0]])
    return points

def generate_rectangle_profile(width=1.0, height=0.5):
    # A closed rectangle profile in the XY plane.
    return np.array([
        [-width/2, -height/2],
        [ width/2, -height/2],
        [ width/2,  height/2],
        [-width/2,  height/2],
        [-width/2, -height/2]  # Close the loop
    ])