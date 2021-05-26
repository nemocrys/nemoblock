"""Mesh for floating zone crystal growth simulation"""
from nemoblock import *
from fz_points import *

mesh = Mesh()

####################
# For mesh optimization
one_mesh_only = True

####################
# Surfaces defined by splines
s_bt = spline(s_bt)  # phase interface: bottom of c1, r1, r2
s_fs = spline(s_fs)  # free surface: right of r2, top of r3
s_mf = spline(s_mf)  # melting front: top of c2
s_cr = spline(s_cr)  # crystal conus

fig, ax = plot_spline(s_bt, [0, r_crystal])
plot_spline(s_fs, [r_feed, r_crystal], fig, ax)
plot_spline(s_mf, [0, r_feed], fig, ax)
plot_spline(s_cr, [0, r_crystal], fig, ax)
# plt.show()

####################
# Mes structure  (left: symmetry axis)
# fmt: off
#
# coordinate system:
#
# ^ z-direction
# |
# |
# |------->
#   r-direction
# .__
# |  | \
# .  |    \
# |c2| r3 / \
# .__|___/    \
# |  |   \ r2 /
# .c1| r1 \  /
# |__|_____\/
#
# fmt: on

####################
# Geometry

# cylinder c1
c1_r_top = r_feed * 1.3
c1_z_top = -h_melt*0.25
c1_r_bt = r_feed * 3

# ring r1
r1_r_top = r_crystal* 0.51
r1_z_top = - h_melt *0.15
r1_r_bt = r_crystal * 0.8

# ring r2
r2_r_bt = r_crystal
r2_r_top = r_crystal * 0.7
r2_z_top = s_fs(r2_r_top)

# cylinder c2
c2_r_top = r_feed

####################
# Mesh sizes
res_phi = 80
res_r_c1 = 4  # applies also for c2
res_r_r1 = 18  # applies also fro r3

# res_z_c1 = 10  # applies also for r1, r2
# res_z_c2 = 20  # applies also for r2, r3
####################
res_z_c1, grading_bottom = boundary_layer(
    h_melt/2, "xmin", smallest_element, layer_thickness, growth_rate
)
res_z_c2, grading_top = boundary_layer(
    h_melt/2, "xmax", smallest_element, layer_thickness, growth_rate
)

####################
# Blocks (defined as cylinders & rings)
c1 = create_cylinder(
    mesh, c1_r_top, c1_r_bt, c1_z_top, s_bt, res_r_c1, res_phi, res_z_c1
)
c2 = create_cylinder(
    mesh,
    c2_r_top,
    c1_r_top,
    s_mf,
    c1_z_top,
    res_r_c1,
    res_phi,
    res_z_c2,
    cylinder_below=c1,
)
r1 = create_ring(
    mesh,
    r1_r_top,
    c1_r_top,
    r1_r_bt,
    c1_r_bt,
    r1_z_top,
    s_bt,
    c1.surf_rad,
    res_r_r1,
    res_phi,
    res_z_c1,
)
r2 = create_ring(
    mesh,
    r2_r_top,
    r1_r_top,
    r2_r_bt,
    r1_r_bt,
    r2_z_top,
    s_bt,
    r1.surf_rad,
    res_z_c2,
    res_phi,
    res_z_c1,
    spline_outside=s_fs,
)
r3 = create_ring(
    mesh,
    r2_r_top,
    c2_r_top,
    r1_r_top,
    c1_r_top,
    s_fs,
    r1_z_top,
    c2.surf_rad,
    res_r_r1,
    res_phi,
    res_z_c2,
    faces_outside=r2.surf_top,
)

####################
# Grading
c2.set_grading_axial(grading_top)
r3.set_grading_axial(grading_top)
r2.set_grading_radial(grading_top)

c1.set_grading_axial(grading_bottom)
r1.set_grading_axial(grading_bottom)
r2.set_grading_axial(grading_bottom)


####################
# Patches
bt_surf = Patch(mesh, "wall BottomSurf")
bt_surf.faces += c1.surf_bt
bt_surf.faces += r1.surf_bt
bt_surf.faces += r2.surf_bt
free_surf = Patch(mesh, "wall FreeSurf")
free_surf.faces += r2.surf_rad
free_surf.faces += r3.surf_top
top_surf = Patch(mesh, "wall TopSurf")
top_surf.faces += c2.surf_top

if not one_mesh_only:
    mesh.write()
    if os.path.exists('./system/blockMeshDict_melt'):
        os.remove('./system/blockMeshDict_melt')
    os.rename('./system/blockMeshDict', './system/blockMeshDict_melt')
    mesh = Mesh()

####################
# crystal in separate mesh


#     melt    \
#    c2, r3   /|
#  c1, r1, r2/ |
# |__|_____\/  |
# .c3|      |  |
# |b1|  r4  |r5|
# |__|______|__|
# .b2|  r6  |r7|
# |__|      |  |
# . b3 \    |  |
# |_______\ |__|
# .            |
# |    c4      |
# .           /
# |        /
# .     /
# | /


