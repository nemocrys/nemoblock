from nemoblock import *
from ds_points import *

one_mesh_only = False

mesh = Mesh()

####################
# grading strings
# parameters: (layer size, number of cells, expansion)
grad_d_xmin = f"( ({grad_d_layer_size} {grad_d_n_cells} {grad_d_expansion}) ({container_r - grad_d_layer_size} {res_d/2 - grad_d_n_cells} 1) )"
grad_d_xmax = f"( ({container_r - grad_d_layer_size} {res_d/2 - grad_d_n_cells} 1) ({grad_d_layer_size} {grad_d_n_cells} {1/grad_d_expansion}))"

melt_h = container_h - h_phase_if_edges
grad_melt_h = f"( ({grad_melt_bt_size} {grad_melt_bt_cells} {grad_melt_bt_expansion}) ({melt_h - grad_melt_bt_size - grad_melt_top_size} {res_h_melt - grad_melt_bt_cells - grad_melt_top_cells} 1) ({grad_melt_top_size} {grad_melt_top_cells} {1/grad_melt_top_expansion}) )"

crys_h = container_h - melt_h
grad_crys_h = f"( ({crys_h - grad_crys_top_size} {res_h_crystal - grad_crys_top_cells} 1) ({grad_crys_top_size} {grad_crys_top_cells} {1/grad_crys_top_expansion}) )"


####################
# solid
####################
# blocks
b1 = Block(
    mesh,
    [0, 0, 0],
    [container_r, 0, 0],
    [container_r, container_r, 0],
    [0, container_r, 0],
    [0, 0, h_phase_if_center],
    [container_r, 0, h_phase_if_side_mid],
    [container_r, container_r, h_phase_if_edges],
    [0, container_r, h_phase_if_side_mid],
)
b1.set_number_of_cells(res_d / 2, res_d / 2, res_h_crystal)
b1.create()

b2 = Block(mesh)
b2.set_connection(b1, "right")
b2.p0 = [-container_r, 0, 0]
b2.p3 = [-container_r, container_r, 0]
b2.p4 = [-container_r, 0, h_phase_if_side_mid]
b2.p7 = [-container_r, container_r, h_phase_if_edges]
b2.cells_x1 = res_d / 2
b2.create()

b3 = Block(mesh)
b3.set_connection(b2, "back")
b3.p0 = [-container_r, -container_r, 0]
b3.p1 = [0, -container_r, 0]
b3.p4 = [-container_r, -container_r, h_phase_if_edges]
b3.p5 = [0, -container_r, h_phase_if_side_mid]
b3.cells_x2 = res_d / 2
b3.create()

b4 = Block(mesh)
b4.set_connection(b3, "left")
b4.set_connection(b1, "back")
b4.p1 = [container_r, -container_r, 0]
b4.p5 = [container_r, -container_r, h_phase_if_edges]
b4.create()

####################
# spline surface
r = np.linspace(0, container_r, 100)
# edges inside container
for e in [b1.e3, b1.e7, b3.e2, b3.e6]:
    e.type = "spline"
for i in range(100):
    b1.e3.points.append([r[i], 0, s_ph_mid(r[i])])
    b1.e7.points.append([0, r[i], s_ph_mid(r[i])])
    b3.e2.points.append([-r[-(i + 1)], 0, s_ph_mid(r[-(i + 1)])])
    b3.e6.points.append([0, -r[-(i + 1)], s_ph_mid(r[-(i + 1)])])
# edges at sides of container
for e in [b1.e2, b1.e6, b2.e2, b2.e7, b3.e3, b3.e7, b4.e3, b4.e6]:
    e.type = "spline"
for i in range(100):
    b1.e2.points.append([r[i], container_r, s_ph_side(r[i])])
    b1.e6.points.append([container_r, r[i], s_ph_side(r[i])])
    b2.e2.points.append([-r[-(i + 1)], container_r, s_ph_side(r[-(i + 1)])])
    b2.e7.points.append([-container_r, r[i], s_ph_side(r[i])])
    b3.e3.points.append([-r[-(i + 1)], -container_r, s_ph_side(r[-(i + 1)])])
    b3.e7.points.append([-container_r, -r[-(i + 1)], s_ph_side(r[-(i + 1)])])
    b4.e3.points.append([r[i], -container_r, s_ph_side(r[i])])
    b4.e6.points.append([container_r, -r[-(i + 1)], s_ph_side(r[-(i + 1)])])


####################
# grading
b1.grading = f"simpleGrading ({grad_d_xmax} {grad_d_xmax} {grad_crys_h})"
b2.grading = f"simpleGrading ({grad_d_xmin} {grad_d_xmax} {grad_crys_h})"
b3.grading = f"simpleGrading ({grad_d_xmin} {grad_d_xmin} {grad_crys_h})"
b4.grading = f"simpleGrading ({grad_d_xmax} {grad_d_xmin} {grad_crys_h})"

####################
# patches
if_surf_crys = Patch(mesh, "wall crysInter")
# if_surf_crys = Patch(mesh, "wall crysInter_crystal")
if_surf_crys.faces.append(b1.face_top)
if_surf_crys.faces.append(b2.face_top)
if_surf_crys.faces.append(b3.face_top)
if_surf_crys.faces.append(b4.face_top)

out_surf = Patch(mesh, "patch crysSide")
out_surf.faces.append(b1.face_right)
out_surf.faces.append(b1.face_back)
out_surf.faces.append(b2.face_back)
out_surf.faces.append(b2.face_left)
out_surf.faces.append(b3.face_left)
out_surf.faces.append(b3.face_front)
out_surf.faces.append(b4.face_front)
out_surf.faces.append(b4.face_right)

