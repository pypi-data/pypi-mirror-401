"""
Central location for all interactive help menu text
"""


# Main Single Spectrum Dialog
single_fit_help = dict()

single_fit_help['graph'] = """
<h4>Graph Component Display with Sum</h4>
<ul>
    <li>Double click to add a Component</li>
    <li>Adjust the Component shape with the drag handles ('+')</li>
    <li>Sum of the Components is displayed with the thicker white trace</li>
</ul>
"""

single_fit_help['residual'] = """
<h4>Residuals</h4>
<ul>
    <li>Thick white trace is residual of data and compound model</li>
    <li>Error bars are shown for each data point</li>
</ul>
"""

single_fit_help['tree_view'] = """
<h4>Component Tree Display</h4>
<p>Examine and modify each of the Component parts of the compound model</p>
<ul>
    <li>Double-click a Component name to edit its description</li>
    <li>Double-click a Parameter name to edit its value and contraints</li>
    <li>The `Value` column displays the current state of each Parameter and 
        will update with actions to the interactive graph window</li>
    <li>The `Constraint` column displays the constraints on this
        Parameter during the fitting process<\li>
</ul>
"""

single_fit_help['export'] = """Store the compound model as a Python module or a Pickle file"""

single_fit_help['fit'] = """Fit the data with the compound model using Parameter initial conditions and constraints as set"""

single_fit_help['ok'] = """Exit the interface and return the compound model"""

single_fit_help['cancel'] = """Exit the interface and return the unchanged, initial model.
[`None` if called without an initial model]
"""

# Parameter Sub-dialog
single_fit_help['param'] = dict()

single_fit_help['param']['value'] = """Current value of Parameter. Used as initial condition for fitting"""

single_fit_help['param']['free'] = """Select the `Free` option to allow this Parameter to be adjusted freely (within bounds) during fitting"""

single_fit_help['param']['fixed'] = """Select the `Fixed` option to hold this Parameter unchanged at the set value during fitting"""

single_fit_help['param']['tied'] = """
<p>Select the `Tied` option to constrain the fitting such that this Parameter
maintains a given relationship with one or more other Parameters in the compound model</p>
<ul>
    <li>Use the unique Parameter names to define the relationship in the `Expression` text box</li>
    <li>Use standard Python mathematical operators</li>
    <li>Do not use `=`, just define the right-hand side of the equation.  I.e.:</li>
</ul>
<h4>Example:</h4>
<p>If adjusting Parameter `amplitude_1`, and wanting it to satisfy the equation</p>
<ul><li>amplitude_1 = 4 * amplitude_0</li></ul>
<p>Then the text in the Expression box should read</p>
<ul><li>4 * amplitude_0</li></ul>
"""
single_fit_help['param']['lb'] = """If selected, limit the fitted value of this Parameter by this lower bound"""

single_fit_help['param']['ub'] = """If selected, limit the fitted value of this Parameter by this upper bound"""

single_fit_help['param']['expression'] = """
<p>Define the Tied contraint relationship</p>
<ul>
    <li>Use the unique Parameter names to define the relationship in this text box</li>
    <li>Use standard Python mathematical operators</li>
    <li>Do not use `=`, just define the right-hand side of the equation</li>
</ul>
<h4>Example:</h4>
<p>If adjusting Parameter `amplitude_1`, and wanting it to satisfy the equation</p>
<ul><li>amplitude_1 = 4 * amplitude_0</li></ul>
<p>Then the text in the Expression box should read</p>
<ul><li>4 * amplitude_0</li></ul>
"""

single_fit_help['param']['ok'] = """Exit this dialog and keep the changes"""

single_fit_help['param']['cancel'] = """Exit this dialog and discard the changes"""


# Block Fit Dialog
block_fit_help = dict()

block_fit_help['overview'] = """
<h4>Overview</h4>
<p>Measured data and fitted model at the selected (X,Y) location</p>
"""

