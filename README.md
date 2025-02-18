# 3D Printing Simulation: Path Generation and Mesh Export/Visualization

This project is a Python-based toolset for generating various 3D paths, converting them into mesh objects via extrusion along Rotation Minimizing Frames (RMF), and visualizing the results (both statically and as animated GIFs). The intended application is in the simulation of 3D printed structures (e.g., concrete printing), and it includes functionality to export paths as CSV, generate different shapes, and output a mesh (OBJ file) for further analysis.

## Features

- **Path Generation**  
  Generate a variety of paths:
  - **Cylindrical Path:** Create a series of circular layers.
  - **Hollow Cube:** Generate square perimeters for each layer.
  - **Convex/Concave Curves:** Produce paths with outward or inward curvature.
  - **Straight Wall with Smooth Arc Transitions:** Produce a zig-zag path with smooth transitions between layers.

- **Profile Generation**  
  Create 2D profiles (e.g., rectangle or circle/ellipse) in local coordinates that can be extruded along a path.

- **Rotation Minimizing Frames (RMF)**  
  Compute RMF along a 3D path and orient the profile accordingly to form a 3D mesh.

- **Mesh Editing & Export**  
  - Export the generated mesh as an OBJ file.
  - Apply mesh editing functions such as Laplacian smoothing and vertex welding.

- **Visualization**  
  - Plot the final oriented profiles and the underlying path.
  - Generate animated GIFs to show the progressive build-up of the object.

## Project Structure

- **main.py**  
  The main orchestrator. It lets you choose a path generator (or load a CSV path), a profile type, computes the RMF frames, orients the profile along the path, exports the mesh, and visualizes the result (either as a static plot or an animation).

- **path_generator.py**  
  Contains functions such as `generate_cylindrical_path()`, `generate_hollow_cube()`, `generate_convex_circle()`, `generate_concave_circle()`, and `generate_straight_wall()`. These functions generate 3D paths for various shapes and export them to CSV.

- **path_importer.py**  
  Provides the `load_path()` function to import path data from CSV files.

- **profile_generator.py**  
  Offers functions for creating 2D profiles, such as `generate_rectangle_profile()` and `generate_circle_profile()`.

- **rmf.py**  
  Implements functions for computing RMF frames along a path (`compute_rmf_frames()`) and for mapping the 2D profile into 3D along the path (`oriented_profiles_rmf()`).

- **mesh_exporter.py**  
  Contains functions for converting oriented profiles into a mesh, including helper functions to close profiles, flatten vertices, create faces, and export the result as an OBJ file (`export_mesh_to_obj()`).

- **mesh_editor.py**  
  Provides additional mesh editing functions such as `laplacian_smoothing()` and `weld_vertices()`.

- **visualization.py**  
  Contains functions to visualize the generated object:
  - `plot_oriented_profiles()` displays a static 3D plot.
  - `animate_oriented_profiles()` (or its variants) produces an animated GIF showing the build process.



