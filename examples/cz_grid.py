"""Mesh for Czochralski crystal growth simulation"""
from nemoblock import *
from cz_points import *

mesh = Mesh()
####################
# For mesh optimization
one_mesh_only = False


####################
# Surfaces defined by splines
s_bt = spline(s_bt)  # crucible: bottom of c1, r1, r2
s_fs = spline(s_fs)  # free surface: right of r2, top of r3
s_ph = spline(s_ph)  # melting front: top of c2
s_cr = spline(s_cr)  # crystal conus

# fig, ax = plot_spline(s_bt, [0, r_crucible])
# plot_spline(s_fs, [r_crystal, r_crucible], fig, ax)
# plot_spline(s_ph, [0, r_crystal], fig, ax)
# plot_spline(s_cr, [0, r_crystal], fig, ax)
# ax.axis('equal')
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
c1_z_top = -h_melt / 2 + h_melt * 1 / 20
c1_r_bt = r_crystal * 1.2

# ring r1
r1_r_top = r_crystal + (r_crucible - r_crystal) * 0.4
r1_z_top = c1_z_top + h_melt/20
r1_r_bt = r_crucible * 0.92

# ring r2
r2_r_top = r_crystal + (r_crucible - r_crystal) * 0.5


####################
# Mesh sizes
res_phi = 40
# res_r_c1 = 4  # applies also for c2
# res_r_r1 = 5  # applies also fro r3
# res_z_c1 = 10  # applies also for r1, r2
# res_z_c2 = 20  # applies also for r2, r3
####################
res_z_c1, grading_bottom = boundary_layer(
    h_melt / 2, "xmin", smallest_element_crucible, layer_thickness_crucible, growth_rate_crucible
)
res_z_c2, grading_top = boundary_layer(
    h_melt / 2, "xmax", smallest_element_top, layer_thickness_top, growth_rate_top
)
res_r_r1, grading_meniscus = boundary_layer(
    h_melt / 2, "xmin", smallest_element_meniscus, layer_thickness_meniscus, growth_rate_meniscus
)
res_r_c1, grading_crys_rad = boundary_layer(
    r_crystal * 0.5, "xmax", smallest_element_crystal_side, layer_thickness_crystal_side, growth_rate_crystal_side
)
####################
# Blocks (defined as cylinders & rings)
c1 = create_cylinder(
    mesh, [c1_r_top, c1_z_top], [c1_r_bt, s_bt(c1_r_bt)], res_r_c1, res_phi, res_z_c1
)
c1.set_spline_surface(s_bt, "bottom")
c2 = create_cylinder(
    mesh,
    [r_crystal, s_ph(r_crystal)],
    [c1_r_top, c1_z_top],
    res_r_c1,
    res_phi,
    res_z_c2,
    cylinder_below=c1,
)
c2.set_spline_surface(s_ph, "top")
r1 = create_ring(
    mesh,
    [r1_r_top, r1_z_top],
    [r1_r_bt, s_bt(r1_r_bt)],
    c1.surf_rad,
    res_r_r1,
    res_phi,
    res_z_c1,
)
r1.set_spline_surface(s_bt, "bottom")
r2 = create_ring(
    mesh,
    [r2_r_top, s_fs(r2_r_top)],
    [r_crucible, s_bt(r_crucible)],
    r1.surf_rad,
    res_z_c2,
    res_phi,
    res_z_c1,
)
r2.set_spline_surface(s_bt, "bottom")
r2.set_spline_surface(s_fs, "side")
r3 = create_ring(
    mesh,
    [r2_r_top, s_fs(r2_r_top)],
    [r1_r_top, r1_z_top],
    c2.surf_rad,
    res_r_r1,
    res_phi,
    res_z_c2,
    faces_outside=r2.surf_top,
)
r3.set_spline_surface(s_fs, "top")

####################
# Grading
c2.set_grading_axial(grading_top)
r3.set_grading_axial(grading_top)
r2.set_grading_radial(grading_top)

c1.set_grading_axial(grading_bottom)
r1.set_grading_axial(grading_bottom)
r2.set_grading_axial(grading_bottom)

r1.set_grading_radial(grading_meniscus)
r3.set_grading_radial(grading_meniscus)

c1.set_grading_radial(grading_crys_rad)
c2.set_grading_radial(grading_crys_rad)
####################
# Patches
bt_surf = Patch(mesh, "wall meltWall")
bt_surf.faces += c1.surf_bt
bt_surf.faces += r1.surf_bt
bt_surf.faces += r2.surf_bt
free_surf = Patch(mesh, "wall freeSurf")
free_surf.faces += r2.surf_rad
free_surf.faces += r3.surf_top
top_surf = Patch(mesh, "wall crysInter")
top_surf.faces += c2.surf_top


if not one_mesh_only:
    mesh.write()
    if os.path.exists("./system/fluid/blockMeshDict"):
        os.remove("./system/fluid/blockMeshDict")
    os.rename("./system/blockMeshDict", "./system/fluid/blockMeshDict")
    mesh = Mesh()

####################
# crystal
res_z_c3, grading_crys = boundary_layer(
    l_crystal + l_conus, "xmin", smallest_element_crystal_bottom, layer_thickness_crystal_bottom, growth_rate_crystal_bottom
)
c3 = create_cylinder(
    mesh,
    [r_crystal, s_cr(r_crystal)],
    [r_crystal, s_ph(r_crystal)],
    res_r_c1,
    res_phi,
    res_z_c3,
)
c3.set_spline_surface(s_cr, "top")
c3.set_spline_surface(s_ph, "bottom")
c3.set_grading_axial(grading_crys)
c3.set_grading_radial(grading_crys_rad)

# Patches
bt_surf = Patch(mesh, "wall crysInter")
# bt_surf = Patch(mesh, "wall crysInter_crystal")
bt_surf.faces += c3.surf_bt

out_surf = Patch(mesh, "patch crysSide")
out_surf.faces += c3.surf_rad

top_surf = Patch(mesh, "patch crysEnd")
top_surf.faces += c3.surf_top


mesh.write()
if not one_mesh_only:
    if os.path.exists("./system/solid/blockMeshDict"):
        os.remove("./system/solid/blockMeshDict")
    os.rename("./system/blockMeshDict", "./system/solid/blockMeshDict")
