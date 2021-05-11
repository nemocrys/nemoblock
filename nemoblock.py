from dataclasses import dataclass
import numpy as np
import os


class Mesh:
    def __init__(self) -> None:
        self.blocks = []
        self.block_count = 0

        self.points = []
        self.point_count = 0

        self.edges = []
        self.edge_count = 0

        self.patches = []

    def _add_point(self, x0, x1, x2):
        p = Point(x0, x1, x2, self.point_count)
        self.point_count += 1
        self.points.append(p)
        return p

    def _add_edge(self, p0, p1):
        e = Edge(p0, p1, self.edge_count)
        self.edge_count += 1
        self.edges.append(e)
        return e
    
    def _add_block(self, block):
        block.id = self.block_count
        self.block_count += 1
        self.blocks.append(block)

    def write(self):
        if not os.path.exists("./system"):
            os.makedirs("./system")
        with open("./system/blockMeshDict", "w") as f:
            # header
            f.writelines([
                "FoamFile\n",
                "{\n",
                "    version     2.0;\n",
                "    format      ascii;\n",
                "    class       dictionary;\n",
                "    object      blockMeshDict;\n",
                "}\n",
                "\n",
                "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n",
                "\n",
                "convertToMeters 1.0;\n",
                "\n",
                            ])
            f.write("vertices\n(\n")
            for p in self.points:
                f.write(f"    ({p.x0} {p.x1} {p.x2})\n")
            f.write(");\n\n")
            f.write("edges\n(\n")
            for e in self.edges:
                f.write(f"    {e.type} {e.p0.id} {e.p1.id} (")
                for p in e.points:
                    f.write(f" ({p[0]} {p[1]} {p[2]}) ")
                f.write(")\n")
            f.write(");\n\n")
            f.write("blocks\n(\n")
            for b in self.blocks:
                f.write(f"    hex ({b.p0.id} {b.p1.id} {b.p2.id} {b.p3.id} {b.p4.id} {b.p5.id} {b.p6.id} {b.p7.id})\n")
                f.write(f"    ({b.cells_x0} {b.cells_x1} {b.cells_x2})\n")
                f.write(f"    {b.grading}\n")
            f.write(");\n\n")
            f.write("patches\n(\n")
            for p in self.patches:
                f.write(f"    {p.name}\n    (\n")
                for face in p._faces:
                    f.write(f"    ({face[0].id} {face[1].id} {face[2].id} {face[3].id})\n")
                f.write("    )\n")
            f.write(");\n\n")
            f.write("mergePatchPairs\n(\n);\n\n")
            f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")



