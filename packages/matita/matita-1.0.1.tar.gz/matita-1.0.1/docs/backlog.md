---
title: Backlog
---

## Open items

### item-02 Parse *data type* of parameters

The column `data type` of the parameters table is not yet parsed.
E.g. from [Sequence.AddEffect method (PowerPoint)](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.sequence.addeffect).

|Name|Required/Optional|Data type|Description|
|:-----|:-----|:-----|:-----|
| _Shape_|Required|**[Shape](PowerPoint.Shape.md)**|The shape to which the animation effect is added.|
| _effectId_|Required|**[MsoAnimEffect](PowerPoint.MsoAnimEffect.md)**|The animation effect to be applied.|
| _Level_|Optional|**[MsoAnimateByLevel](PowerPoint.MsoAnimateByLevel.md)**|For charts, diagrams, or text, the level to which the animation effect will be applied. The default value is **msoAnimationLevelNone**.|
| _trigger_|Optional|**[MsoAnimTriggerType](PowerPoint.MsoAnimTriggerType.md)**|The action that triggers the animation effect. The default value is **msoAnimTriggerOnPageClick**.|
| _Index_|Optional|**Long**|The position at which the effect will be placed in the collection of animation effects. The default value is -1 (added to the end). |

The parsed information can be used to improve the type hints in the generated code.
E.g. the method signature of `AddEffect` can be improved from

```python
   def AddEffect(self, Shape=None, effectId=None, Level=None, trigger=None, Index=None):
```
to

```python
   def AddEffect(self, Shape: Shape = None, effectId: int = None, Level: int = None, trigger: int = None, Index: int = None)
```

Enums are defined as `int`.

**Attention** Some functions accept different type of arguments.
E.g. [`Worksheet.Range`](https://learn.microsoft.com/en-gb/office/vba/api/excel.worksheet.range) can take a `str` and an `Excel.Range` as first argument.

### item-03 Parse *default value* of parameters

Follow-up to item-02.
More complex, because the default value is embedded in the description text.

### item-04 `matita.office` Classes to `None` if defining com_object is `None`

There are operations which return `None` (`null` or `nothing` in VBA).
To be more intuitive, the class instance should be set to `None` directly if the initiation COM object is already `None`.

```python
cell1 = wks.cells(1,1)
cell2 = wks.cells(2,2)
rng = xl_app.intersect(cell1, cell2)

print(rng.com_object is None) # True
print(rng is None) # False, should be True instead
```

### item-05 Define `__len__` method for collection

E.g.:
```python
num_worksheets = wkb.worksheets.count
num_worksheets = len(wkb.worksheets)
```

### item-06 Add support for `Worksheet.Rows(index)` ans `Worksheet.Columns(index)`

```
# Works now
wks.rows.item(2).style = "Heading 1"

# Not supported
wks.rows(2).style = "Heading 1"
```


### item-08 Smart return type for `Outlook.Application.CreateItem`

[`Outlook.Application.CreateItem`](https://learn.microsoft.com/en-gb/office/vba/api/outlook.application.createitem) can return different types depending on the given argument.

Now it returns die COM object directly.
It could return directly the COM object wrapped in the correct class.

```python
# Now
# return instance must be wrapped in `MailItem` class
mail = ol.MailItem(ol_app.create_item(ol.olMailItem))

# After
# return `matita.outlook.MailItem` instance directly
mail = ol_app.create_item(ol.olMailItem) 
```

### item-09 Infer return type object

*Return value* is often just *object* in the documentation.
It can usually be inferred from context.
E.g. *Chart.SeriesCollection* returns a *SeriesCollection*.
https://learn.microsoft.com/en-gb/office/vba/api/excel.chart.seriescollection

Fix by updating the documentation or inferring the class.

### item-10 bug `Excel.FullSeriesCollection.Count` returns a `Excel.Series` instead of a `int`

Something is wrong in the parsing and/or processing.
```
    "excel.fullseriescollection.count": {
        "title": "FullSeriesCollection.Count property (Excel)",
        ...
        "property_class": "Series",
        ...
    },
```

## item-11 Fix invalid collection return class types

E.g. There is no class `Excel.Area`. Is `Range.Areas` a collection of Ranges?

Could be fixed by updating the documentation.
If the return class of the `Item` method of a collection is defined, it should be prioritised over the class inferred by the name.

```
class Areas:

    def __init__(self, areas=None):
        self.com_object= areas

    def __call__(self, item):
        return Area(self.com_object(item))
```

## Done v1.0.1

### item-07 bug `Excel.Chart.FullSeriesCollection(i)` returns a `FullSeriesCollection` instead of `Series`

`Excel.Chart.FullSeriesCollection` is not a collection, despite the name.
It is a set of the collection `Excel.Chart.Series`.
When a class method (like `Excel.Chart.FullSeriesCollection`) has a class with itself an `item` method (like `Excel.Item`), then `return_value_class` of the class method should be set to the same as the `item` method.

## Done v1.0.0

### item-01 Add snake case aliases for all methods and properties

VBA properties and methods are written in [CamelCase](https://developer.mozilla.org/en-US/docs/Glossary/Camel_case).
In Python, the [PEP8](https://peps.python.org/pep-0008/#function-and-variable-names) naming convention is [snake_case](https://developer.mozilla.org/en-US/docs/Glossary/Snake_case).

> Function names should be lowercase, with words separated by underscores as necessary to improve readability.

Add snake_case aliases for all methods and properties to improve intuitiveness for Python developers.

```python
from matita.office import excel
wks = excel.Application().workbooks.open("file.xlsx").worksheets(1)

# Supported
wks.AutoFilter
wks.autofilter()

# New
wks.auto_filter
```
