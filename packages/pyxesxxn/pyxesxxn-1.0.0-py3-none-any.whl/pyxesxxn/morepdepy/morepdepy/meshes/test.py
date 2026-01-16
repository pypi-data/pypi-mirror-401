"""Test implementation of the mesh
"""

__all__ = []

from morepdepy.tests.doctestPlus import _LateImportDocTestSuite
import morepdepy.tests.testProgram

def _suite():
    return _LateImportDocTestSuite(docTestModuleNames = (
        'morepdepy.meshes.mesh',
        'morepdepy.meshes.mesh2D',
        'morepdepy.meshes.nonUniformGrid1D',
        'morepdepy.meshes.nonUniformGrid2D',
        'morepdepy.meshes.nonUniformGrid3D',
        'morepdepy.meshes.tri2D',
        'morepdepy.meshes.gmshMesh',
        'morepdepy.meshes.periodicGrid1D',
        'morepdepy.meshes.periodicGrid2D',
        'morepdepy.meshes.periodicGrid3D',
        'morepdepy.meshes.uniformGrid1D',
        'morepdepy.meshes.uniformGrid2D',
        'morepdepy.meshes.uniformGrid3D',
        'morepdepy.meshes.cylindricalUniformGrid1D',
        'morepdepy.meshes.cylindricalUniformGrid2D',
        'morepdepy.meshes.cylindricalNonUniformGrid1D',
        'morepdepy.meshes.cylindricalNonUniformGrid2D',
        'morepdepy.meshes.sphericalUniformGrid1D',
        'morepdepy.meshes.sphericalNonUniformGrid1D',
        'morepdepy.meshes.factoryMeshes',
        'morepdepy.meshes.abstractMesh',
        'morepdepy.meshes.representations.gridRepresentation'))

if __name__ == '__main__':
    morepdepy.tests.testProgram.main(defaultTest='_suite')
