"Example for creating blocks. Similar to the code in the main readme."

from nemoblock import *

mesh = Mesh()
inlet = Patch(mesh, "inlet inlet1")
b1 = Block(
    mesh,
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1],
)  # points p0 to p7 here
b1.set_number_of_cells(10, 10, 10)
b1.create()
b1.e0.type = "spline"
b1.e0.points.append([0.5, 0.3, 0])
inlet.add_face(b1.face_bottom)
b2 = Block(mesh)
b2.set_connection(b1, "bottom")  # on top of b1
b2.p4 = [0, 0, 2]
b2.p5 = [1, 0, 2]
b2.p6 = [1, 1, 2]
b2.p7 = [0, 1, 2]
b2.cells_x3 = 5  # the others were derived from b1
b2.create()
mesh.write()
