"""Cylinders with an octagonal core. Does not provide the same functionality as cylinders.py."""
from dataclasses import dataclass
from .blocks import *


@dataclass
class Cylinder:
    inner_blocks: list
    outer_blocks: list
    surf_top: list
    surf_bt: list
    surf_rad: list


@dataclass
class Ring:
    blocks: list
    surf_top: list
    surf_bt: list
    surf_rad: list


def cartesian(r, phi, z, degree=True):
    if degree:
        phi = 2 * np.pi * phi / 360
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return [x, y, z]


def create_cylinder(
    mesh,
    r_top,
    r_bt,
    z_top,
    z_bt,
    z_top_mid,
    z_bt_mid,
    res_r,
    res_phi,
    res_z,
    s_in_top=[],
    s_in_bt=[],
    s_out_top=[],
    s_out_bt=[],
):
    # Central blocks
    radius_center_top = r_top / 2
    radius_center_bt = r_bt / 2

    res_center_r = int(res_phi / 8)
    b_0 = Block(
        mesh,
        cartesian(radius_center_bt, 0, z_bt_mid),
        cartesian(radius_center_bt, 45, z_bt_mid),
        cartesian(radius_center_bt, 90, z_bt_mid),
        cartesian(0, 0, z_bt_mid),
        cartesian(radius_center_top, 0, z_top_mid),
        cartesian(radius_center_top, 45, z_top_mid),
        cartesian(radius_center_top, 90, z_top_mid),
        cartesian(0, 0, z_top_mid),
    )
    b_0.set_number_of_cells(res_center_r, res_center_r, res_z)
    b_0.create()

    b_90 = Block(mesh)
    b_90.set_connection(b_0, "front")
    b_90.p2 = cartesian(radius_center_bt, 135, z_bt_mid)
    b_90.p3 = cartesian(radius_center_bt, 180, z_bt_mid)
    b_90.p6 = cartesian(radius_center_top, 135, z_top_mid)
    b_90.p7 = cartesian(radius_center_top, 180, z_top_mid)
    b_90.cells_x1 = res_center_r
    b_90.create()

    b_180 = Block(mesh)
    b_180.set_connection(b_90, "right")
    b_180.p0 = cartesian(radius_center_bt, 270, z_bt_mid)
    b_180.p3 = cartesian(radius_center_bt, 225, z_bt_mid)
    b_180.p4 = cartesian(radius_center_top, 270, z_top_mid)
    b_180.p7 = cartesian(radius_center_top, 225, z_top_mid)
    b_180.cells_x0 = res_center_r
    b_180.create()

    b_270 = Block(mesh)
    b_270.set_connection(b_180, "back")
    b_270.set_connection(b_0, "right")
    b_270.p0 = cartesian(radius_center_bt, 315, z_bt_mid)
    b_270.p4 = cartesian(radius_center_top, 315, z_top_mid)
    b_270.create()

    # if s_in_top != []:
    #     b_0.e7.type = "spline"
    #     b_90.e3.type = "spline"
    #     b_180.e6.type = "spline"
    #     b_270.e2.type = "spline"
    #     for p in s_in_top:
    #         b_0.e7.points.append(cartesian(p[0], 0, p[1]))
    #         b_90.e3.points.append(cartesian(p[0], 90, p[1]))
    #         b_180.e6.points.append(cartesian(p[0], 180, p[1]))
    #         b_270.e2.points.append(cartesian(p[0], 180, p[1]))

    # if s_in_bt != []:
    #     b_0.e4.type = "spline"
    #     b_90.e0.type = "spline"
    #     b_180.e5.type = "spline"
    #     b_270.e1.type = "spline"
    #     for i in range(len(s_in_bt)):
    #         coords = cartesian(s_in_bt[-i][0], 0, s_in_bt[-i][1])
    #         b_0.e4.points.append(cartesian(s_in_bt[-(i+1)][0], 0, s_in_bt[-(i+1)][1]))
    #         b_90.e0.points.append(cartesian(s_in_bt[i][0], 90, s_in_bt[i][1]))
    #         b_180.e5.points.append(cartesian(s_in_bt[i][0], 180, s_in_bt[i][1]))
    #         b_270.e1.points.append(cartesian(s_in_bt[-(i+1)][0], 270, s_in_bt[-(i+1)][1]))

    # #############
    # # TRY SPLINE INTERPOTALTION
    # x0 = np.array(cartesian(radius_center_bt, 0, z_bt_mid))
    # x1 = np.array(cartesian(radius_center_bt, 45, z_bt_mid))

    # radii = []
    # phis = []
    # res = 100
    # for dist in np.linspace(0, 1, res, endpoint=False):
    #     pos = x0 + dist*(x1-x0)
    #     radii.append((pos[0]**2 + pos[1]**2)**0.5)
    #     phis.append(np.arctan(pos[1]/pos[0])*360/(2*np.pi))
    # s_in_bt = [[0, 0]] + s_in_bt + [[radius_center_bt, z_bt_mid]]
    # s_in_bt = np.array(s_in_bt)
    # spline = interp1d(s_in_bt[:, 0], s_in_bt[:, 1], kind='cubic')
    # z_vals = spline(radii)

    # b_0.e0.type = "spline"
    # b_0.e5.type = "spline"
    # for i in range(res-1):
    #     b_0.e0.points.append(cartesian(radii[i+1], phis[i+1], z_vals[i+1]))
    #     b_0.e5.points.append(cartesian(radii[i+1], phis[i+1] + 45, z_vals[i+1]))

    # create ring around these blocks
    ring = create_ring(
        mesh,
        r_top,
        r_bt,
        z_top,
        z_bt,
        [
            b_0.face_front,
            b_0.face_right,
            b_90.face_right,
            b_90.face_back,
            b_180.face_back,
            b_180.face_left,
            b_270.face_left,
            b_270.face_front,
        ],
        res_r - res_center_r,
        res_phi,
        res_z,
    )

    surf_top = [
        b_0.face_top,
        b_90.face_top,
        b_180.face_top,
        b_270.face_top,
    ] + ring.surf_top
    surf_bt = [b_0.face_bottom, b_90.face_bottom, b_180.face_bottom, b_270.face_bottom]

    return Cylinder(
        [b_0, b_90, b_180, b_270], ring.blocks, surf_top, surf_bt, ring.surf_rad
    )


