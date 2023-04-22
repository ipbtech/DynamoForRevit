import System
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
ref_level = UnwrapElement(IN[1])

def get_level_parameter(element):
	if element.Category.Name == "Крыши":
		level_paramater = element.get_Parameter(BuiltInParameter.ROOF_BASE_LEVEL_PARAM)
	if element.Category.Name == "Обобщенные модели" or element.Category.Name == "Каркас несущий" or element.Category.Name == "Несущая арматура" or element.Category.Name == "Окна" or element.Category.Name == "Соединения несущих конструкций":
		level_paramater = element.get_Parameter(BuiltInParameter.FAMILY_LEVEL_PARAM)
	if element.Category.Name == "Несущие колонны":
		level_paramater = element.get_Parameter(BuiltInParameter.FAMILY_BASE_LEVEL_PARAM)
		if level_paramater == None:
			level_paramater = element.get_Parameter(BuiltInParameter.FAMILY_LEVEL_PARAM)
	if element.Category.Name == "Перекрытия":
		level_paramater = element.get_Parameter(BuiltInParameter.LEVEL_PARAM)
	if element.Category.Name == "Фундамент несущей конструкции":
		level_paramater = element.get_Parameter(BuiltInParameter.LEVEL_PARAM)
		if level_paramater == None:
			level_paramater = element.get_Parameter(BuiltInParameter.FAMILY_LEVEL_PARAM)
	if element.Category.Name == "Стены":
		level_paramater = element.get_Parameter(BuiltInParameter.WALL_BASE_CONSTRAINT)
	if element.Category.Name == "Лестницы":
		level_paramater = element.get_Parameter(BuiltInParameter.STAIRS_BASE_LEVEL_PARAM)
	if element.Category.Name == "Группы модели":
		level_paramater = element.get_Parameter(BuiltInParameter.GROUP_LEVEL)
	return level_paramater

TransactionManager.Instance.EnsureInTransaction(doc)

count = 0
for el in elements:
	if el.GroupId == ElementId(-1):
		if (el.GetType()).Name == "FamilyInstance":
			if el.SuperComponent == None:
				lev_el = get_level_parameter(el).Set(ref_level.Id)
				count += 1
		else:
			lev_el = get_level_parameter(el).Set(ref_level.Id)
			count += 1

TransactionManager.Instance.TransactionTaskDone()

out = str(count) + " элементов обработано"
OUT = out
