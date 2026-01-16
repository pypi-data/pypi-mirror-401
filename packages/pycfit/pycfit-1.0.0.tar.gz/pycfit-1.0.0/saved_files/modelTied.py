
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
    model = Const1D() + Moffat1D() + Gaussian1D()

    # Constant_0
    model.amplitude_0.value = 0.210
    model.amplitude_0.fixed = False
    model.amplitude_0.bounds = (-24.0, 32.0)
    model.amplitude_0.tied = False

    # Moffat_1
    model.amplitude_1.value = 5.546
    model.amplitude_1.fixed = False
    model.amplitude_1.bounds = (0.0001, 6927.100960362977)
    model.amplitude_1.tied = TiedFunction("amplitude_2 *4.5")
    model.x_0_1.value = 977.131
    model.x_0_1.fixed = False
    model.x_0_1.bounds = (976.6634873959998, 977.4333273959998)
    model.x_0_1.tied = False
    model.gamma_1.value = 0.895
    model.gamma_1.fixed = False
    model.gamma_1.bounds = (0.03849199999999656, 3.849199999999655)
    model.gamma_1.tied = False
    model.alpha_1.value = 2.529
    model.alpha_1.fixed = False
    model.alpha_1.bounds = (1.0, 10.0)
    model.alpha_1.tied = False

    # Gaussian_2
    model.amplitude_2.value = 1.232
    model.amplitude_2.fixed = False
    model.amplitude_2.bounds = (0.0001, 1234.525259598706)
    model.amplitude_2.tied = False
    model.mean_2.value = 972.627
    model.mean_2.fixed = False
    model.mean_2.bounds = (972.0444473959999, 973.1992073959998)
    model.mean_2.tied = False
    model.stddev_2.value = 0.454
    model.stddev_2.fixed = False
    model.stddev_2.bounds = (0.05773799999999483, 5.581339999999955)
    model.stddev_2.tied = False

    return model
