
from astropy.modeling.models import Const1D
from astropy.modeling.models import Linear1D
from astropy.modeling.models import Polynomial1D
from astropy.modeling.models import Gaussian1D 
from astropy.modeling.models import Moffat1D

import math
import numpy as np


class TiedFunction :
    """ Object used to represent an expression for a Tied astropy parameter """
    def __init__(self, expr) :
        self.expr = expr

    def __call__(self, model) :
        return eval(self.expr, {'np':np, 'math':math}, {param_name:getattr(model, param_name) for param_name in model.param_names})

    def __str__(self) :
        return self.expr

    def __repr__(self) :
        return 'TiedFunction(%r)' % self.expr

def define_model():
    model = Const1D() + Gaussian1D() + Moffat1D()

    # Constant_0
    model.amplitude_0.value = 0.242
    model.amplitude_0.fixed = False
    model.amplitude_0.bounds = (-24.0, 32.0)
    model.amplitude_0.tied = False

    # Gaussian_1
    model.amplitude_1.value = 1.216
    model.amplitude_1.fixed = False
    model.amplitude_1.bounds = (0.0001, 1197.5557113492155)
    model.amplitude_1.tied = False
    model.mean_1.value = 972.628
    model.mean_1.fixed = False
    model.mean_1.bounds = (972.0444473959998, 972.8142873959997)
    model.mean_1.tied = False
    model.stddev_1.value = 0.434
    model.stddev_1.fixed = False
    model.stddev_1.bounds = (0.03849199999999656, 3.849199999999655)
    model.stddev_1.tied = False

    # Moffat_2
    model.amplitude_2.value = 4.864
    model.amplitude_2.fixed = False
    model.amplitude_2.bounds = (0.0001, 3322.2938085400724)
    model.amplitude_2.tied = TiedFunction("amplitude_1 * 4")
    model.x_0_2.value = 977.131
    model.x_0_2.fixed = False
    model.x_0_2.bounds = (976.4710273959998, 979.3940136459998)
    model.x_0_2.tied = False
    model.gamma_2.value = 1.231
    model.gamma_2.fixed = False
    model.gamma_2.bounds = (0.01924599999999828, 1.9245999999998276)
    model.gamma_2.tied = False
    model.alpha_2.value = 3.851
    model.alpha_2.fixed = False
    model.alpha_2.bounds = (1.0, 10.0)
    model.alpha_2.tied = False

    return model