block_fit_help['setpoint'] = """
<p>Update the selected (X,Y,λ) point</p>
<p>Also adjust this point by double-clicking in one of the lower 6 panels</p>
"""

block_fit_help['mask'] = """Remove this (X,Y) point from fitting. No fitted model parameters will be returned with results"""

block_fit_help['maskedpoints'] = """Open an interface to see the currently masked points"""

block_fit_help['redosingle'] = """Open an interactive dialog to adjust the fit at a single (X,Y) location"""

block_fit_help['redogrid'] = """Use parallel fitting across the entire raster, using current Paramater values at each location as initial conditions"""

block_fit_help['intensity0'] = """Use this column to explore intensity values across the data cube"""

block_fit_help['intensity1'] = """
<h4>Intensity Heatmap</h4>
<p>A heatmap of intensity at one λ, X, or Y value shown across the remaining 2 axes</p>
For instance:
<p> - intensity at λ across X x Y</p>
<p> - intensity at X across Y x λ</p>

<ul>
<li>Double-click to select a different point for focus</li>
<li>Right-click on the color bar to adjust the color table</li>
<li>Drag the white grab-points in the color bar to adjust the color range</li>
</ul>
"""

block_fit_help['intensity2'] = """
<h4>Intensity lineplot</h4>
<p>A lineplot of intensity across λ, X, or Y with the remaining axes fixed.</p>
For instance:
<p> - intensity across λ at (X,Y)</p>
<p> - intensity across X at (Y,λ)</p>
<ul><li>Double-click to select a different point for focus</li></ul>
"""

block_fit_help['parameter0'] = """
<p>Use this column to explore the fitted parameter values across the data cube</p>
<p>Select Parameter via the drop-down below</p>"""

block_fit_help['parameter1'] = """
<h4>Parameter Select</h4>
<p>Use this drop-down to select the active Parameter to explore</p>
"""

block_fit_help['parameter2'] = """
<h4>Parameter Heatmap</h4>
<p>A heatmap of the selected Parameter across the X,Y grid</p>
<ul>
<li>Double-click to select a different point for focus</li>
<li>Right-click on the color bar to adjust the color table</li>
<li>Drag the white grab-points in the color bar to adjust the color range</li>
</ul>
"""

block_fit_help['parameter3'] = """
<h4>Parameter lineplot</h4>
<p>A lineplot of the selected Parameter across X or Y with the remaining axis fixed.</p>
For instance:
<p> amplitude_0 across X at Y = 5</p>
<ul><li>Double-click to select a different point for focus</li></ul>
"""

block_fit_help['residuals0'] = """Use this column to explore the residuals between the data and fitted model values across the data cube"""
block_fit_help['residuals1'] = """
<h4>Residuals Heatmap</h4>
<p>A heatmap of residuals at one λ, X, or Y value shown across the remaining 2 axes</p>
For instance:
<p> - residuals at λ across X x Y</p>
<p> - residuals at X across Y x λ</p>

<ul>
<li>Double-click to select a different point for focus</li>
<li>Right-click on the color bar to adjust the color table</li>
<li>Drag the white grab-points in the color bar to adjust the color range</li>
</ul>
"""

block_fit_help['residuals2'] = """
<h4>Residuals lineplot</h4>
<p>A lineplot of residuals across λ, X, or Y with the remaining axes fixed.</p>
For instance:
<p> - residuals across λ at (X,Y)</p>
<p> - residuals across X at (Y,λ)</p>
<ul><li>Double-click to select a different point for focus</li></ul>
"""

block_fit_help['import'] = """Load a fitted block object from an ASDF file"""

block_fit_help['export'] = """Store this fitted block object to an ASDF file"""

block_fit_help['ok'] = """Exit the interface and return the fitted block object model"""

block_fit_help['cancel'] = """Exit the interface and return the unchanged, initial block fit object if one was passed.
[`None` if called without an initial block fit]
"""


