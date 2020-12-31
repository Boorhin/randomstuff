import netCDF4 as nc
import numpy as np
import pyvista as pv
from pyvistaqt import BackgroundPlotter
#from pyproj import Transformer

#Inspired by https://docs.pyvista.org/examples/02-plot/spherical.html

def _cell_bounds(points, bound_position=0.5):
    """
    Calculate coordinate cell boundaries.

    Parameters
    ----------
    points: numpy.array
        One-dimensional array of uniformy spaced values of shape (M,)
    bound_position: bool, optional
        The desired position of the bounds relative to the position
        of the points.

    Returns
    -------
    bounds: numpy.array
        Array of shape (M+1,)

    Examples
    --------
    >>> a = np.arange(-1, 2.5, 0.5)
    >>> a
    array([-1. , -0.5,  0. ,  0.5,  1. ,  1.5,  2. ])
    >>> cell_bounds(a)
    array([-1.25, -0.75, -0.25,  0.25,  0.75,  1.25,  1.75,  2.25])
    """
    assert points.ndim == 1, "Only 1D points are allowed"
    diffs = np.diff(points)
    delta = diffs[0] * bound_position
    bounds = np.concatenate([[points[0] - delta], points + delta])
    return bounds

### GEBCO_2020 data are downloaded from https://www.gebco.net/data_and_products/gridded_bathymetry_data/
data=nc.Dataset("gebco_2020_netcdf/GEBCO_2020.nc")
el =data ["elevation"]
ratio = 240 #/60minutes /15 secs arc
factor=10
subset=el[::int(ratio/factor),::int(ratio/factor)]#.astype(np.float)#find a way to link them with coord
# Approximate radius of the Earth
RADIUS = 6371000

# Longitudes and latitudes
x = np.arange(0, 360, 1/factor)
y = np.arange(-90, 90, 1/factor)
y_polar = 90.0 - y  # grid_from_sph_coords() expects polar angle

# Create arrays of grid cell boundaries, which have shape of (x.shape[0] + 1)
xx_bounds = _cell_bounds(x)
yy_bounds = _cell_bounds(y_polar)

# Vertical levels
# in this case a single level slightly above the surface of a sphere


grid_scalar = pv.grid_from_sph_coords(xx_bounds, yy_bounds, RADIUS)
p=BackgroundPlotter()
p.add_mesh(grid_scalar, scalars = subset.swapaxes(-2, -1).ravel(),cmap="gist_earth",clim=[-4000,4000])
