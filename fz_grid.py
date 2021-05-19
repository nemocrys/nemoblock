from nemoblock import *
import points_fz

mesh = Mesh()

####################
# Surfaces defined by splines
s_bt = spline(points_fz.s_bt)  # phase interface: bottom of c1, r1, r2
s_fs = spline(points_fz.s_fs)  # free surface: right of r2, top of r3
s_mf = spline(points_fz.s_mf)  # melting front: top of c2

fig, ax = plot_spline(s_bt, [0, 0.4])
plot_spline(s_fs, [0.1, 0.4], fig, ax)
plot_spline(s_mf, [0, 0.1], fig, ax)
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
c1_r_top = 0.1
c1_z_top = 0.22
c1_r_bt = 0.15

# ring r1
r1_r_top = 0.25
r1_z_top = 0.25
r1_r_bt = 0.3

# ring r2
r2_r_bt = points_fz.r_crystal
r2_r_top = 0.3
r2_z_top = s_fs(r2_r_top)

# cylinder c2
r_c2_top = points_fz.r_feed

####################
# Mesh sizes
res_phi = 120
res_r_c1 = 10  # applies also for c2
res_r_r1 = 20  # applies also fro r3

# res_z_c1 = 10  # applies also for r1, r2
# res_z_c2 = 20  # applies also for r2, r3
####################
res_z_c1, grading_bottom = boundary_layer(
    0.1, "xmin", smallest_element=0.0003, layer_thickness=0.007, growth_rate=1.2
)
res_z_c2, grading_top = boundary_layer(
    0.1, "xmax", smallest_element=0.0003, layer_thickness=0.01, growth_rate=1.2
)

####################
# Blocks (defined as cylinders & rings)
c1 = create_cylinder(
    mesh, c1_r_top, c1_r_bt, c1_z_top, s_bt, res_r_c1, res_phi, res_z_c1
)
c2 = create_cylinder(
    mesh,
    r_c2_top,
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
    r_c2_top,
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

mesh.write()
