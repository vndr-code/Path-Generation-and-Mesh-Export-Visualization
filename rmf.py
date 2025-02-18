
import numpy as np

"""
Note: the profiles are kind of tilted inwards, only sligltly but is is visible especially if the shape is anisotropic
"""

def compute_rmf_frames(path, up=np.array([0, 0, 1], dtype=float)):
    """
    Compute rotation minimizing frames (RMF) along a 3D path.
    Returns a list of frames (T, N, B) for each path point.
    """
    path = np.array(path, dtype=float)
    frames = []
    n = len(path)
    # Compute initial tangent T0
    T0 = path[1] - path[0]
    norm_T0 = np.linalg.norm(T0)
    if norm_T0 < 1e-6:
        T0 = np.array([1, 0, 0], dtype=float)  # fallback if zero-length
    else:
        T0 /= norm_T0

    # Compute initial normal N0 by projecting 'up' onto the plane perpendicular to T0
    N0 = up - np.dot(up, T0) * T0
    norm_N0 = np.linalg.norm(N0)
    if norm_N0 < 1e-6:
        N0 = np.array([1, 0, 0], dtype=float)
    else:
        N0 /= norm_N0
    B0 = np.cross(T0, N0)
    frames.append((T0, N0, B0))
    
    for i in range(1, n):
        # Compute new tangent T
        if i < n - 1:
            T = path[i+1] - path[i]
        else:
            T = path[i] - path[i-1]
        norm_T = np.linalg.norm(T)
        if norm_T < 1e-6:
            T = frames[-1][0]  # Use previous tangent if current segment is zero-length
        else:
            T /= norm_T

        T_prev, N_prev, B_prev = frames[-1]
        # Update normal: project previous normal onto plane perpendicular to new T
        N = N_prev - np.dot(N_prev, T) * T
        norm_N = np.linalg.norm(N)
        if norm_N < 1e-6:
            N = N_prev  # fallback if nearly aligned
        else:
            N /= norm_N
        B = np.cross(T, N)
        frames.append((T, N, B))
    return frames


def oriented_profiles_rmf(profile, path, frames):
    """
    For each path point with its frame (T, N, B), map the 2D profile into 3D.
    The profile's x-axis aligns with N and y-axis with B.
    """
    oriented_profiles = []
    for pt, (_, N, B) in zip(path, frames):
        oriented = np.array([pt + x * N + y * B for (x, y) in profile])
        oriented_profiles.append(oriented)
    return oriented_profiles