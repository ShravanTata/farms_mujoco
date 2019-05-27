"""Oscillator naming convention"""

def bodyosc2index(joint_i, side=0, n_body_joints=11):
    """body2index"""
    assert joint_i < 11, "Joint must be < 11, got {}".format(joint_i)
    return joint_i + side*n_body_joints


def legosc2index(leg_i, side_i, joint_i, side=0, **kwargs):
    """legosc2index"""
    n_body_joints = kwargs.pop("n_body_joints", 11)
    n_legs_dof = kwargs.pop("n_legs_dof", 4)
    return (
        2*n_body_joints
        + leg_i*2*n_legs_dof*2  # 2 oscillators, 2 legs
        + side_i*n_legs_dof*2  # 2 oscillators
        + joint_i
        + side*n_legs_dof
    )


def leglink2index(leg_i, side_i, joint_i, n_body_links=12, n_legs_dof=4):
    """leglink2index"""
    return (
        n_body_links - 1
        + leg_i*2*n_legs_dof
        + side_i*n_legs_dof
        + joint_i
    )


def leglink2name(leg_i, side_i, joint_i):
    """leglink2index"""
    return "link_leg_{}_{}_{}".format(leg_i, "R" if side_i else "L", joint_i)


def legjoint2index(leg_i, side_i, joint_i, n_body_joints=11, n_legs_dof=4):
    """legjoint2index"""
    return (
        n_body_joints
        + leg_i*2*n_legs_dof
        + side_i*n_legs_dof
        + joint_i
    )


def legjoint2name(leg_i, side_i, joint_i):
    """legjoint2index"""
    return "joint_{}".format(leglink2name(leg_i, side_i, joint_i))
