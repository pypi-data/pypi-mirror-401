"""" test code for dask fitting """


import pycfit
wavelength, intensity, uncertainty, mask = pycfit.data.get_example_grid_spectra(patch=True)
wavelength.shape
wavelength
intensity.shape
intensity[:, 0, 0]
uncertainty[:,0,0]
mask[:, 0 , 0]
intn = intensity[:, 0, 0]
uncr = uncertainty[:, 0, 0]
from astropy.modeling.models import Gaussian1D, Const1D
model = Gaussian1D() + Const1D()
model
max(intn)
np.nanmax(intn)
import numpy as np
np.nanmax(intn)
intn
model.amplitude_0 = 10
model.mean_0 = 974
wavelength
model
from astropy.modeling.fitting import TRFLSQFitter
fitter = TRFLSQFitter()
fitter = TRFLSQFitter?
fitter = TRFLSQFitter(calc_uncertainties=True)