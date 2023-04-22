import clr
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from System.Collections.Generic import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

elements = UnwrapElement(IN[0])
prefix_name = IN[1]

TransactionManager.Instance.EnsureInTransaction(doc)

families = []
for el in elements:
	if (el.GetType()).Name == "FamilyInstance":
		family = el.Symbol.Family
		if family.IsInPlace == True:
			if not (family.Name).startswith(prefix_name):
				family.Name = prefix_name + family.Name
			families.append(family)			

TransactionManager.Instance.TransactionTaskDone()

OUT = families
