from dataclasses import dataclass
import numpy as np
import os


class Mesh:
    """Collection of everything that belongs into the blockMeshDict."""

    def __init__(self) -> None:
        self.blocks = []
        self.block_count = 0

        self.points = []
        self.point_count = 0

        self.edges = []

        self.patches = []

    def _add_point(self, x1, x2, x3):
        p = Point(x1, x2, x3, self.point_count)
        self.point_count += 1
        self.points.append(p)
        return p

    def _add_edge(self, p0, p1):
        e = Edge(p0, p1)
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
            f.writelines(
                [
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
                ]
            )
            f.write("vertices\n(\n")
            for p in self.points:
                f.write(f"    ({p.x1} {p.x2} {p.x3})\n")
            f.write(");\n\n")
            f.write("edges\n(\n")
            for e in self.edges:
                if e.type == "line":
                    pass
                elif e.type == "arc":
                    f.write(f"    {e.type} {e.p0.id} {e.p1.id} (")
                    f.write(f"{e.points[0][0]} {e.points[0][1]} {e.points[0][2]}")
                    f.write(")\n")
                else:
                    f.write(f"    {e.type} {e.p0.id} {e.p1.id} (")
                    for p in e.points:
                        f.write(f" ({p[0]} {p[1]} {p[2]}) ")
                    f.write(")\n")
            f.write(");\n\n")
            f.write("blocks\n(\n")
            for b in self.blocks:
                f.write(
                    f"    hex ({b.p0.id} {b.p1.id} {b.p2.id} {b.p3.id} {b.p4.id} {b.p5.id} {b.p6.id} {b.p7.id})\n"
                )
                f.write(f"    ({b.cells_x1} {b.cells_x2} {b.cells_x3})\n")
                f.write(f"    {b.grading}\n")
            f.write(");\n\n")
            f.write("patches\n(\n")
            for p in self.patches:
                f.write(f"    {p.name}\n    (\n")
                for face in p.faces:
                    f.write(
                        f"    ({face[0].id} {face[1].id} {face[2].id} {face[3].id})\n"
                    )
                f.write("    )\n")
            f.write(");\n\n")
            f.write("mergePatchPairs\n(\n);\n\n")
            f.write(
                "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"
            )


