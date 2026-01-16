
from astropy.modeling.models import Const1D
from astropy.modeling.models import Linear1D
from astropy.modeling.models import Polynomial1D
from astropy.modeling.models import Gaussian1D 
from astropy.modeling.models import Moffat1D


def define_model():
    model = Const1D() + Moffat1D() + Gaussian1D()

    # Constant_0
    model.amplitude_0.value = 0.174
    model.amplitude_0.fixed = False
    model.amplitude_0.bounds = (-24.0, 32.0)
    model.amplitude_0.tied = False

    # Moffat_1
    model.amplitude_1.value = 7.419
    model.amplitude_1.fixed = False
    model.amplitude_1.bounds = (0.0001, 7019.648663721635)
    model.amplitude_1.tied = False
    model.x_0_1.value = 977.132
    model.x_0_1.fixed = False
    model.x_0_1.bounds = (976.6634873959998, 977.4333273959998)
    model.x_0_1.tied = False
    model.gamma_1.value = 0.636
    model.gamma_1.fixed = False
    model.gamma_1.bounds = (0.03849199999999656, 3.849199999999655)
    model.gamma_1.tied = False
    model.alpha_1.value = 1.950
    model.alpha_1.fixed = False
    model.alpha_1.bounds = (1.0, 10.0)
    model.alpha_1.tied = False

    # Gaussian_2
    model.amplitude_2.value = 1.250
    model.amplitude_2.fixed = False
    model.amplitude_2.bounds = (0.0001, 1228.1431364816212)
    model.amplitude_2.tied = False
    model.mean_2.value = 972.626
    model.mean_2.fixed = False
    model.mean_2.bounds = (972.4293673959999, 973.1992073959998)
    model.mean_2.tied = False
    model.stddev_2.value = 0.474
    model.stddev_2.fixed = False
    model.stddev_2.bounds = (0.03849199999999656, 3.849199999999655)
    model.stddev_2.tied = False

    return model
