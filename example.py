from nemoblock import *


# initialize
mesh = Mesh()

# create patches for boundary, inlet, outlet
inlet = Patch(mesh, 'inlet inlet')
outlet = Patch(mesh, 'outlet outlet')
wall = Patch(mesh, 'wall boundary')

# create first block with points
b1 = Block(mesh, [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0 , 1], [1, 1, 1], [0, 1, 1])
b1.set_number_of_cell(10, 10, 10)
b1.grading = f"simpleGrading (1 2 3)"  # This is the default. The string is directly written into the blockMeshDict.
b1.create()  # this creates points & edges

# modify edges
b1.e0.type = "arc"
b1.e0.points.append([0.5, 0.3, 0])

# add surfaces to patches
inlet.add_face(b1.face_bottom)
wall.add_face(b1.face_left)
wall.add_face(b1.face_right)
wall.add_face(b1.face_front)
wall.add_face(b1.face_back)

# create second block on top of it
b2 = Block(mesh)  # raw block
b2.set_connection(b1, "bottom")  # on top of b1
# define missing points
b2.front_left_top = [0, 0, 2]  # alternatively, this point can be set by b2.p5 = [1, 0 ,2]
b2.front_right_top = [1, 0, 2]  # p6
b2.back_right_top = [1, 1, 2]  # p7
b2.back_left_top = [0, 1, 2]  # p8
b2.cells_x2 = 5  # the others were derived from b1
b2.create()

wall.add_face(b2.face_front)
wall.add_face(b2.face_back)
wall.add_face(b2.face_left)
wall.add_face(b2.face_top)

# create third block right of b2
b3 = Block(mesh)
b3.set_connection(b2, "left")
# define missing points
b3.p1 = [2, 0, 1]  # b3.front_right_bottom
b3.p2 = [2, 1, 1]  # b3.back_right_bottom
b3.p5 = [2, 0, 2]  # b3.back_right_top
b3.p6 = [2, 1, 2]  # b3.front_right_top
b3.cells_x0 = 5  # the others were derived from b2
b3.create()

wall.add_face(b3.face_front)
wall.add_face(b3.face_back)
wall.add_face(b3.face_bottom)
wall.add_face(b3.face_top)
outlet.add_face(b3.face_right)


# write blockMeshDict
mesh.write()