class Block:
    """Block of the mesh. Naming of points and edges following openFOAM standard."""

    def __init__(
        self,
        mesh,
        p0=[0, 0, 0],
        p1=[0, 0, 0],
        p2=[0, 0, 0],
        p3=[0, 0, 0],
        p4=[0, 0, 0],
        p5=[0, 0, 0],
        p6=[0, 0, 0],
        p7=[0, 0, 0],
    ) -> None:
        self.mesh = mesh
        self.id = -1

        self._p0_coords = p0
        self._p1_coords = p1
        self._p2_coords = p2
        self._p3_coords = p3
        self._p4_coords = p4
        self._p5_coords = p5
        self._p6_coords = p6
        self._p7_coords = p7

        self._cells_x1 = 0
        self._cells_x2 = 0
        self._cells_x3 = 0
        self.grading = "simpleGrading (1 1 1)"

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
        if self._cells_x1 == 0 or self._cells_x2 == 0 or self._cells_x3 == 0:
            raise RuntimeError("Number of cells not defined.")

        if self._p0 is None:
            self._p0 = self.mesh._add_point(
                self._p0_coords[0],
                self._p0_coords[1],
                self._p0_coords[2],
            )
        if self._p1 is None:
            self._p1 = self.mesh._add_point(
                self._p1_coords[0],
                self._p1_coords[1],
                self._p1_coords[2],
            )
        if self._p2 is None:
            self._p2 = self.mesh._add_point(
                self._p2_coords[0],
                self._p2_coords[1],
                self._p2_coords[2],
            )
        if self._p3 is None:
            self._p3 = self.mesh._add_point(
                self._p3_coords[0],
                self._p3_coords[1],
                self._p3_coords[2],
            )
        if self._p4 is None:
            self._p4 = self.mesh._add_point(
                self._p4_coords[0], self._p4_coords[1], self._p4_coords[2]
            )
        if self._p5 is None:
            self._p5 = self.mesh._add_point(
                self._p5_coords[0],
                self._p5_coords[1],
                self._p5_coords[2],
            )
        if self._p6 is None:
            self._p6 = self.mesh._add_point(
                self._p6_coords[0], self._p6_coords[1], self._p6_coords[2]
            )
        if self._p7 is None:
            self._p7 = self.mesh._add_point(
                self._p7_coords[0], self._p7_coords[1], self._p7_coords[2]
            )

        if type(self._p0) is str:
            if self._p0 == "p1":
                self._p0 = self._p1
            elif self._p0 == "p2":
                self._p0 = self._p2
            elif self._p0 == "p3":
                self._p0 = self._p3
            elif self._p0 == "p4":
                self._p0 = self._p4
            elif self._p0 == "p5":
                self._p0 = self._p5
            elif self._p0 == "p6":
                self._p0 = self._p6
            elif self._p0 == "p7":
                self._p0 = self._p7
            else:
                raise ValueError("invalid point definition")
        if type(self._p1) is str:
            if self._p1 == "p0":
                self._p1 = self._p0
            elif self._p1 == "p2":
                self._p1 = self._p2
            elif self._p1 == "p3":
                self._p1 = self._p3
            elif self._p1 == "p4":
                self._p1 = self._p4
            elif self._p1 == "p5":
                self._p1 = self._p5
            elif self._p1 == "p6":
                self._p1 = self._p6
            elif self._p1 == "p7":
                self._p1 = self._p7
            else:
                raise ValueError("invalid point definition")
        if type(self._p2) is str:
            if self._p2 == "p0":
                self._p2 = self._p0
            elif self._p2 == "p1":
                self._p2 = self._p1
            elif self._p2 == "p3":
                self._p2 = self._p3
            elif self._p2 == "p4":
                self._p2 = self._p4
            elif self._p2 == "p5":
                self._p2 = self._p5
            elif self._p2 == "p6":
                self._p2 = self._p6
            elif self._p2 == "p7":
                self._p2 = self._p7
            else:
                raise ValueError("invalid point definition")
        if type(self._p3) is str:
            if self._p3 == "p0":
                self._p3 = self._p0
            elif self._p3 == "p1":
                self._p3 = self._p1
            elif self._p3 == "p2":
                self._p3 = self._p2
            elif self._p3 == "p4":
                self._p3 = self._p4
            elif self._p3 == "p5":
                self._p3 = self._p5
            elif self._p3 == "p6":
                self._p3 = self._p6
            elif self._p3 == "p7":
                self._p3 = self._p7
            else:
                raise ValueError("invalid point definition")
        if type(self._p4) is str:
            if self._p4 == "p0":
                self._p4 = self._p0
            elif self._p4 == "p1":
                self._p4 = self._p1
            elif self._p4 == "p2":
                self._p4 = self._p2
            elif self._p4 == "p3":
                self._p4 = self._p3
            elif self._p4 == "p5":
                self._p4 = self._p5
            elif self._p4 == "p6":
                self._p4 = self._p6
            elif self._p4 == "p7":
                self._p4 = self._p7
            else:
                raise ValueError("invalid point definition")
        if type(self._p5) is str:
            if self._p5 == "p0":
                self._p5 = self._p0
            elif self._p5 == "p1":
                self._p5 = self._p1
            elif self._p5 == "p2":
                self._p5 = self._p2
            elif self._p5 == "p3":
                self._p5 = self._p3
            elif self._p5 == "p4":
                self._p5 = self._p4
            elif self._p5 == "p6":
                self._p5 = self._p6
            elif self._p5 == "p7":
                self._p5 = self._p7
            else:
                raise ValueError("invalid point definition")
        if type(self._p6) is str:
            if self._p6 == "p0":
                self._p6 = self._p0
            elif self._p6 == "p1":
                self._p6 = self._p1
            elif self._p6 == "p2":
                self._p6 = self._p2
            elif self._p6 == "p3":
                self._p6 = self._p3
            elif self._p6 == "p4":
                self._p6 = self._p4
            elif self._p6 == "p5":
                self._p6 = self._p5
            elif self._p6 == "p7":
                self._p6 = self._p7
            else:
                raise ValueError("invalid point definition")
        if type(self._p7) is str:
            if self._p7 == "p0":
                self._p7 = self._p0
            elif self._p7 == "p1":
                self._p7 = self._p1
            elif self._p7 == "p2":
                self._p7 = self._p2
            elif self._p7 == "p3":
                self._p7 = self._p3
            elif self._p7 == "p4":
                self._p7 = self._p4
            elif self._p7 == "p5":
                self._p7 = self._p5
            elif self._p7 == "p6":
                self._p7 = self._p6
            else:
                raise ValueError("invalid point definition")

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
        """Set connection to other block. This works only if the
        coordinate systems have the same orientation!

        Args:
            other (Block): Block to set connection to.
            pos (str): Position of other block (respective to this one).
                       Options: top, bottom, left, right, front, back
        """
        if other._created == False:
            raise RuntimeError(
                "The other block was not created. Run other_block.create() first!"
            )
        if pos == "top":
            self._p4 = other._p0
            self._p5 = other._p1
            self._p6 = other._p2
            self._p7 = other._p3
            self.e3 = other.e0
            self.e2 = other.e1
            self.e6 = other.e5
            self.e7 = other.e4
            self._cells_x1 = other.cells_x1
            self._cells_x2 = other.cells_x2
        elif pos == "bottom":
            self._p0 = other._p4
            self._p1 = other._p5
            self._p2 = other._p6
            self._p3 = other._p7
            self.e0 = other.e3
            self.e1 = other.e2
            self.e5 = other.e6
            self.e4 = other.e7
            self._cells_x1 = other.cells_x1
            self._cells_x2 = other.cells_x2
        elif pos == "left":
            self._p0 = other._p1
            self._p3 = other._p2
            self._p4 = other._p5
            self._p7 = other._p6
            self.e4 = other.e5
            self.e7 = other.e6
            self.e8 = other.e9
            self.e11 = other.e10
            self._cells_x2 = other.cells_x2
            self._cells_x3 = other.cells_x3
        elif pos == "right":
            self._p1 = other._p0
            self._p2 = other._p3
            self._p5 = other._p4
            self._p6 = other._p7
            self.e5 = other.e4
            self.e6 = other.e7
            self.e9 = other.e8
            self.e10 = other.e11
            self._cells_x2 = other.cells_x2
            self._cells_x3 = other.cells_x3
        elif pos == "front":
            self._p0 = other._p3
            self._p1 = other._p2
            self._p4 = other._p7
            self._p5 = other._p6
            self.e0 = other.e1
            self.e3 = other.e2
            self.e8 = other.e11
            self.e9 = other.e10
            self._cells_x1 = other.cells_x1
            self._cells_x3 = other.cells_x3
        elif pos == "back":
            self._p3 = other._p0
            self._p2 = other._p1
            self._p7 = other._p4
            self._p6 = other._p5
            self.e1 = other.e0
            self.e2 = other.e3
            self.e11 = other.e8
            self.e10 = other.e9
            self._cells_x1 = other.cells_x1
            self._cells_x3 = other.cells_x3
        else:
            raise ValueError(
                "This position does not exist.\nThe following values are allowed for 'pos': top, bottom, left, right, front, back"
            )

    def set_number_of_cells(self, x1=10, x2=10, x3=10):
        self._cells_x1 = x1
        self._cells_x2 = x2
        self._cells_x3 = x3

    @property
    def cells_x1(self):
        return self._cells_x1

    @cells_x1.setter
    def cells_x1(self, val):
        if self._cells_x1 != 0:
            raise RuntimeError(
                "This value was already set or derived from a connected block."
            )
        self._cells_x1 = val

    @property
    def cells_x2(self):
        return self._cells_x2

    @cells_x2.setter
    def cells_x2(self, val):
        if self._cells_x2 != 0:
            raise RuntimeError(
                "This value was already set or derived from a connected block."
            )
        self._cells_x2 = val

    @property
    def cells_x3(self):
        return self._cells_x3

    @cells_x3.setter
    def cells_x3(self, val):
        if self._cells_x3 != 0:
            raise RuntimeError(
                "This value was already set or derived from a connected block."
            )
        self._cells_x3 = val

    @property
    def p0(self):
        return self._p0

    @p0.setter
    def p0(self, val):
        if self._p0 is not None:
            raise RuntimeError("This point exists already.")
        if type(val) == Point:
            self._p0 = val
        if type(val) == str:
            if self._created:
                raise ValueError("Cannot set reference to own point, block was already created")
            self._p0 = val
        else:
            self._p0 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, val):
        if self._p1 is not None:
            raise RuntimeError("This point exists already.")
        if type(val) == Point:
            self._p1 = val
        elif type(val) == str:
            if self._created:
                raise ValueError("Cannot set reference to own point, block was already created")
            self._p1 = val
        else:
            self._p1 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, val):
        if self._p2 is not None:
            raise RuntimeError("This point exists already.")
        if type(val) == Point:
            self._p2 = val
        elif type(val) == str:
            if self._created:
                raise ValueError("Cannot set reference to own point, block was already created")
            self._p2 = val
        else:
            self._p2 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p3(self):
        return self._p3

    @p3.setter
    def p3(self, val):
        if self._p3 is not None:
            raise RuntimeError("This point exists already.")
        if type(val) == Point:
            self._p3 = val
        elif type(val) == str:
            if self._created:
                raise ValueError("Cannot set reference to own point, block was already created")
            self._p3 = val
        else:
            self._p3 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p4(self):
        return self._p4

    @p4.setter
    def p4(self, val):
        if self._p4 is not None:
            raise RuntimeError("This point exists already.")
        if type(val) == Point:
            self._p4 = val
        elif type(val) == str:
            if self._created:
                raise ValueError("Cannot set reference to own point, block was already created")
            self._p4 = val
        else:
            self._p4 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p5(self):
        return self._p5

    @p5.setter
    def p5(self, val):
        if self._p5 is not None:
            raise RuntimeError("This point exists already.")
        if type(val) == Point:
            self._p5 = val
        elif type(val) == str:
            if self._created:
                raise ValueError("Cannot set reference to own point, block was already created")
            self._p5 = val
        else:
            self._p5 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p6(self):
        return self._p6

    @p6.setter
    def p6(self, val):
        if self._p6 is not None:
            raise RuntimeError("This point exists already.")
        if type(val) == Point:
            self._p6 = val
        elif type(val) == str:
            if self._created:
                raise ValueError("Cannot set reference to own point, block was already created")
            self._p6 = val
        else:
            self._p6 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def p7(self):
        return self._p7

    @p7.setter
    def p7(self, val):
        if self._p7 is not None:
            raise RuntimeError("This point exists already.")
        if type(val) == Point:
            self._p7 = val
        elif type(val) == str:
            if self._created:
                raise ValueError("Cannot set reference to own point, block was already created")
            self._p7 = val
        else:
            self._p7 = self.mesh._add_point(val[0], val[1], val[2])

    @property
    def face_front(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p0, self._p1, self._p5, self._p4]

    @face_front.setter
    def face_front(self, val):
        self._p1 = val[0]
        self._p0 = val[1]
        self._p4 = val[2]
        self._p5 = val[3]

    @property
    def face_back(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p2, self._p3, self._p7, self._p6]

    @face_back.setter
    def face_back(self, val):
        self._p3 = val[0]
        self._p2 = val[1]
        self._p6 = val[2]
        self._p7 = val[3]

    @property
    def face_left(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p3, self._p0, self._p4, self._p7]

    @face_left.setter
    def face_left(self, val):
        self._p0 = val[0]
        self._p3 = val[1]
        self._p7 = val[2]
        self._p4 = val[3]

    @property
    def face_right(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p1, self._p2, self._p6, self._p5]

    @face_right.setter
    def face_right(self, val):
        self._p2 = val[0]
        self._p1 = val[1]
        self._p5 = val[2]
        self._p6 = val[3]

    @property
    def face_bottom(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p2, self._p1, self._p0, self._p3]

    @face_bottom.setter
    def face_bottom(self, val):
        self._p3 = val[0]
        self._p0 = val[1]
        self._p1 = val[2]
        self._p2 = val[3]

    @property
    def face_top(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p7, self._p4, self._p5, self._p6]

    @face_top.setter
    def face_top(self, val):
        self._p6 = val[0]
        self._p5 = val[1]
        self._p4 = val[2]
        self._p7 = val[3]


