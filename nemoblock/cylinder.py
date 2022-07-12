import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
import scipy.interpolate as interpolate

from .blocks import *


@dataclass
class Ring:
    """Ring object to build meshes."""

    blocks: list
    surf_top: list
    surf_bt: list
    surf_rad: list
    _grading_r: str = "1"
    _grading_z: str = "1"

    def _update_grading(self):
        for b in self.blocks:
            b.grading = f"simpleGrading ({self._grading_r} 1 {self._grading_z})"

    def set_grading_radial(self, val):
        self._grading_r = val
        self._update_grading()

    def set_grading_axial(self, val):
        self._grading_z = val
        self._update_grading()

    def set_spline_surface(self, spline, pos, res=100):
        # set surface with spline z=f(r)

        # TODO update inside and outside points
        # if type(z_bt) is interp1d:
        #     z_bt_out = z_bt(r_bt)
        # if type(z_top) is interp1d:
        #     z_top_out = z_top(r_top)

        if pos == "bottom":
            r_in = (self.blocks[0]._p0.x1 ** 2 + self.blocks[0]._p0.x2 ** 2) ** 0.5
            r_out = (self.blocks[0]._p1.x1 ** 2 + self.blocks[0]._p1.x2 ** 2) ** 0.5
            self.blocks[0].p0.update_coordinates(cartesian(r_in, 0, spline(r_in)))
            self.blocks[1].p0.update_coordinates(cartesian(r_in, 90, spline(r_in)))
            self.blocks[2].p0.update_coordinates(cartesian(r_in, 180, spline(r_in)))
            self.blocks[3].p0.update_coordinates(cartesian(r_in, 270, spline(r_in)))
            self.blocks[0].p1.update_coordinates(cartesian(r_out, 0, spline(r_out)))
            self.blocks[1].p1.update_coordinates(cartesian(r_out, 90, spline(r_out)))
            self.blocks[2].p1.update_coordinates(cartesian(r_out, 180, spline(r_out)))
            self.blocks[3].p1.update_coordinates(cartesian(r_out, 270, spline(r_out)))
            for b in self.blocks:
                b.e0.type = "spline"
            for r in np.linspace(r_in, r_out, res, endpoint=False):
                self.blocks[0].e0.points.append(cartesian(r, 0, spline(r)))
                self.blocks[1].e0.points.append(cartesian(r, 90, spline(r)))
                self.blocks[2].e0.points.append(cartesian(r, 180, spline(r)))
                self.blocks[3].e0.points.append(cartesian(r, 270, spline(r)))
        elif pos == "top":
            r_in = (self.blocks[0]._p4.x1 ** 2 + self.blocks[0]._p4.x2 ** 2) ** 0.5
            r_out = (self.blocks[0]._p5.x1 ** 2 + self.blocks[0]._p5.x2 ** 2) ** 0.5
            self.blocks[0].p4.update_coordinates(cartesian(r_in, 0, spline(r_in)))
            self.blocks[1].p4.update_coordinates(cartesian(r_in, 90, spline(r_in)))
            self.blocks[2].p4.update_coordinates(cartesian(r_in, 180, spline(r_in)))
            self.blocks[3].p4.update_coordinates(cartesian(r_in, 270, spline(r_in)))
            self.blocks[0].p5.update_coordinates(cartesian(r_out, 0, spline(r_out)))
            self.blocks[1].p5.update_coordinates(cartesian(r_out, 90, spline(r_out)))
            self.blocks[2].p5.update_coordinates(cartesian(r_out, 180, spline(r_out)))
            self.blocks[3].p5.update_coordinates(cartesian(r_out, 270, spline(r_out)))
            for b in self.blocks:
                b.e3.type = "spline"
            for r in np.linspace(r_in, r_out, res, endpoint=False):
                self.blocks[0].e3.points.append(cartesian(r, 0, spline(r)))
                self.blocks[1].e3.points.append(cartesian(r, 90, spline(r)))
                self.blocks[2].e3.points.append(cartesian(r, 180, spline(r)))
                self.blocks[3].e3.points.append(cartesian(r, 270, spline(r)))
        elif pos == "side":
            r_bt = (self.blocks[0]._p1.x1 ** 2 + self.blocks[0]._p1.x2 ** 2) ** 0.5
            r_top = (self.blocks[0]._p5.x1 ** 2 + self.blocks[0]._p5.x2 ** 2) ** 0.5
            self.blocks[0].p1.update_coordinates(cartesian(r_bt, 0, spline(r_bt)))
            self.blocks[1].p1.update_coordinates(cartesian(r_bt, 90, spline(r_bt)))
            self.blocks[2].p1.update_coordinates(cartesian(r_bt, 180, spline(r_bt)))
            self.blocks[3].p1.update_coordinates(cartesian(r_bt, 270, spline(r_bt)))
            self.blocks[0].p5.update_coordinates(cartesian(r_top, 0, spline(r_top)))
            self.blocks[1].p5.update_coordinates(cartesian(r_top, 90, spline(r_top)))
            self.blocks[2].p5.update_coordinates(cartesian(r_top, 180, spline(r_top)))
            self.blocks[3].p5.update_coordinates(cartesian(r_top, 270, spline(r_top)))
            for b in self.blocks:
                b.e9.type = "spline"
            for r in np.linspace(r_bt, r_top, res):
                self.blocks[0].e9.points.append(cartesian(r, 0, spline(r)))
                self.blocks[1].e9.points.append(cartesian(r, 90, spline(r)))
                self.blocks[2].e9.points.append(cartesian(r, 180, spline(r)))
                self.blocks[3].e9.points.append(cartesian(r, 270, spline(r)))
        else:
            raise ValueError(
                "This position does not exists. Allowable parameters for pos are 'bottom', 'top', 'side'."
            )


