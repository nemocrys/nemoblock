import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from scipy.interpolate import interp1d

from .blocks import *


@dataclass
class Ring:
    """Ring object to build meshes."""

    blocks: list
    surf_top: list
    surf_bt: list
    surf_rad: list
    grading_r: str = "1"
    grading_z: str = "1"

    def update_grading(self):
        for b in self.blocks:
            b.grading = f"simpleGrading ({self.grading_r} 1 {self.grading_z})"

    def set_grading_radial(self, val):
        self.grading_r = val
        self.update_grading()

    def set_grading_axial(self, val):
        self.grading_z = val
        self.update_grading()


@dataclass
class Cylinder:
    """Cylinder object to build meshes."""

    core: Block
    ring: Ring
    surf_top: list
    surf_bt: list
    surf_rad: list
    grading_r: str = "1"
    grading_z: str = "1"

    def update_grading(self):
        self.core.grading = f"simpleGrading (1 1 {self.grading_z})"
        self.ring.set_grading_radial(self.grading_r)
        self.ring.set_grading_axial(self.grading_z)

    def set_grading_radial(self, val):
        self.grading_r = val
        self.update_grading()

    def set_grading_axial(self, val):
        self.grading_z = val
        self.update_grading()


def cartesian(r, phi, z, degree=True):
    """Convert cylindrical to cartesian coordinates.

    Args:
        r (float): Radius.
        phi (float): Angle in degree.
        z (float): Axial coordinate.
        degree (bool): If false: use radiant.

    Returns:
        cartesian coordinates (x, y, z)
    """
    if degree:
        phi = 2 * np.pi * phi / 360
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return [x, y, z]


def spline(points, kind="cubic"):
    """Create a spline functions

    Args:
        points (list): list of [r, z] coordinates
        kind (str, optional): spline type (linear / cubic)
    """
    points = np.array(points)
    return interp1d(points[:, 0], points[:, 1], kind=kind)


def plot_spline(sp, r, fig=None, ax=None):
    """plot spline function

    Args:
        sp (function): spline function
        r (list): [min, max radius]
        fig (figure, optional): Matplotlib figure.
        ax (axis, optional): Matplotlib axis.

    Returns:
        matplotlib figure, axis
    """
    if fig is None:
        fig, ax = plt.subplots(1, 1)
    r = np.linspace(r[0], r[1], 100)
    ax.plot(r, sp(r))
    return fig, ax


