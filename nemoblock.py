from dataclasses import dataclass
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


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
                f.write(f"    hex ({b.p0.id} {b.p1.id} {b.p2.id} {b.p3.id} {b.p4.id} {b.p5.id} {b.p6.id} {b.p7.id})\n")
                f.write(f"    ({b.cells_x0} {b.cells_x1} {b.cells_x2})\n")
                f.write(f"    {b.grading}\n")
            f.write(");\n\n")
            f.write("patches\n(\n")
            for p in self.patches:
                f.write(f"    {p.name}\n    (\n")
                for face in p.faces:
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
            self._cells_x0 = other.cells_x0
            self._cells_x1 = other.cells_x1
        elif pos == "bottom":
            self._p0 = other._p4
            self._p1 = other._p5
            self._p2 = other._p6
            self._p3 = other._p7
            self.e0 = other.e3
            self.e1 = other.e2
            self.e5 = other.e6
            self.e4 = other.e7
            self._cells_x0 = other.cells_x0
            self._cells_x1 = other.cells_x1
        elif pos == "left":
            self._p0 = other._p1
            self._p3 = other._p2
            self._p4 = other._p5
            self._p7 = other._p6
            self.e4 = other.e5
            self.e7 = other.e6
            self.e8 = other.e9
            self.e11 = other.e10
            self._cells_x1 = other.cells_x1
            self._cells_x2 = other.cells_x2
        elif pos == "right":
            self._p1 = other._p0
            self._p2 = other._p3
            self._p5 = other._p4
            self._p6 = other._p7
            self.e5 = other.e4
            self.e6 = other.e7
            self.e9 = other.e8
            self.e10 = other.e11
            self._cells_x1 = other.cells_x1
            self._cells_x2 = other.cells_x2
        elif pos == "front":
            self._p0 = other._p3
            self._p1 = other._p2
            self._p4 = other._p7
            self._p5 = other._p6
            self.e0 = other.e1
            self.e3 = other.e2
            self.e8 = other.e11
            self.e9 = other.e10
            self._cells_x0 = other.cells_x0
            self._cells_x2 = other.cells_x2
        elif pos == "back":
            self._p3 = other._p0
            self._p2 = other._p1
            self._p7 = other._p4
            self._p6 = other._p5
            self.e1 = other.e0
            self.e2 = other.e3
            self.e11 = other.e8
            self.e10 = other.e9
            self._cells_x0 = other.cells_x0
            self._cells_x2 = other.cells_x2
        else:
            raise ValueError("This position does not exist.\nThe following values are allowed for 'pos': top, bottom, left, right, front, back")

    def set_number_of_cell(self, x0=10, x1=10, x2=10):
        # if self._cells_x0 != 0 or self._cells_x1 != 0 or self.cells_x2 != 0:
        #     raise RuntimeError("Values were already set or derived from a connected block.")
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
        return [self._p3, self._p2, self._p1, self._p0]

    @property
    def face_top(self):
        if not self._created:
            raise RuntimeError("This block was not created yet.")
        return [self._p7, self._p4, self._p5, self._p6]


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
        self.faces = []
        mesh.patches.append(self)

    def add_face(self, face):
        self.faces.append(face)

@dataclass
class Ring:
    blocks: list
    surf_top: list
    surf_bt: list
    surf_rad: list

@dataclass
class Cylinder:
    core: Block
    ring: Ring
    surf_top: list
    surf_bt: list
    surf_rad: list
    

def cartesian(r, phi, z, degree=True):
    if degree:
        phi = 2*np.pi * phi / 360
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return [x, y, z]


def spline(points, kind='cubic'):
    """Create a spline functions

    Args:
        points (list): list of [r, z] coordinates
    """
    points = np.array(points)
    return interp1d(points[:, 0], points[:, 1], kind=kind)

def plot_spline(sp, r, fig=None, ax=None):
    if fig is None:
        fig, ax = plt.subplots(1, 1)
    r = np.linspace(r[0], r[1], 100)
    ax.plot(r, sp(r))
    return fig, ax




