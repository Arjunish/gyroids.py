import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
z = np.linspace(0, 1, 100)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

A = 1
T = 0
def G(X, Y, Z):
    X_scaled = 2 * np.pi * X / A
    Y_scaled = 2 * np.pi * Y / A
    Z_scaled = 2 * np.pi * Z / A
    return (np.sin(X_scaled) * np.cos(Y_scaled) +
            np.sin(Y_scaled) * np.cos(Z_scaled) +
            np.sin(Z_scaled) * np.cos(X_scaled))
def S(X, Y, Z):
    return X**2 + Y**2 - 0.25 
values = S(X, Y, Z)
spacing = (x[1] - x[0], y[1] - y[0], z[1] - z[0])
verts, faces, _, _ = measure.marching_cubes(values, level=T, spacing=spacing)

def triangle_area(v0, v1, v2):
    return 0.5 * np.linalg.norm(np.cross(v1 - v0, v2 - v0))

area = 0
for face in faces:
    area += triangle_area(*verts[face])

inside_mask = values < T
volume_fraction = np.sum(inside_mask) / values.size
unit_cell_volume = (x[-1] - x[0]) * (y[-1] - y[0]) * (z[-1] - z[0])
gyroid_volume = volume_fraction * unit_cell_volume

print("Surface area: {:.4f}".format(area))
print("Volume fraction inside gyroid: {:.4f}".format(volume_fraction))
print("Enclosed gyroid volume: {:.4f}".format(gyroid_volume))

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
mesh = Poly3DCollection(verts[faces], alpha=0.7, edgecolor='k')
ax.add_collection3d(mesh)
ax.set_xlim(verts[:, 0].min(), verts[:, 0].max())
ax.set_ylim(verts[:, 1].min(), verts[:, 1].max())
ax.set_zlim(verts[:, 2].min(), verts[:, 2].max())
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.tight_layout()
plt.show()
