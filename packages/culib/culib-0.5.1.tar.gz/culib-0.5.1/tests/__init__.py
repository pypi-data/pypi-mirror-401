import numpy as np

# Handle Numpy breaking change with Pytest doctest with NUMBER flag
# (float representation is "np.float64(43.6915)" in Numpy v2.x.x vs "43.6915" in older versions)
if int(np.__version__[0]) >= 2:
    np.set_printoptions(legacy="1.25")
