# -*- coding: utf-8 -*-
import sys
import numpy as np

from vispy import app, scene
from vispy import color
from vispy import visuals
from vispy.gloo import gl

canvas = scene.SceneCanvas(keys='interactive', bgcolor='#0a0a2a', size=(1000, 700))
view = canvas.central_widget.add_view()
view.camera = scene.TurntableCamera(up='z', fov=60, distance=2)

from function import get_lattice

l = np.array( np.linspace(-200, 200, 201) )
xx, yy = np.meshgrid(l, l)
z = get_lattice(l, l)

y = np.copy(z)
y -= np.min(y)
y /= np.max(y)

c = color.get_colormap("hsl").map(y).reshape(z.shape + (-1,))
c = c.flatten().tolist()
c = list(map(lambda x,y,z,w:(x,y,z,w), c[0::4],c[1::4],c[2::4],c[3::4]))

#print(c.shape)
print(z.shape)

p1 = scene.visuals.SurfacePlot(x=l, y=l, z=z, parent=view.scene)
p1.mesh_data.set_vertex_colors(c)

p1.transform = scene.transforms.MatrixTransform()
p1.transform.translate([0, 0, -np.average(z)])
p1.transform.scale([1., 1., 1/3.])
p1.transform.scale([1/400, 1/400, 1/400])

#view.add(p2)

view.add(p1)

# p1._update_data()  # cheating.
# cf = scene.filters.ZColormapFilter('fire', zrange=(z.max(), z.min()))
# p1.attach(cf)


xax = scene.Axis(pos=[[-0.5, -0.5], [0.5, -0.5]], tick_direction=(0, -1),
                 font_size=25, axis_color='red', tick_color='red',
                 text_color='red', parent=view.scene)

xax.transform = scene.STTransform(translate=(0, 0, -0.2))

yax = scene.Axis(pos=[[-0.5, -0.5], [-0.5, 0.5]], tick_direction=(-1, 0),
                font_size=25, axis_color='red', tick_color='red',
                text_color='red', parent=view.scene)

yax.transform = scene.STTransform(translate=(0, 0, -0.2))

zax = scene.Axis(pos=[[-0.5, -0.5, 0], [-0.5, -0.5, 1]], tick_direction=(0, -1),
                font_size=25, axis_color='red', tick_color='red',
                text_color='red', parent=view.scene)

#zax.transform = scene.STTransform(translate=(0, 0, -0.2))

# Add a 3D axis to keep us oriented
axis = scene.visuals.XYZAxis(parent=view.scene)


if __name__ == '__main__':
    canvas.show()
    if sys.flags.interactive == 0:
        app.run()
