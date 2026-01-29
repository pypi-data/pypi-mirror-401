from collections.abc import Sequence

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt


def eval_normal_q4(p1, p2, p3, p4, s, t):
    """Evaluate the normal vector of a 4 noded quad element at
    the parametric coordinates s, and t (in [0, 1]).
    The parametric coordinates for the four nodes are:

    p1: (0, 0)
    p2: (1, 0)
    p3: (1, 1)
    p4: (0, 1)

    :param p1:
        The first node.

    :param p2:
        The second node.

    :param p3:
        The third node.

    :param p4:
        The fourth node.

    :param s:
        The s parameters.

    :param t:
        The t parameters.

    :return:
        The normal vectors at this position.

    """

    # the number of evaluations
    num_eval = len(s)

    # make a return array
    n = np.zeros((num_eval, 3))
    e_s = np.zeros((num_eval, 3))
    e_t = np.zeros((num_eval, 3))

    # compute the two tangential vectors
    e_s[:, 0] = (1.0 - t) * p2[0] - (1.0 - t) * p1[0] + t * p3[0] - t * p4[0]
    e_s[:, 1] = (1.0 - t) * p2[1] - (1.0 - t) * p1[1] + t * p3[1] - t * p4[1]
    e_s[:, 2] = (1.0 - t) * p2[2] - (1.0 - t) * p1[2] + t * p3[2] - t * p4[2]

    e_t[:, 0] = -s * p2[0] - (1.0 - s) * p1[0] + s * p3[0] + (1.0 - s) * p4[0]
    e_t[:, 1] = -s * p2[1] - (1.0 - s) * p1[1] + s * p3[1] + (1.0 - s) * p4[1]
    e_t[:, 2] = -s * p2[2] - (1.0 - s) * p1[2] + s * p3[2] + (1.0 - s) * p4[2]

    # compute the normal vector
    n[:, 0] = e_s[:, 1] * e_t[:, 2] - e_s[:, 2] * e_t[:, 1]
    n[:, 1] = e_s[:, 2] * e_t[:, 0] - e_s[:, 0] * e_t[:, 2]
    n[:, 2] = e_s[:, 0] * e_t[:, 1] - e_s[:, 1] * e_t[:, 0]

    # compute its norm
    norm = np.linalg.norm(n, axis=1)

    # normalize it
    n[:, 0] /= norm
    n[:, 1] /= norm
    n[:, 2] /= norm

    return n


def compute_average_normal_vector(n_1, n_2):
    """Compute the average normal vector at a node, based on the
    two vectors (n_1 and n_2) corresponding to the two finite elements.

    :param n_1:
        The first normal vector.

    :param n_2:
        The second normal vector.

    :return:
        The average normal vector, and the scale factor.
    """
    n = 0.5 * (n_1 + n_2)
    n /= np.linalg.norm(n)
    proj = np.sum(n_1 * n_2)
    if abs(proj) < 1.0:
        alpha = 0.5 * abs(np.arccos(proj))
    elif proj >= 1.0:
        alpha = 0.0
    else:
        alpha = np.pi

    return n, 1.0 / np.cos(alpha)


def find_nr_straight(input_split: Sequence[npt.NDArray[np.float64]]) -> int:
    n_straight = input_split[0].shape[0]
    for arr in input_split:
        arr_xy = arr[:, :2]
        arr_xydiff = np.diff(arr_xy, axis=0)
        # Find first non-zero difference
        for i, diff in enumerate(arr_xydiff):
            if not np.isclose(np.linalg.norm(diff), 0.0):
                if i <= n_straight:
                    n_straight = i
                break
    return n_straight


