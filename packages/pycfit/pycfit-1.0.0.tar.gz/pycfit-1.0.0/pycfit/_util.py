"""
Utility Functions
"""
import re
import sys
import ast
import math
# import asdf
import warnings
import numpy as np
from functools import reduce
from operator import add
from scipy.optimize._optimize import OptimizeResult
from astropy.modeling.fitting import DEFAULT_EPS
from astropy.modeling import Model
from pathlib import Path
import importlib.util
# from ._grid import Grid

# Define the approved TiedFunction implementation
APPROVED_TIED_FUNCTION = '''
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
'''


def load_fit_info(FC_dict):
    '''
    Take a fit container dictionary from 
    ASDF storage and turn it back into an array of 
    scipy OptimizeResult objects
    '''
    # TODO -- vectorize
    fit_info = np.full(FC_dict['status'].shape, None, dtype=object)
    for (i,j),_ in np.ndenumerate(fit_info):
        fit_info[i,j] = OptimizeResult(message=FC_dict['message'][i,j],
                            success=FC_dict['success'][i,j],
                            status=FC_dict['status'][i,j],
                            fun=FC_dict['fun'][i,j],
                            x=FC_dict['x'][i,j],
                            cost=FC_dict['cost'][i,j],
                            jac=FC_dict['jac'][i,j],
                            grad=FC_dict['grad'][i,j],
                            optimality=FC_dict['optimality'][i,j],
                            active_mask=FC_dict['active_mask'][i,j],
                            nfev=FC_dict['nfev'][i,j],
                            njev=FC_dict['njev'][i,j],
                            param_cov=FC_dict['param_cov'][i,j])      
    return fit_info


def first_nonzero_decimal_place(x):
    if x == 0:
        return None
    s = f"{abs(x):.20f}"  # 20 decimal places should be enough for most practical floats
    decimal_part = s.split('.')[1]
    for i, ch in enumerate(decimal_part):
        if ch != '0':
            return i + 1  # 1-based indexing for "place-values"


def isMonotonic(arr0):
    """
    Is this array monotonic (excludind NaNs)?
    """
    arr = np.array(arr0)
    diffs = np.diff(arr[np.isfinite(arr)])
    return np.all(diffs >= 0) or np.all(diffs <= 0)


def ConvertFloat(s) :
    """
    Convert a string to a finite floating point
    Return None if invalid
    """
    try :
        f = float(s)
    except ValueError :
        return None
    
    if not math.isfinite(f) :
        return None	
    return f


def _none_to_nan(val) :
    """ Convert None to NaN	"""
    return np.nan if val is None else val


def eliminate_axis(shape, axis) :
    """ The shape of a dataset after removing one axis """
    return tuple(dim for i, dim in enumerate(shape) if axis!=i)


def expand_array(arr, shape, axis) :
    """ Turn a 1-D array into a multi-D array by repeating elements """
    if arr.ndim != 1 : raise ValueError('arr must be one dimensional')
    if arr.shape[0] != shape[axis] : raise ValueError('dimension size mismatch')
    
    arr = arr[tuple((slice(None) if axis == _axis else np.newaxis) for _axis, s in enumerate(shape))]
    
    for _axis, s in enumerate(shape) :
        if axis != _axis :
            arr = np.repeat(arr, s, axis=_axis)
    
    return arr



def extract_parameter_uncertainties(fit_info_container, param_names):
    cov_matrices = fit_info_container.get_property_as_array('param_cov')
    nx, ny, np1, np2 = cov_matrices.shape
    assert np1 == np2 and np1 == len(param_names), "Bad arguments"

    cov_mat_list = cov_matrices.reshape(-1, np1, np2)
    uncertainties = {}
    for idx, param_name in enumerate(param_names):
        # Extract standard errors (square root of diagonal elements of covariance matrix)
        std_values = np.array([np.sqrt(max(0, cov[idx, idx])) for cov in cov_mat_list])
        uncertainties[param_name] = std_values.reshape(nx, ny)
    return uncertainties
     

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
    

## -- Sum Components -- ##
class _FakeModel :
    def __init__(self, param_names, params, offset_param_name=None) :
        self.param_names = param_names
        self.values = dict(zip(param_names, params))
        
        if offset_param_name is not None :
            self.values[offset_param_name] += DEFAULT_EPS
    
    def __getattr__(self, name) :		
        return self.values[name]