def create_cylinder(mesh, r_top, r_bt, z_top, z_bt, res_r, res_phi, res_z, radius_ratio=0.5, spline_res=100, cylinder_below=None, cylinder_on_top=None):
    if cylinder_below is not None and cylinder_on_top is not None:
        raise ValueError("Both cylinder on top and below is not possible.")
    
    # Central block
    radius_center_top = r_top * radius_ratio
    radius_center_bt = r_bt * radius_ratio

    if type(z_bt) is interp1d:
        z_bt_mid = z_bt(radius_center_bt)
    else:
        z_bt_mid = z_bt
    if type(z_top) is interp1d:
        z_top_mid = z_top(radius_center_top)
    else:
        z_top_mid = z_top

    res_center_r = int(res_phi / 4)

    if cylinder_below is not None:
        b = Block(mesh)
        b.set_connection(cylinder_below.core, 'bottom')
        b.p4 = cartesian(radius_center_top, 0, z_top_mid)
        b.p5 = cartesian(radius_center_top, 90, z_top_mid)
        b.p6 = cartesian(radius_center_top, 180, z_top_mid)
        b.p7 = cartesian(radius_center_top, 270, z_top_mid)
    elif cylinder_on_top is not None:
        b = Block(mesh)
        b.set_connection(cylinder_on_top.core, 'top')
        b.p0 = cartesian(radius_center_bt, 0, z_bt_mid)
        b.p1 = cartesian(radius_center_bt, 90, z_bt_mid)
        b.p2 = cartesian(radius_center_bt, 180, z_bt_mid)
        b.p3 = cartesian(radius_center_bt, 270, z_bt_mid)
    else:
        b = Block(
            mesh,
            cartesian(radius_center_bt, 0, z_bt_mid),
            cartesian(radius_center_bt, 90, z_bt_mid),
            cartesian(radius_center_bt, 180, z_bt_mid),
            cartesian(radius_center_bt, 270, z_bt_mid),
            cartesian(radius_center_top, 0, z_top_mid),
            cartesian(radius_center_top, 90, z_top_mid),
            cartesian(radius_center_top, 180, z_top_mid),
            cartesian(radius_center_top, 270, z_top_mid)
        )
    b.set_number_of_cell(res_center_r, res_center_r, res_z)
    b.create()

    # Spline on bottom edges
    if type(z_bt) is interp1d:
        x0 = np.array(cartesian(radius_center_bt, 0, z_bt_mid))
        x1 = np.array(cartesian(radius_center_bt, 90, z_bt_mid))
        radii = []
        phis = []
        for dist in np.linspace(0, 1, spline_res, endpoint=False):
            pos = x0 + dist*(x1-x0)
            radii.append((pos[0]**2 + pos[1]**2)**0.5)
            phis.append(np.arctan(pos[1]/pos[0])*360/(2*np.pi))
        z_vals = z_bt(radii)
        
        b.e0.type = "spline"
        b.e5.type = "spline"
        b.e1.type = "spline"
        b.e4.type = "spline"
        for i in range(len(radii) - 1):
            b.e0.points.append(cartesian(radii[i+1], phis[i+1], z_vals[i+1]))
            b.e5.points.append(cartesian(radii[i+1], phis[i+1] + 90, z_vals[i+1]))
            b.e1.points.append(cartesian(radii[i+1], 270 - phis[i+1], z_vals[i+1]))
            b.e4.points.append(cartesian(radii[i+1], 360 - phis[i+1], z_vals[i+1]))

    if type(z_top) is interp1d:
        x0 = np.array(cartesian(radius_center_bt, 0, z_top_mid))
        x1 = np.array(cartesian(radius_center_bt, 90, z_top_mid))
        radii = []
        phis = []
        for dist in np.linspace(0, 1, spline_res, endpoint=False):
            pos = x0 + dist*(x1-x0)
            radii.append((pos[0]**2 + pos[1]**2)**0.5)
            phis.append(np.arctan(pos[1]/pos[0])*360/(2*np.pi))
        z_vals = z_top(radii)

        b.e3.type = "spline"
        b.e6.type = "spline"
        b.e2.type = "spline"
        b.e7.type = "spline"

        for i in range(len(radii) - 1):
            b.e3.points.append(cartesian(radii[i+1], phis[i+1], z_vals[i+1]))
            b.e6.points.append(cartesian(radii[i+1], phis[i+1] + 90, z_vals[i+1]))
            b.e2.points.append(cartesian(radii[i+1], 270 - phis[i+1], z_vals[i+1]))
            b.e7.points.append(cartesian(radii[i+1], 360 - phis[i+1], z_vals[i+1]))

    # create ring around these blocks
    ring_below = None
    ring_on_top = None
    if cylinder_below is not None:
        ring_below = cylinder_below.ring
    if cylinder_on_top is not None:
        ring_on_top = cylinder_on_top.ring
    ring = create_ring(mesh, r_top, radius_center_top, r_bt, radius_center_bt, z_top, z_bt, [b.face_front, b.face_right, b.face_back, b.face_left], res_r, res_phi, res_z, spline_res, ring_below=ring_below, ring_on_top=ring_on_top)
    surf_top = [b.face_top] + ring.surf_top
    surf_bt = [b.face_bottom] + ring.surf_bt

    return Cylinder(b, ring, surf_top, surf_bt, ring.surf_rad)


