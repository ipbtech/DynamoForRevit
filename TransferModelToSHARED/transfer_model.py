import clr
clr.AddReference('RevitAPI') # Основная библиотека Revit API
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager as DM

doc = DM.Instance.CurrentDBDocument
path_doc = doc.PathName
bfi = BasicFileInfo.Extract(path_doc)


""" Через Username. Работает только на лицензионных версиях
if doc.IsWorkshared:
	username = bfi.Username
	z = path_doc.rfind("\\") + 1
	file_name = path_doc[z:len(path_doc)]
	file_name_edit = file_name.replace(("_" + username), "")
	file_path = path_doc[0:z]
	OUT = path_doc, file_name_edit
"""

if doc.IsWorkshared:
	z = bfi.CentralPath.rfind("\\") + 1
	file_name = bfi.CentralPath[z:len(bfi.CentralPath)]
	OUT =  bfi.CentralPath, file_name
else: 
	z = path_doc.rfind("\\") + 1
	file_name = path_doc[z:len(path_doc)]	
	OUT = path_doc, file_name
