from nemoblock import *

mesh = Mesh()

# dimensions
cruc_r = 0.06  # crucible radius
cruc_h = 0.03  # crucible height
cruc_hi = 0.015  # crucible height inside
melt_r = 0.025  # melt radius
melt_h = 0.01  # melt height
crys_r = 0.005  # crystal radius
crys_h = 0.1  # crystal height
t = 1e-2

crys = Block(
    mesh,
    [0, 0, melt_h],
    [crys_r, 0, melt_h],
    [crys_r, t, melt_h],
    [0, t, melt_h],
    [0, 0, melt_h + crys_h],
    [crys_r, 0, melt_h + crys_h],
    [crys_r, t, melt_h + crys_h],
    [0, t, melt_h + crys_h],
)
crys.set_number_of_cells(5, 1, 60)
crys.create()

melt1 = Block(mesh)
melt1.set_connection(crys, "top")
melt1.p0 = [0, 0, 0]
melt1.p1 = [crys_r, 0, 0]
melt1.p2 = [crys_r, t, 0]
melt1.p3 = [0, t, 0]
melt1.cells_x3 = 15
melt1.create()

melt2 = Block(mesh)
melt2.set_connection(melt1, "left")
melt2.p1 = [melt_r, 0, 0]
melt2.p2 = [melt_r, t, 0]
melt2.p5 = [melt_r, 0, melt_h]
melt2.p6 = [melt_r, t, melt_h]
melt2.cells_x1 = 15
melt2.create()

cruc_bot1 = Block(mesh)
cruc_bot1.set_connection(melt1, "top")
cruc_bot1.p0 = [0, 0, -(cruc_h - cruc_hi)]
cruc_bot1.p1 = [crys_r*2, 0, -(cruc_h - cruc_hi)]
cruc_bot1.p2 = [crys_r*2, t, -(cruc_h - cruc_hi)]
cruc_bot1.p3 = [0, t, -(cruc_h - cruc_hi)]
cruc_bot1.cells_x3 = 5
cruc_bot1.create()

cruc_bot2 = Block(mesh)
cruc_bot2.set_connection(melt2, "top")
cruc_bot2.set_connection(cruc_bot1, "left")
cruc_bot2.p1 = [cruc_r, 0, -(cruc_h - cruc_hi)]
cruc_bot2.p2 = [cruc_r, t, -(cruc_h - cruc_hi)]
cruc_bot2.create()

cruc_wall1 = Block(mesh)
cruc_wall1.set_connection(melt2, "left")
cruc_wall1.p1 = cruc_bot2.p1
cruc_wall1.p2 = cruc_bot2.p2
cruc_wall1.p5 = [cruc_r, 0, melt_h]
cruc_wall1.p6 = [cruc_r, t, melt_h]
cruc_wall1.cells_x1 = cruc_bot2.cells_x3
cruc_wall1.create()

cruc_wall2 = Block(mesh)
cruc_wall2.set_connection(cruc_wall1, "bottom")
cruc_wall2.p4 = [melt_r, 0, cruc_hi]
cruc_wall2.p5 = [cruc_r, 0, cruc_hi]
cruc_wall2.p6 = [cruc_r, t, cruc_hi]
cruc_wall2.p7 = [melt_r, t, cruc_hi]
cruc_wall2.cells_x3 = 4
cruc_wall2.create()

mesh.write()
