# Internal Modules
from pyiges.IGESCore import IGEStorage
from pyiges.IGESGeomLib import IGESPoint
import pyiges.IGESGeomLib as IGES

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

print(system)

line = IGES.IGESGeomLine(IGESPoint(-2, -5, 0), IGESPoint(22, -5, 0))
print(line)
system.Commit(line)

#system.Commit(IGES.IGESRevolve(polyln, line))

#system.Commit(IGES.IGESExtrude(polyln.DirectoryDataPointer.data, IGESPoint(0,0,10)))
print(system)

system.save(filename)
