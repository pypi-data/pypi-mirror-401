
import sys
import numpy as np
from vispy import scene, app

from . import marching_cubes

class VisPyRenderer:
    def __init__(self, f_numeric, num_variables):
        self.f_numeric = f_numeric
        self.num_variables = num_variables
        self.t = 0.0
        self.timer = None
        
        # Desmos Style: Black background (User Preference)
        self.canvas = scene.SceneCanvas(keys='interactive', bgcolor='black', show=True)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'
        self.view.camera.fov = 45
        self.view.camera.distance = 30
        
        # Initialize mesh data (Blue-ish surface)
        self.mesh = scene.visuals.Mesh(shading='smooth', color='#3b5b9d') # Desmos blue-ish
        self.view.add(self.mesh)
        
        # Add XY Grid (White/Gray for contrast on black)
        # GridLines visual draws infinite grid lines. We want it on XY plane.
        self.grid = scene.visuals.GridLines(color=(0.5, 0.5, 0.5, 1), parent=self.view.scene)
        
        self.create_axes()

        self.update_mesh()

        if self.num_variables == 4:
            self.timer = app.Timer(interval=1/60, connect=self.on_timer, start=True)

    def create_axes(self):
        pos = np.array([
            [-10, 0, 0], [10, 0, 0],  
            [0, -10, 0], [0, 10, 0],  
            [0, 0, -10], [0, 0, 10]   
        ])
        colors = np.array([
            [0.8, 0, 0, 1], [0.8, 0, 0, 1], 
            [0, 0.8, 0, 1], [0, 0.8, 0, 1], 
            [0, 0, 0.8, 1], [0, 0, 0.8, 1]
        ])
        
        self.axes_lines = scene.visuals.Line(pos=pos, color=colors, connect='segments', method='gl', parent=self.view.scene)
        
        text_pos = []
        text_labels = []
        text_colors = []
        # Ticks
        for i in range(-10, 11, 2):
            if i == 0: continue
            
            # X axis
            text_pos.append([i, -0.5, 0]) # Offset slightly
            text_labels.append(str(i))
            text_colors.append('white')
            
            # Y axis
            text_pos.append([0.5, i, 0])
            text_labels.append(str(i))
            text_colors.append('white')
            
            # Z axis
            text_pos.append([0, -0.5, i])
            text_labels.append(str(i))
            text_colors.append('white')

        text_pos.extend([[11, 0, 0], [0, 11, 0], [0, 0, 11]])
        text_labels.extend(['X', 'Y', 'Z'])
        text_colors.extend(['red', 'green', 'blue'])

        self.text = scene.visuals.Text(text=text_labels, pos=np.array(text_pos), color=text_colors, font_size=8, parent=self.view.scene)


    def update_mesh(self):
        try:
            verts, faces, normals = marching_cubes.get_geometry(self.f_numeric, self.num_variables, self.t)
            
            if verts is not None and len(verts) > 0:
                self.mesh.set_data(vertices=verts, faces=faces)
                self.mesh.visible = True
            else:
                self.mesh.visible = False
                
        except Exception as e:
            print(f"Error updating mesh: {e}")

    def on_timer(self, event):
        self.t += 0.05 
        self.update_mesh()

    def show(self):
        self.canvas.show()
        if sys.flags.interactive == 0:
            app.run()
