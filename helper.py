# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# df = pd.read_csv("rings_debug.csv")
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# for s, g in df.groupby("station"):
#     ax.plot(g.x, g.y, g.z, 'b-', lw=0.5)
# plt.show()

# stations = df.groupby("station")[["x","y","z"]].mean().values
# dists = np.linalg.norm(np.diff(stations, axis=0), axis=1)
# print("Min inter-ring spacing:", dists.min())
# print("Max inter-ring spacing:", dists.max())

# # Station centroids
# centroids = df.groupby("station")[["x","y","z"]].mean().values

# # These are every-50th stations, so divide by 50
# dists = np.linalg.norm(np.diff(centroids, axis=0), axis=1)
# print("Spacing between sampled stations (every 50th):", dists.mean())
# print("Estimated consecutive ring spacing:", dists.mean() / 50)


# import vtk
# import numpy as np

# reader = vtk.vtkXMLPolyDataReader()
# reader.SetFileName("LCA_Centerline.vtp")
# reader.Update()
# pd = reader.GetOutput()

# pts = pd.GetPoints()
# lines = pd.GetLines()
# lines.InitTraversal()
# id_list = vtk.vtkIdList()

# # Collect all edges as (point_a_coords, point_b_coords)
# # Check if any two lines share the exact same 3D point
# all_pts = {}
# lines.InitTraversal()
# while lines.GetNextCell(id_list):
#     for k in range(id_list.GetNumberOfIds()):
#         pid = id_list.GetId(k)
#         p = tuple(np.round(pts.GetPoint(pid), 4))
#         if p in all_pts:
#             all_pts[p].add(pid)
#         else:
#             all_pts[p] = {pid}

# # How many 3D positions have more than one point ID?
# shared = {p: ids for p, ids in all_pts.items() if len(ids) > 1}
# print("3D positions with duplicate point IDs:", len(shared))
# print("Example:", list(shared.items())[:3])


import vtk
import numpy as np

reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName("LCA_Centerline.vtp")
reader.Update()
pd = reader.GetOutput()

pts = pd.GetPoints()
lines = pd.GetLines()
lines.InitTraversal()
id_list = vtk.vtkIdList()

all_paths = []
while lines.GetNextCell(id_list):
    p = [pts.GetPoint(id_list.GetId(k)) for k in range(id_list.GetNumberOfIds())]
    all_paths.append(np.array(p))

# Compare first 10 points of path 0 vs path 1
p0 = all_paths[0][:10]
p1 = all_paths[1][:10]
diffs = np.linalg.norm(p0 - p1, axis=1)
print("Point-wise distances between path 0 and path 1 (first 10 pts):")
print(diffs)