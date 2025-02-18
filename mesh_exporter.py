
import numpy as np

def close_profiles(oriented_profiles):
    """
    Remove duplicate endpoints in each profile if the first and last points are the same.
    Returns the updated list of profiles.
    """
    for i, profile in enumerate(oriented_profiles):
        if np.allclose(profile[0], profile[-1]):
            oriented_profiles[i] = profile[:-1]
    return oriented_profiles

def flatten_vertices(oriented_profiles):
    """
    Flattens the list of oriented profiles into a single vertex list.
    Also builds a list of lists that record the OBJ index of each vertex in every profile.
    
    Returns:
      vertices: list of vertex coordinates (as lists).
      vertex_indices: list of lists of indices corresponding to each profile.
    """
    vertices = []
    vertex_indices = []
    for profile in oriented_profiles:
        indices = []
        for pt in profile:
            vertices.append(pt.tolist())
            indices.append(len(vertices))  # OBJ indices start at 1
        vertex_indices.append(indices)
    return vertices, vertex_indices

def create_side_faces(vertex_indices):
    """
    Creates faces (as triangles) connecting consecutive profiles.
    Assumes each profile has the same number of points.
    
    Returns a list of face tuples.
    """
    faces = []
    n_profiles = len(vertex_indices)
    n_points = len(vertex_indices[0])
    
    for i in range(n_profiles - 1):
        for j in range(n_points):
            j_next = (j + 1) % n_points  # wrap-around
            v1 = vertex_indices[i][j]
            v2 = vertex_indices[i][j_next]
            v3 = vertex_indices[i+1][j_next]
            v4 = vertex_indices[i+1][j]
            # Create two triangles for each quad.
            faces.append((v1, v2, v3))
            faces.append((v1, v3, v4))
    return faces

def cap_ends(vertex_indices, oriented_profiles, vertices):
    """
    Caps the first and last profiles by creating a center point for each and
    connecting it with triangles.
    
    Returns a list of face tuples for the caps.
    """
    cap_faces = []
    n_points = len(vertex_indices[0])
    
    # Cap the first profile (start)
    start_indices = vertex_indices[0]
    center_start = np.mean(oriented_profiles[0], axis=0)
    vertices.append(center_start.tolist())
    center_index_start = len(vertices)
    for j in range(n_points):
        j_next = (j + 1) % n_points
        cap_faces.append((start_indices[j], start_indices[j_next], center_index_start))
    
    # Cap the last profile (end)
    end_indices = vertex_indices[-1]
    center_end = np.mean(oriented_profiles[-1], axis=0)
    vertices.append(center_end.tolist())
    center_index_end = len(vertices)
    for j in range(n_points):
        j_next = (j + 1) % n_points
        # Reverse the order to maintain a consistent normal direction.
        cap_faces.append((end_indices[j_next], end_indices[j], center_index_end))
    
    return cap_faces

def write_obj_file(filename, vertices, faces):
    """
    Writes the given vertices and faces into an OBJ file.
    """
    with open(filename, 'w') as f:
        for v in vertices:
            f.write("v {:.6f} {:.6f} {:.6f}\n".format(*v))
        for face in faces:
            f.write("f {} {} {}\n".format(*face))
    print(f"Mesh exported to {filename}")

def export_mesh_to_obj(oriented_profiles, filename='mesh.obj', cap_ends_flag=False):
    """
    Exports a mesh (as an OBJ file) from the oriented profiles.
    
    Steps:
      1. Close profiles (remove duplicate endpoints).
      2. Flatten vertices and record indices.
      3. Create side faces connecting profiles.
      4. Optionally cap the ends.
      5. Write the OBJ file.
    """
    oriented_profiles = close_profiles(oriented_profiles)
    vertices, vertex_indices = flatten_vertices(oriented_profiles)
    faces = create_side_faces(vertex_indices)
    
    if cap_ends_flag:
        cap_faces = cap_ends(vertex_indices, oriented_profiles, vertices)
        faces.extend(cap_faces)
    
    write_obj_file(filename, vertices, faces)


