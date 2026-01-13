import numpy as np
from skimage import measure

def get_geometry(f_numeric, num_variables, t=0):
    print(f"Generating geometry for {num_variables} variables (t={t})...")
    points = np.linspace(-10, 10, 30)
    
    if num_variables == 2:
        x, y = np.meshgrid(points, points)
        grid_data = f_numeric(x, y)
        contours = measure.find_contours(grid_data, 0)
        return contours, None, None 

    elif num_variables == 3:
        x, y, z = np.meshgrid(points, points, points)
        values = f_numeric(x, y, z)
        verts, faces, normals, _ = measure.marching_cubes(values, 0)
        return verts, faces, normals
        
    elif num_variables == 4:
        x, y, z = np.meshgrid(points, points, points)
        volume = f_numeric(x, y, z, t)
        
        verts, faces, normals, _ = measure.marching_cubes(volume, 0)
        return verts, faces, normals
                
    else:
        raise ValueError("Unsupported number of variables")