bt_surf = Patch(mesh, "patch crysEnd")
bt_surf.faces.append(b1.face_bottom)
bt_surf.faces.append(b2.face_bottom)
bt_surf.faces.append(b3.face_bottom)
bt_surf.faces.append(b4.face_bottom)

if not one_mesh_only:
    mesh.write()
    if os.path.exists("./system/solid/blockMeshDict"):
        os.remove("./system/solid/blockMeshDict")
    os.rename("./system/blockMeshDict", "./system/solid/blockMeshDict")
    mesh = Mesh()

####################
# melt
####################
# blocks

b5 = Block(
    mesh,
    [0, 0, h_phase_if_center],
    [container_r, 0, h_phase_if_side_mid],
    [container_r, container_r, h_phase_if_edges],
    [0, container_r, h_phase_if_side_mid],
    [0, 0, container_h],
    [container_r, 0, container_h],
    [container_r, container_r, container_h],
    [0, container_r, container_h],
)
b5.set_number_of_cells(res_d / 2, res_d / 2, res_h_melt)
b5.create()

b6 = Block(mesh)
b6.set_connection(b5, "right")
b6.p0 = [-container_r, 0, h_phase_if_side_mid]
b6.p3 = [-container_r, container_r, h_phase_if_edges]
b6.p4 = [-container_r, 0, container_h]
b6.p7 = [-container_r, container_r, container_h]
b6.cells_x1 = res_d / 2
b6.create()

b7 = Block(mesh)
b7.set_connection(b6, "back")
b7.p0 = [-container_r, -container_r, h_phase_if_edges]
b7.p1 = [0, -container_r, h_phase_if_side_mid]
b7.p4 = [-container_r, -container_r, container_h]
b7.p5 = [0, -container_r, container_h]
b7.cells_x2 = res_d / 2
b7.create()

b8 = Block(mesh)
b8.set_connection(b7, "left")
b8.set_connection(b5, "back")
b8.p1 = [container_r, -container_r, h_phase_if_edges]
b8.p5 = [container_r, -container_r, container_h]
b8.create()

b5.grading = f"simpleGrading ({grad_d_xmax} {grad_d_xmax} {grad_melt_h})"
b6.grading = f"simpleGrading ({grad_d_xmin} {grad_d_xmax} {grad_melt_h})"
b7.grading = f"simpleGrading ({grad_d_xmin} {grad_d_xmin} {grad_melt_h})"
b8.grading = f"simpleGrading ({grad_d_xmax} {grad_d_xmin} {grad_melt_h})"

####################
# spline surface
r = np.linspace(0, container_r, 100)
# edges inside container
for e in [b5.e0, b5.e4, b7.e1, b7.e5]:
    e.type = "spline"
for i in range(100):
    b5.e0.points.append([r[i], 0, s_ph_mid(r[i])])
    b5.e4.points.append([0, r[i], s_ph_mid(r[i])])
    b7.e1.points.append([-r[-(i + 1)], 0, s_ph_mid(r[-(i + 1)])])
    b7.e5.points.append([0, -r[-(i + 1)], s_ph_mid(r[-(i + 1)])])
# edges at sides of container
for e in [b5.e1, b5.e5, b6.e1, b6.e4, b7.e0, b7.e4, b8.e0, b8.e5]:
    e.type = "spline"
for i in range(100):
    b5.e1.points.append([r[i], container_r, s_ph_side(r[i])])
    b5.e5.points.append([container_r, r[i], s_ph_side(r[i])])
    b6.e1.points.append([-r[-(i + 1)], container_r, s_ph_side(r[-(i + 1)])])
    b6.e4.points.append([-container_r, r[i], s_ph_side(r[i])])
    b7.e0.points.append([-r[-(i + 1)], -container_r, s_ph_side(r[-(i + 1)])])
    b7.e4.points.append([-container_r, -r[-(i + 1)], s_ph_side(r[-(i + 1)])])
    b8.e0.points.append([r[i], -container_r, s_ph_side(r[i])])
    b8.e5.points.append([container_r, -r[-(i + 1)], s_ph_side(r[-(i + 1)])])

####################
# patches

surf = Patch(mesh, "wall freeSurf")
surf.faces.append(b5.face_top)
surf.faces.append(b6.face_top)
surf.faces.append(b7.face_top)
surf.faces.append(b8.face_top)

melt_surf = Patch(mesh, "wall meltWall")
melt_surf.faces.append(b5.face_right)
melt_surf.faces.append(b5.face_back)
melt_surf.faces.append(b6.face_back)
melt_surf.faces.append(b6.face_left)
melt_surf.faces.append(b7.face_left)
melt_surf.faces.append(b7.face_front)
melt_surf.faces.append(b8.face_front)
melt_surf.faces.append(b8.face_right)

if_surf = Patch(mesh, "wall crysInter")
if_surf.faces.append(b5.face_bottom)
if_surf.faces.append(b6.face_bottom)
if_surf.faces.append(b7.face_bottom)
if_surf.faces.append(b8.face_bottom)

mesh.write()
if not one_mesh_only:
    if os.path.exists("./system/fluid/blockMeshDict"):
        os.remove("./system/fluid/blockMeshDict")
    os.rename("./system/blockMeshDict", "./system/fluid/blockMeshDict")
