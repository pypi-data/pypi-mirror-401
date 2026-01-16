__docformat__ = 'restructuredtext'

from morepdepy.terms.abstractDiffusionTerm import _AbstractDiffusionTerm
from morepdepy.tools import numerix

__all__ = ["DiffusionTermCorrection"]

class DiffusionTermCorrection(_AbstractDiffusionTerm):

    def _getNormals(self, mesh):
        return mesh._faceCellToCellNormals

    def _treatMeshAsOrthogonal(self, mesh):
        return mesh._isOrthogonal
