# main.py

from path_generator import generate_cylindrical_path, generate_straight_wall, generate_hollow_cube, generate_convex_circle, generate_concave_circle
import path_generator
from path_importer import load_path
from profile_generator import generate_rectangle_profile, generate_circle_profile
from rmf import compute_rmf_frames, oriented_profiles_rmf
from mesh_exporter import export_mesh_to_obj
from mesh_editor import laplacian_smoothing, weld_vertices
from visualization import plot_oriented_profiles, animate_oriented_profiles

def main():
    # ----------------------------
    # Step 1: Generate or load a path
    # ----------------------------
    # Option 1: Generate a cylindrical path (10 layers, radius=1.0, layer height=0.2)
    #path = generate_cylindrical_path(layers=10, radius=10.0, num_points=36, layer_height=2.0)
    #path = generate_hollow_cube(layers=10, side_length=20.0, num_points_per_edge=5, layer_height=2.0)
    #path = generate_convex_circle(radius_bottom=5.0, radius_top=5.0, layers=10, num_points=12, layer_height=2.0)
    path = generate_concave_circle(radius_bottom=5.0, radius_top=5.0, layers=10, num_points=12, layer_height=2.0)
    #path = generate_straight_wall(layers=5, length=10.0, num_points=10, layer_height=2.0, arc_vertices=10, arc_offset=1.0)
    # Option 2: Load a path from a CSV file (uncomment to use)
    path = load_path('concave_path.csv')
    #path = load_path('wall_path.csv')
    
    
    # ----------------------------
    # Step 2: Generate a profile
    # ----------------------------
    # Create a rectangular profile in local coordinates
    #(modify as needed) something is wrong the width is the height
    # the dimensions are correct in the profile’s own space, but the rotation makes them look different globally.
    # so essentially width becomes height and height width as it rotates in the spline profile

    prof = 2

    if prof == 1:
        profile = generate_rectangle_profile(width=2.0, height=2.0)
    elif prof == 2:
        # Alternatively, create a circular (or elliptical) profile:
        profile = generate_circle_profile(radius=1.0, num_points=12, radius_y=2.0)
    # ----------------------------
    # Step 3: Compute RMF frames along the path
    # ----------------------------
    frames = compute_rmf_frames(path)
    
    # ----------------------------
    # Step 4: Orient the profile along the path using the RMF frames
    # ----------------------------
    oriented_profiles = oriented_profiles_rmf(profile, path, frames)
    
    # ----------------------------
    # Step 5: Export the mesh (optional)
    # ----------------------------
    export_mesh_to_obj(oriented_profiles, filename='mesh.obj', cap_ends_flag=True)
    
    # ----------------------------
    # Step 6: Visualize the result
    # ----------------------------
    # For static visualization:
    plot_oriented_profiles(oriented_profiles, path)
    
    # For animated visualization, comment out the static plot above and uncomment below:
    #animate_oriented_profiles(oriented_profiles, path, interval=300)
    
if __name__ == '__main__':
    main()