def get_intersection_line_cylinder(r_0, m, R, debug=False) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.bool_]]:
    """Compute the intersection points between a series of lines and
    a centered cylinder with radius R (infinite length).

    :paramn r_0:
        A (M x 3) numpy array, where M is the number of lines for the line intersects.

    :param m:
        A (M x 3) numpy array, where M is the number of lines for the line slopes.

    :param R:
        The radius of the cylinder

    :param debug:
        Set this flag to true if You like to generate a plot.

    :return:
        A (M x 3) numpy array, where M is the number of lines, for the intersections.
        A (M, ) numpy array with the vadilities of the intersections. i.e. if the intersection
        was found.
    """

    # the number of lines
    M = r_0.shape[0]
    # the parameters of the intersection
    t = np.zeros((M,))

    # intersections
    r = np.zeros((M, 3))

    # valid intersections
    valid = t != 0

    # loop over the points
    for i in range(M):
        # the parameters of the polynomial to solve
        a = m[i, 0] ** 2 + m[i, 1] ** 2
        b = 2.0 * (m[i, 0] * r_0[i, 0] + m[i, 1] * r_0[i, 1])
        c = r_0[i, 0] ** 2 + r_0[i, 1] ** 2 - R**2

        if True:
            # to do: check the vadility
            valid[i] = True

            # compute the two possible parameters
            t1 = (b + np.sqrt(abs(b**2 - 4 * a * c))) / 2.0 / a
            t2 = (b - np.sqrt(abs(b**2 - 4 * a * c))) / 2.0 / a
            # store the positive one

            if t1 > 0:
                t[i] = -t2
            else:
                t[i] = t1

            r[i, :] = t[i] * m[i, :] + r_0[i, :]

    if debug:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot(r_0[:, 0], r_0[:, 1], r_0[:, 2], "o")
        ax.plot(r_0[:, 0] + m[:, 0], r_0[:, 1] + m[:, 1], r_0[:, 2] + m[:, 2], "o")

        for i in range(M):
            ax.plot([r_0[i, 0], r[i, 0]], [r_0[i, 1], r[i, 1]], [r_0[i, 2], r[i, 2]])
        ax.set_aspect("equal")
        plt.show()

    return r, valid


def normalize_vectors(r):
    """Normalize a series of vectors.

    :param r:
        The vectors in a (M x 3) array. We normalize along M.

    :return:
        The normalized vectors.

    """

    r_ret = r.copy()
    r_norm = np.linalg.norm(r_ret, axis=1)
    r_ret[:, 0] /= r_norm
    r_ret[:, 1] /= r_norm
    r_ret[:, 2] /= r_norm

    return r_ret


