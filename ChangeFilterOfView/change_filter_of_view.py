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

chapter_name = IN[0]

TransactionManager.Instance.EnsureInTransaction(doc)

## Коллекторы фильтров и параметров
all_filters = FilteredElementCollector(doc).OfClass(FilterElement).ToElements()
all_parameters = FilteredElementCollector(doc).OfClass(ParameterElement).ToElements()

## Выборка необходимых параметров для настройки фильтров
try:
	for param in all_parameters:
		if "Мрк.МаркаКонструкции" == param.Name:
			mark_con_id = param.Id
		if "Арм.ВыполненаСемейством" == param.Name:
			rebar_created_id = param.Id

	mark = ParameterValueProvider(ElementId(BuiltInParameter.ALL_MODEL_MARK))
	mark_con = ParameterValueProvider(mark_con_id)
	rebar_created = ParameterValueProvider(rebar_created_id)
	rebar_host = ParameterValueProvider(ElementId(BuiltInParameter.REBAR_ELEM_HOST_MARK))
except:
	OUT = "В проекте отсутствуют один или несколько необходимых параметров для настройки фильтров"

TransactionManager.Instance.EnsureInTransaction(doc)
try:
## Выборка набора требуемых фильтров
	for filter in all_filters:
		if "Конструкции не КЖ" in filter.Name and filter.Name != "Конструкции не КЖ0.1.2":
			structure_filter = filter
		if "Арм Комплект не КЖ" in filter.Name and filter.Name != "Арм Комплект не КЖ0.1.2":
			chapter_filter = filter

## Переименование фильтров по разделам
	structure_filter.Name = structure_filter.Name[:14] + " " + chapter_name
	chapter_filter.Name = chapter_filter.Name[:15] + " " + chapter_name
	
## Настройка фильтра "Конструкции не..."
	structure_filter_markrules = FilterStringRule(mark, FilterStringContains(), "-" + chapter_name[2:] + "-", False)
	structure_filter_markrules = FilterInverseRule(structure_filter_markrules)
	structure_filter_element = ElementParameterFilter(structure_filter_markrules)
	structure_filter = structure_filter.SetElementFilter(structure_filter_element)

## Настройка фильтра "Арм Комплект не..."
# Создание правил проверок первого набора
	chapter_filter_rebarcreatedrules_set01 = FilterIntegerRule(rebar_created, FilterNumericEquals(), 0)
	chapter_filter_rebarhostrules_set01 = FilterStringRule(rebar_host, FilterStringContains(), "-" + chapter_name[2:] + "-", False)
	chapter_filter_rebarhostrules_set01 = FilterInverseRule(chapter_filter_rebarhostrules_set01)
# Создание первого набора из правил проверок
	chapter_filter_rules_set01 = []
	chapter_filter_rules_set01.Add(ElementParameterFilter(chapter_filter_rebarcreatedrules_set01))
	chapter_filter_rules_set01.Add(ElementParameterFilter(chapter_filter_rebarhostrules_set01))

	iCollect_chapter_filter_rules_set01 = List[ElementFilter](chapter_filter_rules_set01)
	chapter_filter_element_set01 = LogicalAndFilter(iCollect_chapter_filter_rules_set01)
# Создание правил проверок второго набора
	chapter_filter_rebarcreatedrules_set02 = FilterIntegerRule(rebar_created, FilterNumericEquals(), 1)
	chapter_filter_markconrules_set02 = FilterStringRule(mark_con, FilterStringContains(), "-" + chapter_name[2:] + "-", False)
	chapter_filter_markconrules_set02 = FilterInverseRule(chapter_filter_markconrules_set02)
# Создание второго набора из правил проверок
	chapter_filter_rules_set02 = []
	chapter_filter_rules_set02.Add(ElementParameterFilter(chapter_filter_rebarcreatedrules_set02))
	chapter_filter_rules_set02.Add(ElementParameterFilter(chapter_filter_markconrules_set02))

	iCollect_chapter_filter_rules_set02 = List[ElementFilter](chapter_filter_rules_set02)
	chapter_filter_element_set02 = LogicalAndFilter(iCollect_chapter_filter_rules_set02)
# Объединение первого и второго набора проверок
	chapter_filter_setsrules = []
	chapter_filter_setsrules.Add(chapter_filter_element_set01)
	chapter_filter_setsrules.Add(chapter_filter_element_set02)

	iCollect_chapter_filter_setsrules = List[ElementFilter](chapter_filter_setsrules)
	chapter_filter_element = LogicalOrFilter(iCollect_chapter_filter_setsrules)
# Назначение набора фильтрав самому фильтру
	chapter_filter = chapter_filter.SetElementFilter(chapter_filter_element)
	out = "Фильтры \"Конструкции не КЖ" + chapter_name[2:] + "\" и " + "\"Арм Комплект не КЖ\"" + chapter_name[2:] + " настроены!"
	OUT = out
except:
	OUT = "В проекте отсутствуют требуемые для настройки фильтры: \"Конструкции не <Раздел>\", \"Арм Комплект не <Раздел>\""

TransactionManager.Instance.TransactionTaskDone()
