from nemoblock import *


mesh = Mesh()


####################
# fmt: off
#
# Mes structure (left: symmetry axis)
#  __
# |  | \
# |  |    \
# |c2| r3 / \
# |__|___/    \
# |  |   \ r2 /
# |c1| r1 \  /
# |__|_____\/
# 
#
# coordinate system:
#
# ^ z-direction
# | 
# |
# |------->
#   r-direction 
#  
# fmt: on
#
####################
# Geometry parameter
####################
# cylinder c1
#
# fmt: off
#            z_c1_bt_mid
#  --------- r_c1_top/2 ---------   r_c1_top, z_c1_top
#  _____________ __________________ 
# |             |                  |
# |        cylinder c1             |
# |_____________|__________________|
#  ----s1-- r_c1_bt/2  ----s2----   r_c1_bt, z_c1_bt
#           z_c1_bt_mid
# fmt: on
# 
# This cylinder consists of a octagonal core ranging from radius 0 to r/2 and a surronding ring from r/2 to r.
# The bottom surface can be given in form of a spline defined by [r, z] points for the lines s1 (inner part) and s2 (outer part).

r_c1_bt = 0.1
z_c1_bt = 0.0
z_c1_bt_mid = 0.0

r_c1_top = 0.1
z_c1_top = 0.3
z_c1_top_mid = z_c1_top

s1_c1 = [[0.01, -0.01], [0.02, -0.03], [0.03, -0.02], [0.04, -0.01]]
s2_c1 = [[0.075, 0.01]]

# ring r1
r_r1_bt = 0.25
r_r1_top = 0.2
z_r1_bt = 0.05
z_r1_top = z_c1_top

# ring r2
r_r2_bt = 0.5  # crystal diameter (FZ)
r_r2_top = 0.25
z_r2_bt = z_c1_top
z_r2_top = 0.4


####################
# Mesh parameters
res_phi = 180  # 2° angle

res_r_c1 = 20  # applies also for c2
res_z_c1 = 10  # applies also for r1, r2

res_r_r1 = 50  # applies also fro r3

res_r_r2 = 50  # applies also for r3, c2 

####################
# Patches
top_surf = Patch(mesh, "wall topSurf")
bt_surf = Patch(mesh, "wall BottomSurf")
free_surf = Patch(mesh, "wall FreeSurf")

####################
# Central cylinder
c1 = create_cylinder(mesh, r_c1_top, r_c1_bt, z_c1_top, z_c1_bt, z_c1_top_mid, z_c1_bt_mid, res_r_c1, res_phi, res_z_c1, s_in_bt=s1_c1, s_out_bt=s2_c1)

# r1 = create_ring(mesh, r_r1_top, r_r1_bt, z_r1_top, z_r1_bt, c1.surf_rad, res_r_r1, res_phi, res_z_c1)

# r2 = create_ring(mesh, r_r2_top, r_r2_bt, z_r2_top, z_r2_bt, r1.surf_rad, res_r_r2, res_phi, res_z_c1)

# c2 = create_cylinder_on_top()

# c3 = create_ring_in_between()

mesh.write()
