
from astropy.modeling.models import Const1D
from astropy.modeling.models import Linear1D
from astropy.modeling.models import Polynomial1D
from astropy.modeling.models import Gaussian1D 
from astropy.modeling.models import Moffat1D


def define_model():
    model = Const1D() + Gaussian1D() + Moffat1D()

    # Constant_0
    model.amplitude_0.value = 0.174
    model.amplitude_0.fixed = False
    model.amplitude_0.bounds = (-24.0, 32.0)
    model.amplitude_0.tied = False

    # Gaussian_1
    model.amplitude_1.value = 1.250
    model.amplitude_1.fixed = False
    model.amplitude_1.bounds = (0.0001, 985.9522832490848)
    model.amplitude_1.tied = False
    model.mean_1.value = 972.626
    model.mean_1.fixed = False
    model.mean_1.bounds = (972.4293673959999, 973.1992073959998)
    model.mean_1.tied = False
    model.stddev_1.value = 0.474
    model.stddev_1.fixed = False
    model.stddev_1.bounds = (0.03849199999999656, 3.849199999999655)
    model.stddev_1.tied = False

    # Moffat_2
    model.amplitude_2.value = 7.419
    model.amplitude_2.fixed = False
    model.amplitude_2.bounds = (0.0001, 6719.919706688111)
    model.amplitude_2.tied = False
    model.x_0_2.value = 977.132
    model.x_0_2.fixed = False
    model.x_0_2.bounds = (976.6634873959998, 977.4333273959998)
    model.x_0_2.tied = False
    model.gamma_2.value = 0.636
    model.gamma_2.fixed = False
    model.gamma_2.bounds = (0.03849199999999656, 3.849199999999655)
    model.gamma_2.tied = False
    model.alpha_2.value = 1.950
    model.alpha_2.fixed = False
    model.alpha_2.bounds = (1.0, 10.0)
    model.alpha_2.tied = False

    return model
