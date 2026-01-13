"""Export/Import handler for ftw.referencewidget's ReferenceBrowserWidget.

This module provides the IWidgetExportImportHandler implementation that enables
serialization of ReferenceBrowserWidget parameters to/from plone.supermodel XML.

This allows configuring the reference widget directly in XML schema definitions:

    <field name="related_items" type="z3c.relationfield.schema.RelationList">
      <title>Related Items</title>
      <form:widget type="ftw.referencewidget.widget.ReferenceBrowserWidget">
        <selectable>
          <element>Document</element>
          <element>News Item</element>
        </selectable>
        <start>parent</start>
        <override>true</override>
      </form:widget>
    </field>
"""

from plone.autoform.interfaces import IWidgetExportImportHandler
from plone.supermodel.utils import elementToValue
from plone.supermodel.utils import noNS
from plone.supermodel.utils import valueToElement
from zope.interface import implementer
from zope.interface import Interface

import zope.schema


class IReferenceBrowserWidgetSchema(Interface):
    """Schema interface defining configurable attributes of ReferenceBrowserWidget.

    This interface describes all the parameters that can be configured via XML
    supermodel definitions for the ftw.referencewidget ReferenceBrowserWidget.

    Attributes:
        block_traversal: List of portal types to block traversal into.
            When browsing the content tree, these types will not be expandable.
        allow_traversal: List of portal types to explicitly allow traversal into.
            Overrides default traversal behavior for these types.
        selectable: List of portal types that can be selected as references.
            Only items of these types will be selectable in the widget.
        nonselectable: List of portal types that cannot be selected.
            These types will be visible but not selectable.
        start: TALES expression or path defining the starting location for browsing.
            Examples: 'parent', 'navroot', '/path/to/folder'
        override: When True, the selectable/nonselectable settings override
            global configuration rather than extending it.
        allow_nonsearched_types: When True, allows selecting types that are
            not normally searchable.
        explicit_type_filter: List of portal types for explicit filtering.
            Limits the displayed items to only these types.
    """

    block_traversal = zope.schema.List(
        title="Block Traversal",
        description="Portal types to block traversal into when browsing.",
        value_type=zope.schema.TextLine(),
        required=False,
        default=[],
    )

    allow_traversal = zope.schema.List(
        title="Allow Traversal",
        description="Portal types to explicitly allow traversal into.",
        value_type=zope.schema.TextLine(),
        required=False,
        default=[],
    )

    selectable = zope.schema.List(
        title="Selectable Types",
        description="Portal types that can be selected as references.",
        value_type=zope.schema.TextLine(),
        required=False,
        default=[],
    )

    nonselectable = zope.schema.List(
        title="Non-Selectable Types",
        description="Portal types that cannot be selected.",
        value_type=zope.schema.TextLine(),
        required=False,
        default=[],
    )

    start = zope.schema.TextLine(
        title="Start Path",
        description="TALES expression or path for the starting browse location.",
        required=False,
        default="",
    )

    override = zope.schema.Bool(
        title="Override",
        description="Override global configuration instead of extending it.",
        required=False,
        default=False,
    )

    allow_nonsearched_types = zope.schema.Bool(
        title="Allow Non-Searched Types",
        description="Allow selecting types that are not normally searchable.",
        required=False,
        default=False,
    )

    explicit_type_filter = zope.schema.List(
        title="Explicit Type Filter",
        description="Limit displayed items to only these portal types.",
        value_type=zope.schema.TextLine(),
        required=False,
        default=[],
    )


@implementer(IWidgetExportImportHandler)
class ReferenceBrowserWidgetExportImportHandler:
    """Handler for importing/exporting ReferenceBrowserWidget parameters to XML.

    This handler enables the serialization of ftw.referencewidget's
    ReferenceBrowserWidget configuration to/from plone.supermodel XML format.

    The handler uses IReferenceBrowserWidgetSchema to define which attributes
    can be configured and their types for proper serialization.

    Attributes:
        fieldAttributes: Dictionary mapping attribute names to their schema fields.
            Used for reading and writing XML elements.

    Example XML configuration:
        <form:widget type="ftw.referencewidget.widget.ReferenceBrowserWidget">
          <selectable>
            <element>Image</element>
            <element>File</element>
          </selectable>
          <start>navroot</start>
          <override>true</override>
        </form:widget>
    """

    def __init__(self):
        """Initialize the handler with field attributes from the widget schema."""
        self.fieldAttributes = zope.schema.getFields(IReferenceBrowserWidgetSchema)

    def read(self, widgetNode, params):
        """Parse widget parameters from XML element children.

        Reads child elements of the widget node and converts them to Python
        values using the schema field definitions. Each child element's tag
        name should match an attribute name in IReferenceBrowserWidgetSchema.

        Args:
            widgetNode: lxml Element containing the widget configuration.
                Expected to have child elements named after widget attributes.
            params: Dictionary to populate with parsed parameter values.
                Keys are attribute names, values are the parsed Python objects.
        """
        for attributeName, attributeField in self.fieldAttributes.items():
            for node in widgetNode.iterchildren():
                if noNS(node.tag) == attributeName:
                    params[attributeName] = elementToValue(attributeField, node)

    def write(self, widgetNode, params):
        """Serialize widget parameters to XML element children.

        Writes parameter values as child elements of the widget node. Only
        parameters that differ from their default values are written.

        Args:
            widgetNode: lxml Element to append child elements to.
                Child elements will be created for each non-default parameter.
            params: Dictionary of parameter values to serialize.
                Keys are attribute names, values are Python objects to convert.
        """
        for attributeName, attributeField in self.fieldAttributes.items():
            elementName = attributeField.__name__
            value = params.get(elementName, attributeField.default)
            if value != attributeField.default:
                child = valueToElement(attributeField, value, name=elementName)
                widgetNode.append(child)


ReferenceBrowserWidgetHandler = ReferenceBrowserWidgetExportImportHandler()