@dataclass
class Cylinder:
    """Cylinder object to build meshes."""

    core: Block
    ring: Ring
    surf_top: list
    surf_bt: list
    surf_rad: list
    _grading_r: str = "1"
    _grading_z: str = "1"

    def _update_grading(self):
        self.core.grading = f"simpleGrading (1 1 {self._grading_z})"
        self.ring.set_grading_radial(self._grading_r)
        self.ring.set_grading_axial(self._grading_z)

    def set_grading_radial(self, val):
        self._grading_r = val
        self._update_grading()

    def set_grading_axial(self, val):
        self._grading_z = val
        self._update_grading()

    def set_spline_surface(self, spline, pos, res=100):
        # set surface with spline z=f(r)

        if pos == "bottom":
            # update core
            radius_center_bt = (self.core._p1.x1 ** 2 + self.core._p1.x2 ** 2) ** 0.5
            z_bt_mid = spline(radius_center_bt)
            # update points
            self.core.p0.update_coordinates(cartesian(radius_center_bt, 0, z_bt_mid))
            self.core.p1.update_coordinates(cartesian(radius_center_bt, 90, z_bt_mid))
            self.core.p2.update_coordinates(cartesian(radius_center_bt, 180, z_bt_mid))
            self.core.p3.update_coordinates(cartesian(radius_center_bt, 270, z_bt_mid))
            # set values on edges
            x0 = np.array(cartesian(radius_center_bt, 0, z_bt_mid))
            x1 = np.array(cartesian(radius_center_bt, 90, z_bt_mid))
            radii = []
            phis = []
            for dist in np.linspace(0, 1, res, endpoint=False):
                pos = x0 + dist * (x1 - x0)
                radii.append((pos[0] ** 2 + pos[1] ** 2) ** 0.5)
                phis.append(np.arctan(pos[1] / pos[0]) * 360 / (2 * np.pi))
            z_vals = spline(radii)
            self.core.e0.type = "spline"
            self.core.e5.type = "spline"
            self.core.e1.type = "spline"
            self.core.e4.type = "spline"
            for i in range(len(radii) - 1):
                self.core.e0.points.append(
                    cartesian(radii[i + 1], phis[i + 1], z_vals[i + 1])
                )
                self.core.e5.points.append(
                    cartesian(radii[i + 1], phis[i + 1] + 90, z_vals[i + 1])
                )
                self.core.e1.points.append(
                    cartesian(radii[i + 1], 270 - phis[i + 1], z_vals[i + 1])
                )
                self.core.e4.points.append(
                    cartesian(radii[i + 1], 360 - phis[i + 1], z_vals[i + 1])
                )
            self.ring.set_spline_surface(spline, "bottom", res)

        elif pos == "top":
            # update core
            radius_center_top = (self.core._p5.x1 ** 2 + self.core._p5.x2 ** 2) ** 0.5
            z_top_mid = spline(radius_center_top)
            # update points
            self.core.p4.update_coordinates(cartesian(radius_center_top, 0, z_top_mid))
            self.core.p5.update_coordinates(cartesian(radius_center_top, 90, z_top_mid))
            self.core.p6.update_coordinates(
                cartesian(radius_center_top, 180, z_top_mid)
            )
            self.core.p7.update_coordinates(
                cartesian(radius_center_top, 270, z_top_mid)
            )
            # set values on edges
            x0 = np.array(cartesian(radius_center_top, 0, z_top_mid))
            x1 = np.array(cartesian(radius_center_top, 90, z_top_mid))
            radii = []
            phis = []
            for dist in np.linspace(0, 1, res, endpoint=False):
                pos = x0 + dist * (x1 - x0)
                radii.append((pos[0] ** 2 + pos[1] ** 2) ** 0.5)
                phis.append(np.arctan(pos[1] / pos[0]) * 360 / (2 * np.pi))
            z_vals = spline(radii)

            self.core.e3.type = "spline"
            self.core.e6.type = "spline"
            self.core.e2.type = "spline"
            self.core.e7.type = "spline"

            for i in range(len(radii) - 1):
                self.core.e3.points.append(
                    cartesian(radii[i + 1], phis[i + 1], z_vals[i + 1])
                )
                self.core.e6.points.append(
                    cartesian(radii[i + 1], phis[i + 1] + 90, z_vals[i + 1])
                )
                self.core.e2.points.append(
                    cartesian(radii[i + 1], 270 - phis[i + 1], z_vals[i + 1])
                )
                self.core.e7.points.append(
                    cartesian(radii[i + 1], 360 - phis[i + 1], z_vals[i + 1])
                )
            self.ring.set_spline_surface(spline, "top", res)

        elif pos == "side":
            raise NotImplementedError()
        else:
            raise ValueError(
                "This position does not exists. Allowable parameters for pos are 'bottom', 'top', 'side'."
            )


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
    return interpolate.interp1d(points[:, 0], points[:, 1], kind=kind)


