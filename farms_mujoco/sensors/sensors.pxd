"""Cython sensors"""

include 'types.pxd'
include 'sensor_convention.pxd'
import numpy as np

cimport numpy as np
from farms_core.array.array_cy cimport DoubleArray3D
from farms_core.sensors.data_cy cimport ContactsArrayCy, MusclesArrayCy


cpdef cycontacts2data(
    object physics,
    unsigned int iteration,
    ContactsArrayCy data,
    dict geom2data,
    double meters,
    double newtons,
)

cpdef cymusclesensors2data(
    object physics,
    unsigned int iteration,
    MusclesArrayCy data,
    np.int64_t[:, :] musclesensor2data,
    double meters,
    double velocity,
    double newtons,
)

cdef void cymusclesensor2data(
    unsigned int iteration,
    unsigned int index,
    np.int64_t[:] objids,
    DTYPEv3 cdata,
    double[:] d_ctrl,
    double[:] d_act,
    double[:] d_l_mtu,
    double[:] d_v_mtu,
    double[:] d_force,
    double[:, :] m_gainprm,
    double[:, :] m_userprm,
    double imeters,
    double ivelocity,
    double inewtons,
)
