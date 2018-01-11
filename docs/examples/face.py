# Internal Modules
from pyiges.IGESCore import IGEStorage
from pyiges.IGESGeomLib import IGESPoint
import pyiges.IGESGeomLib as IGES
import numpy

system = IGEStorage()
system.StartSection.Prolog = " "
system.GlobalSection.IntegerBits = int(32)
system.GlobalSection.SPMagnitude = int(38)
system.GlobalSection.SPSignificance = int(6)
system.GlobalSection.DPMagnitude = int(38)
system.GlobalSection.DPSignificance = int(15)
system.GlobalSection.MaxNumberLineWeightGrads = int(8)
system.GlobalSection.WidthMaxLineWeightUnits = float(0.016)
system.GlobalSection.MaxCoordValue = float(71)

from scipy.special import comb


def bernstein_poly(n, i, u):
    return comb(n, i) * u ** (i) * (1 - u) ** (n - i)


def bezier_curve(P, nTimes = 1000, dC = False):

    n = len(P[1])
    u = numpy.linspace(0.0, 1.0, nTimes)
    polynomial_array = numpy.empty([n, nTimes])

    for i in range(0, n):
        polynomial_array[i] = bernstein_poly(n - 1, i, u)

    return numpy.dot(P, polynomial_array)

print(system)

P = [[0, 0],
     [numpy.divide(1, 3), numpy.divide(numpy.pi, 6)],
     [numpy.divide(2, 3), 1],
     [1, 1],
     [1 + numpy.divide(1, 3), 1],
     [1 + numpy.divide(2, 3), numpy.divide(numpy.pi, 6)],
     [2, 0],
     [2 + numpy.divide(1, 3), 0 - numpy.divide(numpy.pi, 6)],
     [2 + numpy.divide(2, 3), 0 - 1],
     [3, 0 - 1],
     [3 + numpy.divide(1, 3), 0 - 1],
     [3 + numpy.divide(2, 3), 0 - numpy.divide(numpy.pi, 6)],
     [4, 0]]

for i in range(0, 1):
    P.extend

P = numpy.transpose(P)
bezi = bezier_curve(P, nTimes = 50)

polyln = IGES.IGESGeomPolyline()
system.Commit(polyln)

line = IGES.IGESGeomLine(IGESPoint(-2, -5, 0), IGESPoint(22, -5, 0))
print(line)
system.Commit(line)

line = IGES.IGESGeomLine(IGESPoint(-2, -1, 0), IGESPoint(22, -3, 3))
print(line)
system.Commit(line)


system.Commit(IGES.IGESRevolve(polyln, line))

# system.Commit(IGES.IGESExtrude(polyln.DirectoryDataPointer.data, IGESPoint(0,0,10)))

# system.Commit(IGES.IGESRevolve(line0, line))
#system.Commit(IGES.IGESRevolve(polyln, line))

#system.Commit(IGES.IGESExtrude(polyln.DirectoryDataPointer.data, IGESPoint(0,0,10)))
print(system)
filename = "/tmp/face.iges"
system.save(filename)