# inspired by https://github.com/kawache/Python-B-spline-examples
def b_spline(control_points, plot=False, res=100):
    """Create a spline curve that does not go through the control points.

    Args:
        control_points (list): list of points [[x0, y0], [x1, y1], ...]
        plot (bool): Plot the spline and the control points
        res (int): Resolution. Defaults to 100.

    Returns:
        array: [x coordinates, y coordinates]
    """
    control_points = np.array(control_points)
    t = np.concatenate(
        [[0, 0, 0], np.linspace(0, 1, control_points.shape[0] - 2), [1, 1, 1]]
    )  # knots

    spline = interpolate.splev(np.linspace(0, 1, res), [t, control_points.T, 3])

    if plot:
        fig, ax = plt.subplots(1, 1)
        ax.plot(spline[0], spline[1], label="b-spline curve")
        ax.plot(
            control_points[:, 0], control_points[:, 1], "x--", label="control points"
        )
        ax.legend()
        ax.grid(linestyle=":")
        plt.show()
    return np.array(spline)


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
    p_top,
    p_bt,
    res_r,
    res_phi,
    res_z,
    radius_ratio=0.5,
    cylinder_below=None,
    cylinder_on_top=None,
):
    """Create a cylinder object consisting of a square core surrounded by a ring.

    Args:
        mesh (Mesh): Mesh containing the blocks.
        p_top (list): [r, z] coordinate at top
        p_bt (list): [r, z] coordinate at bottom
        res_r (float): Number of cells in radial direction (in Ring).
        res_phi (float): Number of cells in circumferential direction.
        res_z (float): Number of cells in axial direction.
        radius_ratio (float, optional): Fraction inner square / total radius.
        cylinder_below (Cylinder, optional): Cylinder object below this cylinder.
        cylinder_on_top (Cylinder, optional): Cylinder object on top of this cylinder.

    Returns:
        Cylinder object.
    """
    if cylinder_below is not None and cylinder_on_top is not None:
        raise ValueError("Both cylinder on top and below is not supported.")

    # Central block
    radius_center_top = p_top[0] * radius_ratio
    radius_center_bt = p_bt[0] * radius_ratio
    res_center_r = int(round(res_phi / 4))

    if cylinder_below is not None:
        b = Block(mesh)
        b.set_connection(cylinder_below.core, "bottom")
        b.p4 = cartesian(radius_center_top, 0, p_top[1])
        b.p5 = cartesian(radius_center_top, 90, p_top[1])
        b.p6 = cartesian(radius_center_top, 180, p_top[1])
        b.p7 = cartesian(radius_center_top, 270, p_top[1])
    elif cylinder_on_top is not None:
        b = Block(mesh)
        b.set_connection(cylinder_on_top.core, "top")
        b.p0 = cartesian(radius_center_bt, 0, p_bt[1])
        b.p1 = cartesian(radius_center_bt, 90, p_bt[1])
        b.p2 = cartesian(radius_center_bt, 180, p_bt[1])
        b.p3 = cartesian(radius_center_bt, 270, p_bt[1])
    else:
        b = Block(
            mesh,
            cartesian(radius_center_bt, 0, p_bt[1]),
            cartesian(radius_center_bt, 90, p_bt[1]),
            cartesian(radius_center_bt, 180, p_bt[1]),
            cartesian(radius_center_bt, 270, p_bt[1]),
            cartesian(radius_center_top, 0, p_top[1]),
            cartesian(radius_center_top, 90, p_top[1]),
            cartesian(radius_center_top, 180, p_top[1]),
            cartesian(radius_center_top, 270, p_top[1]),
        )
    b.set_number_of_cells(res_center_r, res_center_r, res_z)
    b.create()

    # create ring around these blocks
    ring_below = None
    ring_on_top = None
    if cylinder_below is not None:
        ring_below = cylinder_below.ring
    if cylinder_on_top is not None:
        ring_on_top = cylinder_on_top.ring
    ring = create_ring(
        mesh,
        p_top,
        p_bt,
        [b.face_front, b.face_right, b.face_back, b.face_left],
        res_r,
        res_phi,
        res_z,
        ring_below=ring_below,
        ring_on_top=ring_on_top,
    )
    surf_top = [b.face_top] + ring.surf_top
    surf_bt = [b.face_bottom] + ring.surf_bt

    return Cylinder(b, ring, surf_top, surf_bt, ring.surf_rad)