@dataclass
class Point:
    """Point in the mesh."""

    x1: float
    x2: float
    x3: float
    id: int = -1

    def update_coordinates(self, coords):
        self.x1 = coords[0]
        self.x2 = coords[1]
        self.x3 = coords[2]


class Edge:
    """Edge of a block."""

    def __init__(self, p0, p1) -> None:
        self.p0 = p0
        self.p1 = p1
        self.type = "line"
        self.points = []


class Patch:
    """Patch to define boundaries."""

    def __init__(self, mesh, name) -> None:
        self.name = name
        self.faces = []
        mesh.patches.append(self)

    def add_face(self, face):
        self.faces.append(face)


def boundary_layer(
    block_size,
    pos="xmin",
    smallest_element=0.0003,
    layer_thickness=0.007,
    growth_rate=1.2,
):
    """Compute boundary layer

    Args:
        block_size (float): length of block in direction of BL
        pos (str): Coordinate position for grading
        smallest_element (float): Minimum element size (preserved)
        layer_thickness (float): Thickness of BL (modified to match number of elements).
        growth_rate (float): Growth rate of element size in BL.

    Returns:
        number of elements, grading-string
    """
    if growth_rate < 1:
        growth_rate = 1 / growth_rate
    # compute number of elements in boundary layer
    if growth_rate == 1:
        n_el_bl = int(np.ceil(layer_thickness / smallest_element))
    else:
        n_el_bl = int(
            np.ceil(
                np.log(1 - layer_thickness * (1 - growth_rate) / smallest_element)
                / np.log(growth_rate)
            )
        )
    # update layer thickness to match rounded number of elements
    if growth_rate == 1:
        layer_thickness = smallest_element * n_el_bl
    else:
        layer_thickness = (
            smallest_element * (1 - growth_rate ** n_el_bl) / (1 - growth_rate)
        )
    # maximum element size
    if growth_rate == 1:
        largest_element = smallest_element
    else:
        largest_element = smallest_element * growth_rate ** (n_el_bl - 1)
    # number of elements outside of boundary layer
    n_el_out = int((block_size - layer_thickness) / largest_element)
    n_el = n_el_bl + n_el_out

    if pos == "xmin":
        grading = f"( ({layer_thickness / block_size} {n_el_bl} {growth_rate**(n_el_bl-1)}) ({(block_size-layer_thickness)/block_size} {n_el_out} 1) )"
    elif pos == "xmax":
        grading = f"( ({(block_size-layer_thickness)/block_size} {n_el_out} 1) ({layer_thickness/block_size} {n_el_bl} {1/growth_rate**(n_el_bl-1)}) )"
    else:
        raise ValueError(f"Position '{pos}'' not defined. Use either 'xmin' or 'xmax'")
    print("Elements in BL:", n_el_bl)
    print("Elements outside:", n_el_out)
    print("Layer thickness:", layer_thickness)
    print("Larges Element:", largest_element)
    if n_el_out <= 0 or n_el_bl <= 0:
        raise ValueError("Impossible grading!")
    return n_el, grading