# Class to represent the Jacobian of a sum of componenets
class _Jacobian :
    def __init__(self, model, *components, transfer_jac=True) :
        self.model = model
        self.components = components
        self.transfer_jac = transfer_jac
        # print("_Jacobian: A", flush=True)

        # Set the slices of the parameters that will be passed that correspond to each component
        self.param_slices = []
        i = 0
        for component in components :
            self.param_slices.append(slice(i, i+len(component.param_names)))
            i += len(component.param_names)
        # print("_Jacobian: B", flush=True)

    # Calculate the Jacobian
    def __call__(self, xdata, *params) :
        # print("_Jacobian: C", flush=True)

        jac = []
        for component, param_slice in zip(self.components, self.param_slices) :
            if component.col_fit_deriv :
                jac.extend(component.fit_deriv(xdata, *params[param_slice]))
            else :
                jac.extend(component.fit_deriv(xdata, *params[param_slice]).T)
        
        # Calculate derivatives of jac components with regard to tied parameters
        if self.transfer_jac and any(callable(tied) for tied in self.model.tied.values()) :
            center = _FakeModel(self.model.param_names, params)
            offsets = [_FakeModel(self.model.param_names, params, offset_param_name) for offset_param_name in self.model.param_names]
            
            for i, (param_name, tied) in enumerate(self.model.tied.items()) :
                if not callable(tied) : continue
                
                center_val = tied(center)
                offset_vals = np.array([tied(offset) for offset in offsets])
                derivs = (offset_vals - center_val) / DEFAULT_EPS
                
                for j, deriv in enumerate(derivs) :
                    if not np.isclose(0.0, deriv) :
                        jac[j] += deriv * jac[i]
        
        return jac


def sum_components(*components, transfer_jac=True) :
    """
    Combine models via addition
    Create a new fit_deriv (Jacobian) that combines the fit_deriv results of the individual componenets
    TODO: Evaluate if this can be removed now that astropy 7.1+ is released.
    """
    
    if not components :
        raise TypeError('Must give at least one component')
    
    if len(components) == 1 :
        return components[0]
    
    # Add up the component models
    compound_model = reduce(add, components)
    
    # Create Jacobian if it does not exist
    if compound_model.fit_deriv is None:
        # If each componenet has a Jacobian function
        if all(component.fit_deriv is not None for component in components) :
            # print("sum_components: A", flush=True)
            # try:
            compound_model.fit_deriv = _Jacobian(compound_model, *components, transfer_jac=transfer_jac)
            # print("sum_components: BBBB", flush=True)
            
            # compound_model.col_fit_deriv = True
        else :
            warnings.warn('Building model without Jacobian. This will adversely affect fitting run time.')
    
    # print("sum_components: C", flush=True)
       
    return compound_model


def auto_adjust_bounds(p):
    """
    To use after adjusting a parameter value.
    If fitting is bounded, will check if the new value is within bounds.
    If not, will adjust the bounds so that fit won't fail due to bad 
    initial condition.

    p:  astropy.modeling.parameters.Parameter type
    """
    if (not p.fixed) and (p.bounds != (None, None)):
        too_low = True if (p.bounds[0] is not None) and (p.value <= p.bounds[0]) else False
        too_high = True if (p.bounds[1] is not None) and (p.value >= p.bounds[1]) else False
        if too_low or too_high:
            lower_bound = p.bounds[0]
            upper_bound = p.bounds[1]
            if too_low:
                if upper_bound is None:
                    delta = lower_bound - p.value
                    lower_bound -= (delta * 3)
                else:
                    delta = upper_bound - lower_bound
                    lower_bound -= delta/2

            if too_high:
                if lower_bound is None:
                    delta = p.value - upper_bound
                    upper_bound += (delta * 3)
                else:
                    delta = upper_bound - lower_bound
                    upper_bound += delta/2

            p.bounds = (lower_bound, upper_bound)
    return




######### For loading saved models from a passed `.py` module file

class ValidationError(Exception):
    pass

def load_defined_model(file_path):
    """
    Validate Python module for creating astropy model
    and return the defined model

    Must have a `define_model()` function defined
    """

    temp_module_name = 'this_module'
    original_module = sys.modules.get(temp_module_name)

    file_path = Path(file_path)
    
    # 1. Basic file checks
    if not file_path.exists():
        raise ValidationError(f"File does not exist: {file_path}")
    
    if not file_path.is_file():
        raise ValidationError(f"Path is not a file: {file_path}")
    
    if file_path.suffix != '.py':
        raise ValidationError(f"File must be a Python file (.py), got: {file_path.suffix}")
    
    # Check file size
    if file_path.stat().st_size > 1024 * 1024:  # 1MB limit
        raise ValidationError(f"File too large: {file_path.stat().st_size} bytes")
    
    # 2. Content safety check
    try:
        validate_python_file_safety(file_path)
    except ValidationError as e:
        print(f"Warning: Safety validation failed: {e}")
        return None
    else:

    # 3. If safe: Import and validate the module; return defined model
        try:
            module = validate_and_import_module(file_path, 
                                                required_items={'define_model': callable}, 
                                                module_name=temp_module_name)
            loaded_model = module.define_model()
            if isinstance(loaded_model, Model):
                return loaded_model
            else: 
                print(f"Warning: File does not define an astropy model. No model loaded.")
                return None
        except:
            print(f"Warning: File does not meet specifications. No model loaded.")
            return None
        finally:
            # Cleanup loaded module
            if original_module is not None:
                sys.modules[temp_module_name] = original_module
            else:
                sys.modules.pop(temp_module_name, None)