class Block:
    def __init__(
        self,
        mesh,
        front_left_bottom=[0, 0, 0],
        front_right_bottom=[0, 0, 0],
        back_right_bottom=[0, 0, 0],
        back_left_bottom=[0, 0, 0],
        front_left_top=[0, 0, 0],
        front_right_top=[0, 0, 0],
        back_right_top=[0, 0, 0],
        back_left_top=[0, 0, 0],
    ) -> None:
        self.mesh = mesh
        self.id = -1

        self.front_left_bottom = front_left_bottom
        self.front_right_bottom = front_right_bottom
        self.back_right_bottom = back_right_bottom
        self.back_left_bottom = back_left_bottom
        self.front_left_top = front_left_top
        self.front_right_top = front_right_top
        self.back_right_top = back_right_top
        self.back_left_top = back_left_top

        self._cells_x0 = 0
        self._cells_x1 = 0
        self._cells_x2 = 0
        self.grading = "simpleGrading (1 2 3)"

        self._p0 = None
        self._p1 = None
        self._p2 = None
        self._p3 = None
        self._p4 = None
        self._p5 = None
        self._p6 = None
        self._p7 = None

        self.e0 = None
        self.e1 = None
        self.e2 = None
        self.e3 = None
        self.e4 = None
        self.e5 = None
        self.e6 = None
        self.e7 = None
        self.e8 = None
        self.e9 = None
        self.e10 = None
        self.e11 = None

        self._created = False

    def create(self):
        """Create points and edges"""
        if self._created:
            raise RuntimeError("This block was already crated.")
        if self._cells_x0 == 0 or self._cells_x1 == 0 or self._cells_x2 == 0:
            raise RuntimeError("Number of cells not defined.")

        if self._p0 is None:
            self._p0 = self.mesh._add_point(
                self.front_left_bottom[0], self.front_left_bottom[1], self.front_left_bottom[2]
            )
        if self._p1 is None:
            self._p1 = self.mesh._add_point(
                self.front_right_bottom[0], self.front_right_bottom[1], self.front_right_bottom[2]
            )
        if self._p2 is None:
            self._p2 = self.mesh._add_point(
                self.back_right_bottom[0], self.back_right_bottom[1], self.back_right_bottom[2]
            )
        if self._p3 is None:
            self._p3 = self.mesh._add_point(
                self.back_left_bottom[0], self.back_left_bottom[1], self.back_left_bottom[2]
            )
        if self._p4 is None:
            self._p4 = self.mesh._add_point(
                self.front_left_top[0], self.front_left_top[1], self.front_left_top[2]
            )
        if self._p5 is None:
            self._p5 = self.mesh._add_point(
                self.front_right_top[0], self.front_right_top[1], self.front_right_top[2]
            )
        if self._p6 is None:
            self._p6 = self.mesh._add_point(
                self.back_right_top[0], self.back_right_top[1], self.back_right_top[2]
            )
        if self._p7 is None:
            self._p7 = self.mesh._add_point(self.back_left_top[0], self.back_left_top[1], self.back_left_top[2])

        if self.e0 is None:
            self.e0 = self.mesh._add_edge(self._p0, self._p1)
        if self.e1 is None:
            self.e1 = self.mesh._add_edge(self._p3, self._p2)
        if self.e2 is None:
            self.e2 = self.mesh._add_edge(self._p7, self._p6)
        if self.e3 is None:
            self.e3 = self.mesh._add_edge(self._p4, self._p5)
        if self.e4 is None:
            self.e4 = self.mesh._add_edge(self._p0, self._p3)
        if self.e5 is None:
            self.e5 = self.mesh._add_edge(self._p1, self._p2)
        if self.e6 is None:
            self.e6 = self.mesh._add_edge(self._p5, self._p6)
        if self.e7 is None:
            self.e7 = self.mesh._add_edge(self._p4, self._p7)
        if self.e8 is None:
            self.e8 = self.mesh._add_edge(self._p0, self._p4)
        if self.e9 is None:
            self.e9 = self.mesh._add_edge(self._p1, self._p5)
        if self.e10 is None:
            self.e10 = self.mesh._add_edge(self._p2, self._p6)
        if self.e11 is None:
            self.e11 = self.mesh._add_edge(self._p3, self._p7)
        self._created = True
        self.mesh._add_block(self)

    def set_connection(self, other, pos):
        """Set connection to other block.

        Args:
            other (Block): Block to set connection to.
            pos (str): Position of other block (respective to this one).
                       Options: top, bottom, left, right, front, back
        """
        if other._created == False:
            raise RuntimeError("The other block was not created. Run other_block.create() first!")
        if pos == "top":
            self._p4 = other._p0
            self._p5 = other._p1
            self._p6 = other._p2
            self._p7 = other._p3
            self.e3 = other.e0
            self.e2 = other.e1
            self.e6 = other.e5
            self.e7 = other.e4
            self.cells_x0 = other.cells_x0
            self.cells_x1 = other.cells_x1
        elif pos == "bottom":
            self._p0 = other._p4
            self._p1 = other._p5
            self._p2 = other._p6
            self._p3 = other._p7
            self.e0 = other.e3
            self.e1 = other.e2
            self.e5 = other.e6
            self.e4 = other.e7
            self.cells_x0 = other.cells_x0
            self.cells_x1 = other.cells_x1
        elif pos == "left":
            self._p0 = other._p1
            self._p3 = other._p2
            self._p4 = other._p5
            self._p7 = other._p6
            self.e4 = other.e5
            self.e7 = other.e6
            self.e8 = other.e9
            self.e11 = other.e10
            self.cells_x1 = other.cells_x1
            self.cells_x2 = other.cells_x2
        elif pos == "right":
            self._p1 = other._p0
            self._p2 = other._p3
            self._p5 = other._p4
            self._p6 = other._p7
            self.e5 = other.e4
            self.e6 = other.e7
            self.e9 = other.e8
            self.e10 = other.e11
            self.cells_x1 = other.cells_x1
            self.cells_x2 = other.cells_x2
        elif pos == "front":
            self._p0 = other._p3
            self._p1 = other._p2
            self._p4 = other._p7
            self._p5 = other._p6
            self.e0 = other.e1
            self.e3 = other.e2
            self.e8 = other.e11
            self.e9 = other.e10
            self.cells_x0 = other.cells_x0
            self.cells_x2 = other.cells_x2
        elif pos == "back":
            self._p3 = other._p0
            self._p2 = other._p1
            self._p7 = other._p4
            self._p6 = other._p5
            self.e1 = other.e0
            self.e2 = other.e3
            self.e11 = other.e8
            self.e10 = other.e9
            self.cells_x0 = other.cells_x0
            self.cells_x2 = other.cells_x2
        else:
            raise ValueError("This position does not exist.\nThe following values are allowed for 'pos': top, bottom, left, right, front, back")

    def set_number_of_cell(self, x0=10, x1=10, x2=10):
        if self._cells_x0 != 0 or self._cells_x1 != 0 or self.cells_x2 != 0:
            raise RuntimeError("Values were already set or derived from a connected block.")
        self._cells_x0 = x0
        self._cells_x1 = x1
        self._cells_x2 = x2

    @property
    def cells_x0(self):
        return self._cells_x0

    @cells_x0.setter
    def cells_x0(self, val):
        if self._cells_x0 != 0:
            raise RuntimeError("This value was already set or derived from a connected block.")
        self._cells_x0 = val
    
    @property
    def cells_x1(self):
        return self._cells_x1

    @cells_x1.setter
    def cells_x1(self, val):
        if self._cells_x1 != 0:
            raise RuntimeError("This value was already set or derived from a connected block.")
        self._cells_x1 = val

    @property
    def cells_x2(self):
        return self._cells_x2

    @cells_x2.setter
    def cells_x2(self, val):
        if self._cells_x2 != 0:
            raise RuntimeError("This value was already set or derived from a connected block.")
        self._cells_x2 = val

    @property
    def edge_frontside_bottom(self):
        if self._created:
            return self.e0
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_frontside_top(self):
        if self._created:
            return self.e3
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_frontside_left(self):
        if self._created:
            return self.e8
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_edge_frontside_right(self):
        if self._created:
            return self.e9
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_leftside_bottom(self):
        if self._created:
            return self.e4
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_leftside_top(self):
        if self._created:
            return self.e7
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_leftside_front(self):
        if self._created:
            return self.e8
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_leftside_back(self):
        if self._created:
            return self.e11
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_leftside_back(self):
        if self._created:
            return self.e11
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_rightside_bottom(self):
        if self._created:
            return self.e5
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_rightside_top(self):
        if self._created:
            return self.e10
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_rightside_front(self):
        if self._created:
            return self.e9
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_rightside_back(self):
        if self._created:
            return self.e10
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_backside_bottom(self):
        if self._created:
            return self.e1
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_backside_top(self):
        if self._created:
            return self.e2
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_backside_left(self):
        if self._created:
            return self.e11
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def edge_backside_right(self):
        if self._created:
            return self.e10
        else:
            raise RuntimeError("Edges were not created.")

    @property
    def p0(self):
        return self._p0

    @p0.setter
    def p0(self, val):
        self._p0 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, val):
        self._p1 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, val):
        self._p2 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p3(self):
        return self._p3

    @p3.setter
    def p3(self, val):
        self._p3 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p4(self):
        return self._p4

    @p4.setter
    def p4(self, val):
        self._p4 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p5(self):
        return self._p5

    @p5.setter
    def p5(self, val):
        self._p5 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p6(self):
        return self._p6

    @p6.setter
    def p6(self, val):
        self._p6 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p7(self):
        return self._p7

    @p7.setter
    def p7(self, val):
        self._p7 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def face_front(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p0, self._p1, self._p5, self._p4]

    @property
    def face_back(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p3, self._p7, self._p6, self._p2]

    @property
    def face_left(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p0, self._p4, self._p7, self._p3]

    @property
    def face_right(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p1, self._p2, self._p6, self._p5]

    @property
    def face_bottom(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p0, self._p3, self._p2, self._p1]

    @property
    def face_top(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p4, self._p5, self._p6, self._p7]


@dataclass
class Point:
    x0: float
    x1: float
    x2: float
    id: int = -1

class Edge:
    def __init__(self, p0, p1, id=-1) -> None:
        self.p0 = p0
        self.p1 = p1
        self.id = id
        self.type = "line"
        self.points = []

class Patch:
    def __init__(self, mesh, name) -> None:
        self.name = name
        self._faces = []
        mesh.patches.append(self)

    def add_face(self, face):
        self._faces.append(face)

