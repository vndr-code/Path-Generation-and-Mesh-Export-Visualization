# mesh_editor.py

import numpy as np

def laplacian_smoothing(vertices, faces, iterations=10, alpha=0.5):
    """
    Applies Laplacian smoothing to a mesh.

    Parameters:
      vertices: (N, 3) NumPy array of vertex positions.
      faces: List of faces (each face is a tuple/list of vertex indices, 0-indexed).
      iterations: Number of smoothing iterations.
      alpha: Smoothing factor (0 < alpha <= 1); higher alpha produces stronger smoothing.

    Returns:
      Smoothed vertices as an (N, 3) NumPy array.
    """
    # Build a dictionary mapping each vertex index to its neighboring vertex indices.
    neighbors = {i: set() for i in range(len(vertices))}
    for face in faces:
        i1, i2, i3 = face  # assuming triangular faces
        neighbors[i1].update([i2, i3])
        neighbors[i2].update([i1, i3])
        neighbors[i3].update([i1, i2])
    
    vertices = vertices.copy()
    for _ in range(iterations):
        new_vertices = vertices.copy()
        for i in range(len(vertices)):
            if neighbors[i]:
                neighbor_positions = np.array([vertices[j] for j in neighbors[i]])
                avg = neighbor_positions.mean(axis=0)
                new_vertices[i] = (1 - alpha) * vertices[i] + alpha * avg
        vertices = new_vertices
    return vertices

def weld_vertices(vertices, faces, threshold=1e-6):
    """
    Welds (merges) vertices that are within a specified threshold distance.

    Parameters:
      vertices: List or (N,3) array of vertex positions.
      faces: List of faces (each face is a tuple/list of vertex indices, 0-indexed).
      threshold: Distance threshold below which vertices are considered identical.

    Returns:
      A tuple (new_vertices, new_faces) where:
        - new_vertices is an (M, 3) NumPy array of welded vertex positions.
        - new_faces is a list of faces with updated indices.
    """
    vertices = np.array(vertices)
    new_indices = {}
    new_vertices = []
    for i, v in enumerate(vertices):
        found = False
        for j, nv in enumerate(new_vertices):
            if np.linalg.norm(v - np.array(nv)) < threshold:
                new_indices[i] = j
                found = True
                break
        if not found:
            new_indices[i] = len(new_vertices)
            new_vertices.append(v.tolist())
    
    new_faces = []
    for face in faces:
        new_face = tuple(new_indices[i] for i in face)
        new_faces.append(new_face)
    
    return np.array(new_vertices), new_faces

# You can add more mesh editing functions here (e.g., subdivision, Taubin smoothing, etc.)
