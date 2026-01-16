""":ref:`Discretizations <section:discretization>` of partial differential equation expressions
"""
__docformat__ = 'restructuredtext'

class ExplicitVariableError(Exception):
    def __init__(self, s='Terms with explicit Variables cannot mix with Terms with implicit Variables.'):
        Exception.__init__(self, s)

class TermMultiplyError(Exception):
    def __init__(self, s='Must multiply terms by int or float.'):
        Exception.__init__(self, s)

class AbstractBaseClassError(NotImplementedError):
    def __init__(self, s="can't instantiate abstract base class"):
        NotImplementedError.__init__(self, s)

class VectorCoeffError(TypeError):
    def __init__(self, s="The coefficient must be a vector value."):
        TypeError.__init__(self, s)

class SolutionVariableNumberError(Exception):
    def __init__(self, s='Different number of solution variables and equations.'):
        Exception.__init__(self, s)

class SolutionVariableRequiredError(Exception):
    def __init__(self, s='The solution variable needs to be specified.'):
        Exception.__init__(self, s)

class IncorrectSolutionVariable(Exception):
    def __init__(self, s='The solution variable is incorrect.'):
        Exception.__init__(self, s)

class TransientTermError(Exception):
    def __init__(self, s='The equation requires a TransientTerm with explicit convection.'):
        Exception.__init__(self, s)

from morepdepy.terms.transientTerm import *
from morepdepy.terms.diffusionTerm import *
from morepdepy.terms.explicitDiffusionTerm import *
from morepdepy.terms.implicitDiffusionTerm import *
from morepdepy.terms.implicitSourceTerm import *
from morepdepy.terms.residualTerm import *
from morepdepy.terms.centralDiffConvectionTerm import *
from morepdepy.terms.explicitUpwindConvectionTerm import *
from morepdepy.terms.exponentialConvectionTerm import *
from morepdepy.terms.hybridConvectionTerm import *
from morepdepy.terms.powerLawConvectionTerm import *
from morepdepy.terms.upwindConvectionTerm import *
from morepdepy.terms.vanLeerConvectionTerm import *
from morepdepy.terms.firstOrderAdvectionTerm import *
from morepdepy.terms.advectionTerm import *
ConvectionTerm = PowerLawConvectionTerm