# parameters
c3_z_bt = s_bt(0) + s_bt(0)*0.7
b1_z_bt = c3_z_bt + s_bt(0)*0.3
b3_z_bt = b1_z_bt - r1_r_bt
b2_z_bt = b1_z_bt + (b3_z_bt - b1_z_bt) / 2

# resolution, grading
res_z_b2 = 8
res_z_c4 = 20
res_z_c3, grading_crys = boundary_layer(
    abs(s_bt(0)*1.5), "xmax", smallest_element, layer_thickness=0.03, growth_rate=1.5
)

# blocks
c3 = create_cylinder(mesh, c1_r_bt, c1_r_bt, s_bt, c3_z_bt, res_r_c1, res_phi, res_z_c3)
r4 = create_ring(mesh, r1_r_bt, c1_r_bt, r1_r_bt, c1_r_bt, s_bt, c3_z_bt, c3.surf_rad, res_r_r1, res_phi, res_z_c3)
r5 = create_ring(mesh, r2_r_bt, r1_r_bt, r2_r_bt, r1_r_bt, s_bt, c3_z_bt, r4.surf_rad, res_z_c2, res_phi, res_z_c3)
b1 = Block(mesh)
b1.set_connection(c3.core, 'top')
b1.face_front = c3.ring.blocks[0].face_bottom
b1.face_right = c3.ring.blocks[1].face_bottom
b1.face_back = c3.ring.blocks[2].face_bottom
b1.face_left = c3.ring.blocks[3].face_bottom
for b in c3.ring.blocks:
    b.e5.type = 'line'
    b.e5.points = []
b1.p0.x2 = b1_z_bt
b1.p1.x2 = b1_z_bt
b1.p2.x2 = b1_z_bt
b1.p3.x2 = b1_z_bt
b1.set_number_of_cell(c3.core.cells_x0, c3.core.cells_x0, res_r_c1)
b1.create()

b2 = Block(mesh)
b2.set_connection(b1, 'top')
b2.p0 = cartesian(c1_r_bt, 0, b2_z_bt)
b2.p1 = cartesian(c1_r_bt, 90, b2_z_bt)
b2.p2 = cartesian(c1_r_bt, 180, b2_z_bt)
b2.p3 = cartesian(c1_r_bt, 270, b2_z_bt)
b2.set_number_of_cell(c3.core.cells_x0, c3.core.cells_x0, res_z_b2)
b2.create()
r6 = create_ring(mesh, r1_r_bt, c1_r_bt, r_crystal/2, c1_r_bt, b1_z_bt, b2_z_bt, [b2.face_front, b2.face_right, b2.face_back,  b2.face_left], res_r_r1, res_phi, res_z_b2, ring_on_top=r4)
for b in r6.blocks:
    b.e5.type = 'line'
    b.e5.points = []
b3 = Block(mesh)
b3.set_connection(b2, 'top')
b3.face_front = r6.blocks[0].face_bottom
b3.face_right = r6.blocks[1].face_bottom
b3.face_back = r6.blocks[2].face_bottom
b3.face_left = r6.blocks[3].face_bottom
b3.p0.x2 = b3_z_bt
b3.p1.x2 = b3_z_bt
b3.p2.x2 = b3_z_bt
b3.p3.x2 = b3_z_bt
b3.set_number_of_cell(c3.core.cells_x0, c3.core.cells_x0, res_r_r1)
b3.create()
r7 = create_ring(mesh, r_crystal, r1_r_bt, r_crystal, r_crystal/2, b1_z_bt, b3_z_bt, r6.surf_rad, res_z_c2, res_phi, res_z_b2, ring_on_top=r5)
c_b3_r7 = Cylinder(b3, r7, [], [], [])

c4 = create_cylinder(mesh, r_crystal, r_crystal, b3_z_bt, s_cr, res_z_c2, res_phi, res_z_c4, cylinder_on_top=c_b3_r7)

# grading
r5.set_grading_radial(grading_top)
r7.set_grading_radial(grading_top)
c4.set_grading_radial(grading_top)

c3.set_grading_axial(grading_crys)
r4.set_grading_axial(grading_crys)
r5.set_grading_axial(grading_crys)

# Patches
top_surf = Patch(mesh, "wall CrysTopSurf")
top_surf.faces += c3.surf_top
top_surf.faces += r4.surf_top
top_surf.faces += r5.surf_top

out_surf = Patch(mesh, "wall CrysOutSurf")
out_surf.faces += r5.surf_rad
out_surf.faces += r7.surf_rad
out_surf.faces += c4.surf_rad
out_surf.faces += c4.surf_bt

mesh.write()
if not one_mesh_only:
    if os.path.exists('./system/blockMeshDict_crys'):
        os.remove('./system/blockMeshDict_crys')
    os.rename('./system/blockMeshDict', './system/blockMeshDict_crys')