def create_cylinder(
    mesh,
    r_top,
    r_bt,
    z_top,
    z_bt,
    res_r,
    res_phi,
    res_z,
    radius_ratio=0.5,
    spline_res=100,
    cylinder_below=None,
    cylinder_on_top=None,
):
    """Create a cylinder object consisting of a square and a ring.

    Args:
        mesh (Mesh): Mesh containing the blocks.
        r_top (float): Radius at the top.
        r_bt (float): Radius at the bottom.
        z_top (float or function): Axial coordinate at top or z=f(r).
        z_bt (float or function): Axial coordinate at bootom or z=f(r).
        res_r (float): Number of cells in radial direction (in Ring).
        res_phi (float): Number of cells in circumferential direction.
        res_z (float): Number of cells in axial direction.
        radius_ratio (float, optional): Fraction inner square / total radius.
        spline_res (int, optional): Resolution for spline interplation.
        cylinder_below (Cylinder, optional): Cylinder object below this cylinder.
        cylinder_on_top (Cylinder, optional): Cylinder object on top of this cylinder.

    Returns:
        Cylinder object.
    """
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
        b.set_connection(cylinder_below.core, "bottom")
        b.p4 = cartesian(radius_center_top, 0, z_top_mid)
        b.p5 = cartesian(radius_center_top, 90, z_top_mid)
        b.p6 = cartesian(radius_center_top, 180, z_top_mid)
        b.p7 = cartesian(radius_center_top, 270, z_top_mid)
    elif cylinder_on_top is not None:
        b = Block(mesh)
        b.set_connection(cylinder_on_top.core, "top")
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
            cartesian(radius_center_top, 270, z_top_mid),
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
            pos = x0 + dist * (x1 - x0)
            radii.append((pos[0] ** 2 + pos[1] ** 2) ** 0.5)
            phis.append(np.arctan(pos[1] / pos[0]) * 360 / (2 * np.pi))
        z_vals = z_bt(radii)

        b.e0.type = "spline"
        b.e5.type = "spline"
        b.e1.type = "spline"
        b.e4.type = "spline"
        for i in range(len(radii) - 1):
            b.e0.points.append(cartesian(radii[i + 1], phis[i + 1], z_vals[i + 1]))
            b.e5.points.append(cartesian(radii[i + 1], phis[i + 1] + 90, z_vals[i + 1]))
            b.e1.points.append(
                cartesian(radii[i + 1], 270 - phis[i + 1], z_vals[i + 1])
            )
            b.e4.points.append(
                cartesian(radii[i + 1], 360 - phis[i + 1], z_vals[i + 1])
            )

    if type(z_top) is interp1d:
        x0 = np.array(cartesian(radius_center_top, 0, z_top_mid))
        x1 = np.array(cartesian(radius_center_top, 90, z_top_mid))
        radii = []
        phis = []
        for dist in np.linspace(0, 1, spline_res, endpoint=False):
            pos = x0 + dist * (x1 - x0)
            radii.append((pos[0] ** 2 + pos[1] ** 2) ** 0.5)
            phis.append(np.arctan(pos[1] / pos[0]) * 360 / (2 * np.pi))
        z_vals = z_top(radii)

        b.e3.type = "spline"
        b.e6.type = "spline"
        b.e2.type = "spline"
        b.e7.type = "spline"

        for i in range(len(radii) - 1):
            b.e3.points.append(cartesian(radii[i + 1], phis[i + 1], z_vals[i + 1]))
            b.e6.points.append(cartesian(radii[i + 1], phis[i + 1] + 90, z_vals[i + 1]))
            b.e2.points.append(
                cartesian(radii[i + 1], 270 - phis[i + 1], z_vals[i + 1])
            )
            b.e7.points.append(
                cartesian(radii[i + 1], 360 - phis[i + 1], z_vals[i + 1])
            )

    # create ring around these blocks
    ring_below = None
    ring_on_top = None
    if cylinder_below is not None:
        ring_below = cylinder_below.ring
    if cylinder_on_top is not None:
        ring_on_top = cylinder_on_top.ring
    ring = create_ring(
        mesh,
        r_top,
        radius_center_top,
        r_bt,
        radius_center_bt,
        z_top,
        z_bt,
        [b.face_front, b.face_right, b.face_back, b.face_left],
        res_r,
        res_phi,
        res_z,
        spline_res,
        ring_below=ring_below,
        ring_on_top=ring_on_top,
    )
    surf_top = [b.face_top] + ring.surf_top
    surf_bt = [b.face_bottom] + ring.surf_bt

    return Cylinder(b, ring, surf_top, surf_bt, ring.surf_rad)


