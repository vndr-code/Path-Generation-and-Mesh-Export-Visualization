import numpy as np
from matplotlib.animation import PillowWriter
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def set_axes_equal(ax):
    """Set equal scaling for all axes in a 3D plot."""
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    y_range = abs(y_limits[1] - y_limits[0])
    z_range = abs(z_limits[1] - z_limits[0])
    plot_radius = 0.5 * max([x_range, y_range, z_range])

    x_middle = np.mean(x_limits)
    y_middle = np.mean(y_limits)
    z_middle = np.mean(z_limits)
    
    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

def plot_oriented_profiles(oriented_profiles, path):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the central path
    xs, ys, zs = zip(*path)
    ax.plot(xs, ys, zs, 'ko-', label='Path')
    
    # Plot each oriented profile
    for profile in oriented_profiles:
        ax.plot(profile[:, 0], profile[:, 1], profile[:, 2], 'b-')
    
    # Optionally, connect corresponding vertices between adjacent profiles
    n_points = oriented_profiles[0].shape[0]
    for i in range(n_points):
        for j in range(len(oriented_profiles) - 1):
            p1 = oriented_profiles[j][i]
            p2 = oriented_profiles[j+1][i]
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'r--', linewidth=0.5)
    

    set_axes_equal(ax)  # Ensure equal aspect ratio.

    # After plotting the profiles:
    zmin, zmax = ax.get_zlim3d()
    ax.set_zlim3d(0, zmax)  # Force z to start from 0
    

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.show()

def animate_oriented_profiles(oriented_profiles, path, interval=100):
    """
    Animates the sequential addition of oriented profiles (layers) along a path.
    
    Parameters:
      oriented_profiles: List of numpy arrays (each array is a profile/layer).
      path: List of (x, y, z) points for the central path.
      interval: Time (ms) between updates.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the central path with lower opacity
    xs, ys, zs = zip(*path)
    ax.plot(xs, ys, zs, 'ko-', alpha=0.3, label='Path')
    
    set_axes_equal(ax)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    def update(frame):
        ax.cla()  # Clear the axes
        # Redraw the central path
        ax.plot(xs, ys, zs, 'ko-', alpha=0.3, label='Path')
        set_axes_equal(ax)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        
        # Plot all profiles up to the current frame
        for i in range(frame + 1):
            profile = oriented_profiles[i]
            # Ensure the profile is closed by checking first and last point
            if not np.allclose(profile[0], profile[-1]):
                profile = np.vstack([profile, profile[0]])
            ax.plot(profile[:, 0], profile[:, 1], profile[:, 2], 'b-')
            # Connect with the previous profile if available
            if i > 0:
                prev = oriented_profiles[i-1]
                n_points = prev.shape[0]
                for j in range(n_points):
                    p1 = prev[j]
                    p2 = profile[j]
                    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'r--', linewidth=0.5)
        
        ax.legend()
    
    ani = FuncAnimation(fig, update, frames=len(oriented_profiles), interval=interval, repeat=False)
    # save movie
    #ani.save('animation.mp4', writer='ffmpeg', fps=30)
    ani.save('animation.gif', writer=PillowWriter(fps=30))
    plt.show()