def create_ring(mesh, r_top, r_in_top, r_bt, r_in_bt, z_top, z_bt, faces_inside, res_r, res_phi, res_z, spline_res=100, spline_outside=None, ring_below=None, ring_on_top=None, faces_outside=[]):
    
    if ring_below is not None and ring_on_top is not None:
        raise ValueError("It's not allowed to provide both ring_on_top and ring_below.")

    if type(z_bt) is interp1d:
        z_bt_out = z_bt(r_bt)
    else:
        z_bt_out = z_bt
    if type(z_top) is interp1d:
        z_top_out = z_top(r_top)
    else:
        z_top_out = z_top

    blocks = []
    
    b = Block(mesh)
    b.face_left = faces_inside[0]
    if faces_outside != []:
        b.face_right = faces_outside[0]
        b.set_number_of_cell(res_r, int(res_phi/4), res_z)
        b.create()
    elif ring_below is not None:
        b.set_connection(ring_below.blocks[0], 'bottom')
        b.p5 = cartesian(r_top, 0, z_top_out)
        b.p6 = cartesian(r_top, 90, z_top_out)
        b.set_number_of_cell(res_r, int(res_phi/4), res_z)
        b.create()
        b.e6.type = "arc"
        b.e6.points = [cartesian(r_top, 45, z_top_out)]
    elif ring_on_top is not None:
        b.set_connection(ring_on_top[0], 'top')
        b.p1 = cartesian(r_bt, 0, z_bt_out)
        b.p2 = cartesian(r_bt, 90, z_bt_out)
        b.set_number_of_cell(res_r, int(res_phi/4), res_z)
        b.create()
        b.e5.type = "arc"
        b.e5.points = [cartesian(r_bt, 45, z_bt_out)]
    else:
        b.p1 = cartesian(r_bt, 0, z_bt_out)
        b.p2 = cartesian(r_bt, 90, z_bt_out)
        b.p5 = cartesian(r_top, 0, z_top_out)
        b.p6 = cartesian(r_top, 90, z_top_out)
        b.set_number_of_cell(res_r, int(res_phi/4), res_z)
        b.create()
        b.e5.type = "arc"
        b.e5.points = [cartesian(r_bt, 45, z_bt_out)]
        b.e6.type = "arc"
        b.e6.points = [cartesian(r_top, 45, z_top_out)]
    blocks.append(b)

    for i in range(2):
        i+=1
        b = Block(mesh)
        b.face_left = faces_inside[i]
        b.face_front = blocks[i-1].face_back
        if faces_outside != []:
            b.face_right = faces_outside[i]
            b.set_number_of_cell(res_r, int(res_phi/4), res_z)
            b.create()
        elif ring_below is not None:
            b.set_connection(ring_below.blocks[i], 'bottom')
            b.p6 = cartesian(r_top, 90*(i+1), z_top_out)
            b.set_number_of_cell(res_r, int(res_phi/4), res_z)
            b.create()
            b.e6.type = "arc"
            b.e6.points = [cartesian(r_top, i*90 + 45, z_top_out)]
        elif ring_on_top is not None:
            b.set_connection(ring_on_top.blocks[i], 'top')
            b.p2 = cartesian(r_bt, 90*(i+1), z_bt_out)
            b.set_number_of_cell(res_r, int(res_phi/4), res_z)
            b.create()
            b.e5.type = "arc"
            b.e5.points = [cartesian(r_bt, i*90 + 45, z_bt_out)]
        else:
            b.p2 = cartesian(r_bt, 90*(i+1), z_bt_out)
            b.p6 = cartesian(r_top, 90*(i+1), z_top_out)
            b.set_number_of_cell(res_r, int(res_phi/4), res_z)
            b.create()
            b.e5.type = "arc"
            b.e5.points = [cartesian(r_bt, i*90 + 45, z_bt_out)]
            b.e6.type = "arc"
            b.e6.points = [cartesian(r_top, i*90 + 45, z_top_out)]
        blocks.append(b)

    b = Block(mesh)
    b.face_left = faces_inside[-1]
    b.face_front = blocks[-1].face_back
    b.face_back = blocks[0].face_front
    b.set_number_of_cell(res_r, int(res_phi/4), res_z)
    b.create()
    if faces_outside != []:
        pass
    elif ring_below is not None:
        b.e6.type = "arc"
        b.e6.points = [cartesian(r_top, 360 - 45, z_top_out)]
    elif ring_on_top is not None:
        b.e5.type = "arc"
        b.e5.points = [cartesian(r_bt, 360 - 45, z_bt_out)]
    else:
        b.e5.type = "arc"
        b.e5.points = [cartesian(r_bt, 360 - 45, z_bt_out)]
        b.e6.type = "arc"
        b.e6.points = [cartesian(r_top, 360 - 45, z_top_out)]
    blocks.append(b)

    if type(z_bt) is interp1d:
        for b in blocks:
            b.e0.type = "spline"
        for r in np.linspace(r_in_bt, r_bt, spline_res, endpoint=False):
            blocks[0].e0.points.append(cartesian(r, 0, z_bt(r)))
            blocks[1].e0.points.append(cartesian(r, 90, z_bt(r)))
            blocks[2].e0.points.append(cartesian(r, 180, z_bt(r)))
            blocks[3].e0.points.append(cartesian(r, 270, z_bt(r)))

    if type(z_top) is interp1d:
        for b in blocks:
            b.e3.type = "spline"
        for r in np.linspace(r_in_top, r_top, spline_res, endpoint=False):
            blocks[0].e3.points.append(cartesian(r, 0, z_top(r)))
            blocks[1].e3.points.append(cartesian(r, 90, z_top(r)))
            blocks[2].e3.points.append(cartesian(r, 180, z_top(r)))
            blocks[3].e3.points.append(cartesian(r, 270, z_top(r)))

    if spline_outside is not None:
        for b in blocks:
            b.e9.type = "spline"
        for r in np.linspace(r_bt, r_top, spline_res):
            blocks[0].e9.points.append(cartesian(r, 0, spline_outside(r)))
            blocks[1].e9.points.append(cartesian(r, 90, spline_outside(r)))
            blocks[2].e9.points.append(cartesian(r, 180, spline_outside(r)))
            blocks[3].e9.points.append(cartesian(r, 270, spline_outside(r)))

    surf_top = []
    surf_bt = []
    surf_rad = []
    for b in blocks:
        surf_top.append(b.face_top)
        surf_bt.append(b.face_bottom)
        surf_rad.append(b.face_right)

    return Ring(blocks, surf_top, surf_bt, surf_rad)


def create_cylinder_on_top():
    pass

def create_ring_on_top():
    pass

def create_cylinder_below():
    pass

def create_ring_below():
    pass

def create_ring_in_between():
    pass