def create_ring(
    mesh,
    r_top,
    r_in_top,
    r_bt,
    r_in_bt,
    z_top,
    z_bt,
    faces_inside,
    res_r,
    res_phi,
    res_z,
    spline_res=100,
    spline_outside=None,
    ring_below=None,
    ring_on_top=None,
    faces_outside=[],
):
    """Create a ring of 4 blocks.

    Args:
        mesh (Mesh): Mesh object containing the blocks.
        r_top (float): Outer radius at top.
        r_in_top (float): Inner radius at top.
        r_bt (float): Outer radius at bottom.
        r_in_bt (float): Inner radius at bottom.
        z_top (float or function): Axial coordinate at top or z=f(r).
        z_bt (float or function): Axial coordinate at bottom or z=f(r).
        faces_inside (list): Faces of blocks inside of the ring.
        res_r (float): Number of cells in radial direction.
        res_phi (float): Number of cells in circumferential direction.
        res_z (float): Number of cells in axial direction.
        spline_res (int, optional): Resolution for spline interpolation.
        spline_outside (function, optional): Outer surface z=f(r).
        ring_below (Ring, optional): Ring object bellow this ring.
        ring_on_top (Ring, optional): Ring object on top of this ring.
        faces_outside (list, optional): Surfaces of blocks outside of this ring.

    Returns:
        Ring object.
    """

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
        b.set_number_of_cell(res_r, int(res_phi / 4), res_z)
        b.create()
    elif ring_below is not None:
        b.set_connection(ring_below.blocks[0], "bottom")
        b.p5 = cartesian(r_top, 0, z_top_out)
        b.p6 = cartesian(r_top, 90, z_top_out)
        b.set_number_of_cell(res_r, int(res_phi / 4), res_z)
        b.create()
        b.e6.type = "arc"
        b.e6.points = [cartesian(r_top, 45, z_top_out)]
    elif ring_on_top is not None:
        b.set_connection(ring_on_top.blocks[0], "top")
        b.p1 = cartesian(r_bt, 0, z_bt_out)
        b.p2 = cartesian(r_bt, 90, z_bt_out)
        b.set_number_of_cell(res_r, int(res_phi / 4), res_z)
        b.create()
        b.e5.type = "arc"
        b.e5.points = [cartesian(r_bt, 45, z_bt_out)]
    else:
        b.p1 = cartesian(r_bt, 0, z_bt_out)
        b.p2 = cartesian(r_bt, 90, z_bt_out)
        b.p5 = cartesian(r_top, 0, z_top_out)
        b.p6 = cartesian(r_top, 90, z_top_out)
        b.set_number_of_cell(res_r, int(res_phi / 4), res_z)
        b.create()
        b.e5.type = "arc"
        b.e5.points = [cartesian(r_bt, 45, z_bt_out)]
        b.e6.type = "arc"
        b.e6.points = [cartesian(r_top, 45, z_top_out)]
    blocks.append(b)

    for i in range(2):
        i += 1
        b = Block(mesh)
        b.face_left = faces_inside[i]
        b.face_front = blocks[i - 1].face_back
        if faces_outside != []:
            b.face_right = faces_outside[i]
            b.set_number_of_cell(res_r, int(res_phi / 4), res_z)
            b.create()
        elif ring_below is not None:
            b.set_connection(ring_below.blocks[i], "bottom")
            b.p6 = cartesian(r_top, 90 * (i + 1), z_top_out)
            b.set_number_of_cell(res_r, int(res_phi / 4), res_z)
            b.create()
            b.e6.type = "arc"
            b.e6.points = [cartesian(r_top, i * 90 + 45, z_top_out)]
        elif ring_on_top is not None:
            b.set_connection(ring_on_top.blocks[i], "top")
            b.p2 = cartesian(r_bt, 90 * (i + 1), z_bt_out)
            b.set_number_of_cell(res_r, int(res_phi / 4), res_z)
            b.create()
            b.e5.type = "arc"
            b.e5.points = [cartesian(r_bt, i * 90 + 45, z_bt_out)]
        else:
            b.p2 = cartesian(r_bt, 90 * (i + 1), z_bt_out)
            b.p6 = cartesian(r_top, 90 * (i + 1), z_top_out)
            b.set_number_of_cell(res_r, int(res_phi / 4), res_z)
            b.create()
            b.e5.type = "arc"
            b.e5.points = [cartesian(r_bt, i * 90 + 45, z_bt_out)]
            b.e6.type = "arc"
            b.e6.points = [cartesian(r_top, i * 90 + 45, z_top_out)]
        blocks.append(b)

    b = Block(mesh)
    b.face_left = faces_inside[-1]
    b.face_front = blocks[-1].face_back
    b.face_back = blocks[0].face_front
    b.set_number_of_cell(res_r, int(res_phi / 4), res_z)
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
