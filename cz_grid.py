from nemoblock import *
from cz_points import *

mesh = Mesh()

####################
# For mesh optimization
one_mesh_only = True


####################
# Surfaces defined by splines
s_bt = spline(s_bt)  # crucible: bottom of c1, r1, r2
s_fs = spline(s_fs)  # free surface: right of r2, top of r3
s_ph = spline(s_ph)  # melting front: top of c2
s_cr = spline(s_cr)  # crystal conus

fig, ax = plot_spline(s_bt, [0, r_crucible])
plot_spline(s_fs, [r_crystal, r_crucible], fig, ax)
plot_spline(s_ph, [0, r_crystal], fig, ax)
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
c1_r_top = r_crystal
c1_z_top = - h_melt/2 + h_melt*1/20
c1_r_bt = r_crystal*1.2

# ring r1
r1_r_top = r_crystal + (r_crucible - r_crystal)*1/3
r1_z_top = c1_z_top
r1_r_bt = r_crucible * 5 / 6

# ring r2
r2_r_bt = r_crucible
r2_r_top = r_crystal + (r_crucible - r_crystal)*1/2
r2_z_top = s_fs(r2_r_top)

# cylinder c2
c2_r_top = r_crystal

####################
# Mesh sizes
res_phi = 80
res_r_c1 = 10  # applies also for c2
res_r_r1 = 10  # applies also fro r3

# res_z_c1 = 10  # applies also for r1, r2
# res_z_c2 = 20  # applies also for r2, r3
####################
res_z_c1, grading_bottom = boundary_layer(
    0.1, "xmin", smallest_element, layer_thickness, growth_rate
)
res_z_c2, grading_top = boundary_layer(
    0.1, "xmax", smallest_element, layer_thickness, growth_rate
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
    s_ph,
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
# crystal
res_z_c3, grading_crys = boundary_layer(
    l_crystal, "xmin", smallest_element, layer_thickness, growth_rate
)


c3 = create_cylinder(mesh, c2_r_top, c2_r_top, s_cr, s_ph, res_r_c1, res_phi, res_z_c3)
c3.set_grading_axial(grading_crys)

# Patches
bt_surf = Patch(mesh, "wall CrysBtSurf")
bt_surf.faces += c3.surf_bt

out_surf = Patch(mesh, "wall CrysOutSurf")
out_surf.faces += c3.surf_rad
out_surf.faces += c3.surf_top


mesh.write()
if not one_mesh_only:
    if os.path.exists('./system/blockMeshDict_crys'):
        os.remove('./system/blockMeshDict_crys')
    os.rename('./system/blockMeshDict', './system/blockMeshDict_crys')
