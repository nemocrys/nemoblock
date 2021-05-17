from nemoblock import *


mesh = Mesh()


####################
# Geometry parameters (origin of coordinate system in bottom of melt)
r_top = 0.1  # radius feed rod
r_bt = 0.3  # radius crystal
h_axis = 0.5  # height of floating zone

####################
# Mesh parameters
factor = 1


####################
# Patches
top_surf = Patch(mesh, "wall topSurf")
bt_surf = Patch(mesh, "wall BottomSurf")
free_surf = Patch(mesh, "wall FreeSurf")

####################
# Central cylinder
radius_sides = r_top / 2
radius_middle = 1.15 * radius_sides

cells_center_r = factor * 10
cells_center_h = factor * 10
b_center_0 = Block(
    mesh,
    cartesian(radius_sides, 0, 0),
    cartesian(radius_middle, 45, 0),
    cartesian(radius_sides, 90, 0),
    cartesian(0, 0, 0),
    cartesian(radius_sides, 0, h_axis),
    cartesian(radius_middle, 45, h_axis),
    cartesian(radius_sides, 90, h_axis),
    cartesian(0, 0, h_axis)
)
b_center_0.set_number_of_cell(cells_center_r, cells_center_r, cells_center_h)
b_center_0.create()

b_center_90 = Block(mesh)
b_center_90.set_connection(b_center_0, "front")
b_center_90.p2 = cartesian(radius_middle, 135, 0)
b_center_90.p3 = cartesian(radius_sides, 180, 0)
b_center_90.p6 = cartesian(radius_middle, 135, h_axis)
b_center_90.p7 = cartesian(radius_sides, 180, h_axis)
b_center_90.cells_x1 = cells_center_r
b_center_90.create()

b_center_180 = Block(mesh)
b_center_180.set_connection(b_center_90, "right")
b_center_180.p0 = cartesian(radius_sides, 270, 0)
b_center_180.p3 = cartesian(radius_middle, 225, 0)
b_center_180.p4 = cartesian(radius_sides, 270, h_axis)
b_center_180.p7 = cartesian(radius_middle, 225, h_axis)
b_center_180.cells_x0 = cells_center_r
b_center_180.create()

b_center_270 = Block(mesh)
b_center_270.set_connection(b_center_180, "back")
b_center_270.set_connection(b_center_0, "right")
b_center_270.p0 = cartesian(radius_middle, 315, 0)
b_center_270.p4 = cartesian(radius_middle, 315, h_axis)
b_center_270.create()

top_surf.add_face(b_center_0.face_top)
top_surf.add_face(b_center_90.face_top)
top_surf.add_face(b_center_180.face_top)
top_surf.add_face(b_center_270.face_top)
bt_surf.add_face(b_center_0.face_bottom)
bt_surf.add_face(b_center_90.face_bottom)
bt_surf.add_face(b_center_180.face_bottom)
bt_surf.add_face(b_center_270.face_bottom)

####################
# Central ring

cells_cring = factor * 10

b_cring_0 = Block(mesh)
b_cring_0.set_connection(b_center_0, "back")
b_cring_0.p0 = cartesian(r_top, 0, 0)
b_cring_0.p1 = cartesian(r_top, 45, 0)
b_cring_0.p4 = cartesian(r_top, 0, h_axis)
b_cring_0.p5 = cartesian(r_top, 45, h_axis)
b_cring_0.cells_x1 = cells_cring
b_cring_0.create()
b_cring_0.e0.type = "arc"
b_cring_0.e0.points.append(cartesian(r_top, 22.5, 0))
b_cring_0.e3.type = "arc"
b_cring_0.e3.points.append(cartesian(r_top,22.5, h_axis))

mesh.write()