def validate_and_import_module(file_path, required_items=None, module_name='this_module'):
    """
    Import and validate a Python module using pathlib.
    
    Args:
        file_path (str or Path): Path to the .py file
        required_items (dict): Dict of {name: type} for required items
    
    Returns:
        The imported module object
    """
    if required_items is None:
        required_items = {}
    
    # Import the module
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not find module specification for {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    # Validate required items
    for item_name, expected_type in required_items.items():
        if not hasattr(module, item_name):
            raise ValidationError(f"Module missing required item: {item_name}")
        
        item = getattr(module, item_name)
        
        if expected_type == type and not isinstance(item, type):
            raise ValidationError(f"{item_name} should be a class, got {type(item)}")
        elif expected_type == callable and not callable(item):
            raise ValidationError(f"{item_name} should be callable, got {type(item)}")
        elif expected_type != type and expected_type != callable:
            if not isinstance(item, expected_type):
                raise ValidationError(f"{item_name} should be {expected_type}, got {type(item)}")
    
    return module


def validate_python_file_safety(file_path):
    """
    Safety check that allows approved TiedFunction implementation 
    but flags other dangerous operations.
    """
    file_path = Path(file_path)
    
    dangerous_functions = {
        'exec', 'compile', '__import__', 'open', 
        'file', 'input', 'raw_input', 'execfile'
        # Note: 'eval' is handled specially below
    }
    
    dangerous_modules = {
        'os', 'sys', 'subprocess', 'shutil', 'pickle', 'socket'
    }
    
    # Read the file content
    content = file_path.read_text(encoding='utf-8')
    tree = ast.parse(content)
    
    # First, check if TiedFunction exists and validate it if present
    tied_function_node = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == 'TiedFunction':
            tied_function_node = node
            break
    
    if tied_function_node is not None:
        # Validate that TiedFunction matches approved implementation
        validate_tied_function_implementation(content, tied_function_node)
    
    # Now check for dangerous operations, but skip eval() inside approved TiedFunction
    for node in ast.walk(tree):
        # Check for eval() calls
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'eval':
            # Check if this eval is inside TiedFunction.__call__
            if not is_eval_in_tied_function_call(node, tied_function_node):
                raise ValidationError(f"Dangerous eval() call detected outside of approved TiedFunction")
        
        # Check for other dangerous function calls
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in dangerous_functions:
                raise ValidationError(f"Dangerous function call detected: {node.func.id}")
        
        # Check for dangerous imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in dangerous_modules:
                    raise ValidationError(f"Dangerous import detected: {alias.name}")
        
        if isinstance(node, ast.ImportFrom):
            if node.module in dangerous_modules:
                raise ValidationError(f"Dangerous import detected: {node.module}")
    
    return True

def validate_tied_function_implementation(file_content, tied_function_node):
    """
    Validate that TiedFunction implementation matches the approved version.
    """
    # Extract the TiedFunction class from the file content
    start_line = tied_function_node.lineno - 1  # AST uses 1-based line numbers
    end_line = tied_function_node.end_lineno if hasattr(tied_function_node, 'end_lineno') else None
    
    lines = file_content.split('\n')
    
    if end_line:
        tied_function_lines = lines[start_line:end_line]
    else:
        # Fallback: find the end by looking for the next class/function or end of file
        tied_function_lines = []
        for i in range(start_line, len(lines)):
            line = lines[i].strip()
            # Stop if we hit another top-level definition
            if i > start_line and (line.startswith('class ') or line.startswith('def ')):
                break
            tied_function_lines.append(lines[i])
    
    actual_implementation = '\n'.join(tied_function_lines)
    
    # Normalize both implementations for comparison (remove extra whitespace)
    def normalize_code(code):
        # Remove leading/trailing whitespace, normalize internal whitespace
        normalized = re.sub(r'\s+', ' ', code.strip())
        # Remove spaces around certain characters for more flexible matching
        normalized = re.sub(r'\s*([(),:{}])\s*', r'\1', normalized)
        return normalized
    
    actual_norm = normalize_code(actual_implementation)
    approved_norm = normalize_code(APPROVED_TIED_FUNCTION)
    
    if actual_norm != approved_norm:
        raise ValidationError(
            "TiedFunction implementation does not match approved version. "
            f"Found:\n{actual_implementation}\n\n"
            f"Expected something equivalent to:\n{APPROVED_TIED_FUNCTION}"
        )

def is_eval_in_tied_function_call(eval_node, tied_function_node):
    """
    Check if an eval() call is inside TiedFunction class definition.
    """
    if tied_function_node is None:
        return False

    # Check if the eval_node is within the TiedFunction class definition
    # This is a check based on line numbers
    start_line = tied_function_node.lineno - 1  # AST uses 1-based line numbers
    end_line = tied_function_node.end_lineno if hasattr(tied_function_node, 'end_lineno') else start_line + 10

    eval_line = eval_node.lineno
    return start_line <= eval_line <= end_line