def create_ring(
    mesh,
    p_top,
    p_bt,
    faces_inside,
    res_r,
    res_phi,
    res_z,
    ring_below=None,
    ring_on_top=None,
    faces_outside=[],
):
    """Create a ring of 4 blocks.

    Args:
        mesh (Mesh): Mesh object containing the blocks.
        p_top (list): [r, z] coordinate at top
        p_bt (list): [r, z] coordinate at bottom
        faces_inside (list): Faces of blocks inside of the ring.
        res_r (float): Number of cells in radial direction.
        res_phi (float): Number of cells in circumferential direction.
        res_z (float): Number of cells in axial direction.
        ring_below (Ring, optional): Ring object bellow this ring.
        ring_on_top (Ring, optional): Ring object on top of this ring.
        faces_outside (list, optional): Surfaces of blocks outside of this ring.

    Returns:
        Ring object.
    """

    if ring_below is not None and ring_on_top is not None:
        raise ValueError("It's not allowed to provide both ring_on_top and ring_below.")

    blocks = []

    b = Block(mesh)
    b.face_left = faces_inside[0]
    if faces_outside != []:
        b.face_right = faces_outside[0]
        b.set_number_of_cells(res_r, int(round(res_phi / 4)), res_z)
        b.create()
    elif ring_below is not None:
        b.set_connection(ring_below.blocks[0], "bottom")
        b.p5 = cartesian(p_top[0], 0, p_top[1])
        b.p6 = cartesian(p_top[0], 90, p_top[1])
        b.set_number_of_cells(res_r, int(round(res_phi / 4)), res_z)
        b.create()
        b.e6.type = "arc"
        b.e6.points = [cartesian(p_top[0], 45, p_top[1])]
    elif ring_on_top is not None:
        b.set_connection(ring_on_top.blocks[0], "top")
        b.p1 = cartesian(p_bt[0], 0, p_bt[1])
        b.p2 = cartesian(p_bt[0], 90, p_bt[1])
        b.set_number_of_cells(res_r, int(round(res_phi / 4)), res_z)
        b.create()
        b.e5.type = "arc"
        b.e5.points = [cartesian(p_bt[0], 45, p_bt[1])]
    else:
        b.p1 = cartesian(p_bt[0], 0, p_bt[1])
        b.p2 = cartesian(p_bt[0], 90, p_bt[1])
        b.p5 = cartesian(p_top[0], 0, p_top[1])
        b.p6 = cartesian(p_top[0], 90, p_top[1])
        b.set_number_of_cells(res_r, int(round(res_phi / 4)), res_z)
        b.create()
        b.e5.type = "arc"
        b.e5.points = [cartesian(p_bt[0], 45, p_bt[1])]
        b.e6.type = "arc"
        b.e6.points = [cartesian(p_top[0], 45, p_top[1])]
    blocks.append(b)

    for i in range(2):
        i += 1
        b = Block(mesh)
        b.face_left = faces_inside[i]
        b.face_front = blocks[i - 1].face_back
        if faces_outside != []:
            b.face_right = faces_outside[i]
            b.set_number_of_cells(res_r, int(round(res_phi / 4)), res_z)
            b.create()
        elif ring_below is not None:
            b.set_connection(ring_below.blocks[i], "bottom")
            b.p6 = cartesian(p_top[0], 90 * (i + 1), p_top[1])
            b.set_number_of_cells(res_r, int(round(res_phi / 4)), res_z)
            b.create()
            b.e6.type = "arc"
            b.e6.points = [cartesian(p_top[0], i * 90 + 45, p_top[1])]
        elif ring_on_top is not None:
            b.set_connection(ring_on_top.blocks[i], "top")
            b.p2 = cartesian(p_bt[0], 90 * (i + 1), p_bt[1])
            b.set_number_of_cells(res_r, int(round(res_phi / 4)), res_z)
            b.create()
            b.e5.type = "arc"
            b.e5.points = [cartesian(p_bt[0], i * 90 + 45, p_bt[1])]
        else:
            b.p2 = cartesian(p_bt[0], 90 * (i + 1), p_bt[1])
            b.p6 = cartesian(p_top[0], 90 * (i + 1), p_top[1])
            b.set_number_of_cells(res_r, int(round(res_phi / 4)), res_z)
            b.create()
            b.e5.type = "arc"
            b.e5.points = [cartesian(p_bt[0], i * 90 + 45, p_bt[1])]
            b.e6.type = "arc"
            b.e6.points = [cartesian(p_top[0], i * 90 + 45, p_top[1])]
        blocks.append(b)

    b = Block(mesh)
    b.face_left = faces_inside[-1]
    b.face_front = blocks[-1].face_back
    b.face_back = blocks[0].face_front
    b.set_number_of_cells(res_r, int(round(res_phi / 4)), res_z)
    b.create()
    if faces_outside != []:
        pass
    elif ring_below is not None:
        b.e6.type = "arc"
        b.e6.points = [cartesian(p_top[0], 360 - 45, p_top[1])]
    elif ring_on_top is not None:
        b.e5.type = "arc"
        b.e5.points = [cartesian(p_bt[0], 360 - 45, p_bt[1])]
    else:
        b.e5.type = "arc"
        b.e5.points = [cartesian(p_bt[0], 360 - 45, p_bt[1])]
        b.e6.type = "arc"
        b.e6.points = [cartesian(p_top[0], 360 - 45, p_top[1])]
    blocks.append(b)

    surf_top = []
    surf_bt = []
    surf_rad = []
    for b in blocks:
        surf_top.append(b.face_top)
        surf_bt.append(b.face_bottom)
        surf_rad.append(b.face_right)

    return Ring(blocks, surf_top, surf_bt, surf_rad)
