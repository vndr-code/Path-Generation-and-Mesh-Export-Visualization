import numpy as np
import csv
##############
def generate_circle(radius=1.0, num_points=36, z=0.0):
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    return [[radius * np.cos(angle), radius * np.sin(angle), z] for angle in angles]

def generate_cylindrical_path(layers=3, radius=1.0, num_points=36, layer_height=0.2):
    points = []
    for i in range(layers):
        z = i * layer_height
        circle = generate_circle(radius, num_points, z)
        points.extend(circle)

    write_csv(points)

    return points

#############################
import numpy as np
import csv

def generate_square(layer, side_length, num_points_per_edge, z):
    """
    Generates a closed square (perimeter) for one layer.
    The square is centered at (0,0) with given side_length.
    num_points_per_edge specifies how many points per edge.
    Returns a list of (x, y, z) points.
    """
    half = side_length / 2.0
    # Generate one edge from (-half, -half) to (half, -half)
    x_edge = np.linspace(-half, half, num_points_per_edge, endpoint=False)
    edge1 = [(x, -half, z) for x in x_edge]
    # Right edge: from (half, -half) to (half, half)
    y_edge = np.linspace(-half, half, num_points_per_edge, endpoint=False)
    edge2 = [(half, y, z) for y in y_edge]
    # Top edge: from (half, half) to (-half, half)
    x_edge_rev = np.linspace(half, -half, num_points_per_edge, endpoint=False)
    edge3 = [(x, half, z) for x in x_edge_rev]
    # Left edge: from (-half, half) to (-half, -half)
    y_edge_rev = np.linspace(half, -half, num_points_per_edge, endpoint=False)
    edge4 = [(-half, y, z) for y in y_edge_rev]
    
    # Close the loop by repeating the first point.
    return edge1 + edge2 + edge3 + edge4 + [edge1[0]]

def generate_hollow_cube(layers, side_length, num_points_per_edge, layer_height):
    """
    Generates a hollow cube path by stacking squares.
    Each layer is a square at a different z.
    Returns a list of points.
    """
    points = []
    for i in range(layers):
        z = i * layer_height
        square = generate_square(i, side_length, num_points_per_edge, z)
        points.extend(square)

    write_csv(points)
    return points

# Example usage:
# path = generate_hollow_cube(layers=10, side_length=20.0, num_points_per_edge=10, layer_height=2.0)
###############################
def generate_convex_circle(radius_bottom, radius_top, layers, num_points, layer_height):
    """
    Generates a convex curved path by varying the circle radius per layer.
    For example, use a sine function so that the radius peaks at mid-height.
    
    Parameters:
      radius_bottom: radius at the bottom layer.
      radius_top: radius at the top layer.
      layers: number of layers.
      num_points: number of points per layer.
      layer_height: vertical distance between layers.
    
    Returns a list of 3D points.
    """
    points = []
    for i in range(layers):
        z = i * layer_height
        # Compute a factor that peaks at mid-height.
        t = i / (layers - 1)  # goes from 0 to 1
        # Use sine to have a peak in the middle: sin(pi*t)
        factor = np.sin(np.pi * t)
        # Let radius vary from radius_bottom to radius_top, peaking in the middle.
        # One simple way: linear interpolation plus the sine bump.
        base_radius = (1 - t) * radius_bottom + t * radius_top
        r = base_radius + factor * 2.0  # 2.0 is an extra bump amplitude, adjust as needed
        circle = generate_circle(r, num_points, z)
        points.extend(circle)

    write_csv(points)

    return points

# Example usage:
# path = generate_convex_circle(radius_bottom=5.0, radius_top=5.0, layers=10, num_points=36, layer_height=2.0)

####################