def add_insulation_thickness(
    p: npt.NDArray[np.float64], c: list[list[int]], delta_r: float, delta_phi: float
) -> npt.NDArray[np.float64]:
    """Given the positions of the four edges of a cable geometry, add
    the insulation thicknesses.

    :param p:
        The nodal coordinates of the 8 noded bricks.

    :param c:
        The connectivity of the 8 noded bricks.

    :param delta_r:
        The insulation thickness at the thin side of the cable.

    :param delta_phi:
        The insulation thickness at the thick side of the cable.

    :return:
        The updated nodal coordinates.
    """

    # the number of bricks
    num_bricks = len(c)
    p_ret = p.copy()

    # loop over the elements
    for i, e in enumerate(c):
        # normal vectors of face 3
        n_f3_1 = eval_normal_q4(
            p[e[0], :],
            p[e[1], :],
            p[e[5], :],
            p[e[4], :],
            np.array([0, 1, 1, 0]),
            np.array([0, 0, 1, 1]),
        )

        # normal vectors of face 4
        n_f4_1 = eval_normal_q4(
            p[e[2], :],
            p[e[3], :],
            p[e[7], :],
            p[e[6], :],
            np.array([0, 1, 1, 0]),
            np.array([0, 0, 1, 1]),
        )

        # normal vectors of face 5
        n_f5_1 = -1.0 * eval_normal_q4(
            p[e[0], :],
            p[e[3], :],
            p[e[7], :],
            p[e[4], :],
            np.array([0, 1, 1, 0]),
            np.array([0, 0, 1, 1]),
        )

        # normal vectors of face 6
        n_f6_1 = eval_normal_q4(
            p[e[1], :],
            p[e[2], :],
            p[e[6], :],
            p[e[5], :],
            np.array([0, 1, 1, 0]),
            np.array([0, 0, 1, 1]),
        )

        if i == 0:
            # This is the straight section, we dont need to average over the two elements
            p_ret[e[0], :] += n_f5_1[0, :] * delta_phi + n_f3_1[0, :] * delta_r
            p_ret[e[3], :] += n_f5_1[1, :] * delta_phi + n_f4_1[1, :] * delta_r

            p_ret[e[1], :] += n_f6_1[0, :] * delta_phi + n_f3_1[1, :] * delta_r
            p_ret[e[2], :] += n_f6_1[1, :] * delta_phi + n_f4_1[0, :] * delta_r

        if i != num_bricks - 1:
            # this is the next element
            e_2 = c[i + 1]

            # evaluate also the next element

            # normal vectors of face 3
            n_f3_2 = eval_normal_q4(
                p[e_2[0], :],
                p[e_2[1], :],
                p[e_2[5], :],
                p[e_2[4], :],
                np.array([0, 1, 1, 0]),
                np.array([0, 0, 1, 1]),
            )

            # normal vectors of face 4
            n_f4_2 = eval_normal_q4(
                p[e_2[2], :],
                p[e_2[3], :],
                p[e_2[7], :],
                p[e_2[6], :],
                np.array([0, 1, 1, 0]),
                np.array([0, 0, 1, 1]),
            )

            # normal vectors of face 5
            n_f5_2 = -1.0 * eval_normal_q4(
                p[e_2[0], :],
                p[e_2[3], :],
                p[e_2[7], :],
                p[e_2[4], :],
                np.array([0, 1, 1, 0]),
                np.array([0, 0, 1, 1]),
            )

            # normal vectors of face 6
            n_f6_2 = eval_normal_q4(
                p[e_2[1], :],
                p[e_2[2], :],
                p[e_2[6], :],
                p[e_2[5], :],
                np.array([0, 1, 1, 0]),
                np.array([0, 0, 1, 1]),
            )

            # Average over the two elements

            # r direction
            # node 5
            n_5_r, s_5_r = compute_average_normal_vector(n_f3_1[3, :], n_f3_2[0, :])

            # node 6
            n_6_r, s_6_r = compute_average_normal_vector(n_f3_1[2, :], n_f3_2[1, :])

            # node 7
            n_7_r, s_7_r = compute_average_normal_vector(n_f4_1[3, :], n_f4_2[0, :])

            # node 8
            n_8_r, s_8_r = compute_average_normal_vector(n_f4_1[2, :], n_f4_2[1, :])

            # phi direction
            # node 5
            n_5_phi, s_5_phi = compute_average_normal_vector(n_f5_1[3, :], n_f5_2[0, :])

            # node 6
            n_6_phi, s_6_phi = compute_average_normal_vector(n_f6_1[3, :], n_f6_2[0, :])

            # node 7
            n_7_phi, s_7_phi = compute_average_normal_vector(n_f6_1[2, :], n_f6_2[1, :])

            # node 8
            n_8_phi, s_8_phi = compute_average_normal_vector(n_f5_1[2, :], n_f5_2[1, :])

            # shift the nodes
            p_ret[e[4], :] += s_5_phi * n_5_phi * delta_phi + s_5_r * n_5_r * delta_r
            p_ret[e[5], :] += s_6_phi * n_6_phi * delta_phi + s_6_r * n_6_r * delta_r
            p_ret[e[6], :] += s_7_phi * n_7_phi * delta_phi + s_7_r * n_7_r * delta_r
            p_ret[e[7], :] += s_8_phi * n_8_phi * delta_phi + s_8_r * n_8_r * delta_r

        else:
            # Define normal vectors between points in F2
            nr1 = p_ret[e[4], :] - p_ret[e[5], :]
            nr2 = p_ret[e[7], :] - p_ret[e[6], :]
            np1 = p_ret[e[4], :] - p_ret[e[7], :]
            np2 = p_ret[e[5], :] - p_ret[e[6], :]

            nr1_n, nr2_n, np1_n, np2_n = map(lambda x: x / np.linalg.norm(x), [nr1, nr2, np1, np2])

            p_ret[e[4], :] += +nr1_n * delta_r + np1_n * delta_phi
            p_ret[e[5], :] += -nr1_n * delta_r + np2_n * delta_phi
            p_ret[e[6], :] += -nr2_n * delta_r - np2_n * delta_phi
            p_ret[e[7], :] += +nr2_n * delta_r - np1_n * delta_phi

    return p_ret
