# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True
import numpy as np
cimport numpy as cnp
from libc.math cimport sin, cos, atan2, sqrt, M_PI

def haversine_cython_array(cnp.float64_t[:] lat1, cnp.float64_t[:] lon1, 
                           cnp.float64_t[:] lat2, cnp.float64_t[:] lon2):
    """Version Cython typée pour traiter des MemoryViews (tableaux NumPy)."""
    cdef int n = lat1.shape[0]
    cdef cnp.float64_t[:] res = np.empty(n, dtype=np.float64)
    cdef int i
    cdef double r = 6371.0
    cdef double p1, p2, dp, dl, a
    cdef double d2r = M_PI / 180.0

    for i in range(n):
        p1 = lat1[i] * d2r
        p2 = lat2[i] * d2r
        dp = (lat2[i] - lat1[i]) * d2r
        dl = (lon2[i] - lon1[i]) * d2r
        
        a = sin(dp/2)**2 + cos(p1) * cos(p2) * sin(dl/2)**2
        res[i] = 2 * r * atan2(sqrt(a), sqrt(1 - a))
        
    return np.asarray(res)