def generate_concave_circle(radius_bottom, radius_top, layers, num_points, layer_height):
    """
    Generates a concave curved path by varying the circle radius per layer.
    The radius is smaller in the middle and larger at the top and bottom.
    
    Parameters:
      radius_bottom: radius at the bottom layer.
      radius_top: radius at the top layer.
      layers: number of layers.
      num_points: number of points per layer.
      layer_height: vertical distance between layers.
    
    Returns a list of 3D points.
    """
    points = []
    for i in range(layers):
        z = i * layer_height
        t = i / (layers - 1)
        # Invert sine: use (1 - sin(pi*t)) so that the minimum is in the middle.
        factor = 1 - np.sin(np.pi * t)
        base_radius = (1 - t) * radius_bottom + t * radius_top
        r = base_radius + factor * 2.0  # adjust amplitude
        circle = generate_circle(r, num_points, z)
        points.extend(circle)

    write_csv(points)
    
    return points

# Example usage:
# path = generate_concave_circle(radius_bottom=5.0, radius_top=5.0, layers=10, num_points=36, layer_height=2.0)

####################################


def generate_arc(p0, p1, control, n_vertices):
    """
    Generates points along a quadratic Bézier arc between p0 and p1,
    using 'control' as the control point.
    
    Parameters:
      p0, p1, control: Lists or arrays representing 3D points.
      n_vertices: Number of vertices to generate along the arc.
    
    Returns:
      A list of 3D points along the arc.
    """
    points = []
    for t in np.linspace(0, 1, n_vertices):
        pt = (1-t)**2 * np.array(p0) + 2*(1-t)*t*np.array(control) + t**2 * np.array(p1)
        points.append(pt.tolist())
    return points

def generate_straight_wall(layers=3, length=10.0, num_points=10, layer_height=0.2, arc_vertices=5, arc_offset=0.5):
    """
    Generates a wall path with smooth arc transitions between layers.
    
    For each layer (z-level), a line of points is generated along x.
    On even layers, points go left-to-right; on odd layers, right-to-left.
    At the end of each layer (except the last), a smooth arc is inserted
    to transition to the start of the next layer.
    
    Parameters:
      layers: Number of layers.
      length: Length of the wall (in the x-direction).
      num_points: Number of points in each layer.
      layer_height: Vertical distance between layers.
      arc_vertices: Number of vertices used to approximate the transition arc.
      arc_offset: Horizontal offset for the arc's control point.
      
    Returns:
      A list of 3D points representing the continuous printing path.
    """
    points = []
    
    for i in range(layers):
        z = i * layer_height
        # Generate evenly spaced x-coordinates.
        x_coords = np.linspace(0, length, num_points)
        # Reverse order on odd layers to create a zig-zag pattern.
        if i % 2 == 1:
            x_coords = x_coords[::-1]
        
        # Generate current layer points.
        layer_points = [[x, 0.0, z] for x in x_coords]
        points.extend(layer_points)
        
        # If not the last layer, insert a smooth arc transition.
        if i < layers - 1:
            # p0: last point of current layer.
            p0 = layer_points[-1]
            # p1: first point of the next layer.
            if i % 2 == 0:
                # Even layer: p0 is at (length,0,z) and next layer (odd) starts at (length,0,z+layer_height)
                p1 = [length, 0.0, z + layer_height]
                # Control point is offset to the right.
                control = [length + arc_offset, 0.0, z + layer_height/2]
            else:
                # Odd layer: p0 is at (0,0,z) and next layer (even) starts at (0,0,z+layer_height)
                p1 = [0, 0.0, z + layer_height]
                # Control point is offset to the left.
                control = [0 - arc_offset, 0.0, z + layer_height/2]
            
            # Generate arc points (the arc includes p0 and p1).
            arc_points = generate_arc(p0, p1, control, arc_vertices)
            # Avoid duplicating p0 by skipping the first and last point of the arc.
            points.extend(arc_points[1:-1])
    
    write_csv(points, filename="wall_path.csv")
    return points

def write_csv(points, filename="concave_path.csv"):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["x", "y", "z"])
        writer.writerows(points)
    print(f"CSV file '{filename}' created.")

"""  How to use
cylinder_points = generate_cylindrical_path(layers=10, radius=10.0, num_points=12, layer_height=2.0)
generate_straight_wall(layers=4, length=10.0, num_points=5, layer_height=2.0, arc_vertices=5, arc_offset=1.0)
 """