def create_ring(mesh, r_top, r_bt, z_top, z_bt, faces_inside, res_r, res_phi, res_z):

    blocks = []

    b = Block(mesh)
    b.face_left = faces_inside[0]
    b.p1 = cartesian(r_bt, 0, z_bt)
    b.p2 = cartesian(r_bt, 45, z_bt)
    b.p5 = cartesian(r_top, 0, z_top)
    b.p6 = cartesian(r_top, 45, z_top)
    b.set_number_of_cells(res_r, int(res_phi / 8), res_z)
    b.create()
    b.e5.type = "arc"
    b.e5.points = [cartesian(r_bt, 45 / 2, z_bt)]
    b.e6.type = "arc"
    b.e6.points = [cartesian(r_top, 45 / 2, z_top)]
    blocks.append(b)

    for i in range(6):
        i += 1
        b = Block(mesh)
        b.face_left = faces_inside[i]

        b.face_front = blocks[i - 1].face_back
        b.p2 = cartesian(r_bt, 45 * (i + 1), z_bt)
        b.p6 = cartesian(r_top, 45 * (i + 1), z_top)
        b.set_number_of_cells(res_r, int(res_phi / 8), res_z)
        b.create()
        b.e5.type = "arc"
        b.e5.points = [cartesian(r_bt, i * 45 + 45 / 2, z_bt)]
        b.e6.type = "arc"
        b.e6.points = [cartesian(r_top, i * 45 + 45 / 2, z_top)]
        blocks.append(b)

    b = Block(mesh)
    b.face_left = faces_inside[-1]
    b.face_front = blocks[-1].face_back
    b.face_back = blocks[0].face_front
    b.set_number_of_cells(res_r, int(res_phi / 8), res_z)
    b.create()
    b.e5.type = "arc"
    b.e5.points = [cartesian(r_bt, 360 - 45 / 2, z_bt)]
    b.e6.type = "arc"
    b.e6.points = [cartesian(r_top, 360 - 45 / 2, z_top)]

    surf_top = []
    surf_bt = []
    surf_rad = []
    for b in blocks:
        surf_top.append(b.face_top)
        surf_bt.append(b.face_bottom)
        surf_rad.append(b.face_right)

    return Ring(blocks, surf_top, surf_bt, surf_rad)
