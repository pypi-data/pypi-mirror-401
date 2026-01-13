from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget.referencewidget_handler import IReferenceBrowserWidgetSchema
from ftw.referencewidget.referencewidget_handler import ReferenceBrowserWidgetExportImportHandler
from ftw.referencewidget.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from lxml import etree
from plone.autoform.interfaces import IWidgetExportImportHandler
from zope.component import queryUtility
import unittest
import zope.schema
import transaction


class TestReferenceBrowserWidgetSchema(unittest.TestCase):
    """Tests for the IReferenceBrowserWidgetSchema interface."""

    def test_schema_has_all_widget_attributes(self):
        """Verify that the schema defines all configurable widget attributes."""
        fields = zope.schema.getFields(IReferenceBrowserWidgetSchema)
        expected_fields = [
            'block_traversal',
            'allow_traversal',
            'selectable',
            'nonselectable',
            'start',
            'override',
            'allow_nonsearched_types',
            'explicit_type_filter',
        ]
        for field_name in expected_fields:
            self.assertIn(field_name, fields)

    def test_list_fields_have_textline_value_type(self):
        """Verify that list fields use TextLine as value type."""
        fields = zope.schema.getFields(IReferenceBrowserWidgetSchema)
        list_field_names = [
            'block_traversal',
            'allow_traversal',
            'selectable',
            'nonselectable',
            'explicit_type_filter',
        ]
        for field_name in list_field_names:
            field = fields[field_name]
            self.assertIsInstance(field, zope.schema.List)
            self.assertIsInstance(field.value_type, zope.schema.TextLine)

    def test_start_field_is_textline(self):
        """Verify that start field is a TextLine."""
        fields = zope.schema.getFields(IReferenceBrowserWidgetSchema)
        self.assertIsInstance(fields['start'], zope.schema.TextLine)

    def test_boolean_fields(self):
        """Verify that boolean fields are defined correctly."""
        fields = zope.schema.getFields(IReferenceBrowserWidgetSchema)
        self.assertIsInstance(fields['override'], zope.schema.Bool)
        self.assertIsInstance(fields['allow_nonsearched_types'], zope.schema.Bool)


class TestReferenceBrowserWidgetHandlerRead(unittest.TestCase):
    """Tests for reading widget parameters from XML (unit tests)."""

    def setUp(self):
        self.handler = ReferenceBrowserWidgetExportImportHandler()

    def test_handler_has_field_attributes(self):
        """Verify that handler has field attributes from schema."""
        self.assertIn('selectable', self.handler.fieldAttributes)
        self.assertIn('start', self.handler.fieldAttributes)
        self.assertIn('override', self.handler.fieldAttributes)

    def test_read_list_attribute(self):
        """Test reading a list attribute from XML."""
        xml = """
        <widget type="ftw.referencewidget.widget.ReferenceBrowserWidget">
            <selectable>
                <element>Document</element>
                <element>News Item</element>
            </selectable>
        </widget>
        """
        widget_node = etree.fromstring(xml)
        params = {}

        self.handler.read(widget_node, params)

        self.assertEqual(['Document', 'News Item'], params.get('selectable'))

    def test_read_textline_attribute(self):
        """Test reading a text attribute from XML."""
        xml = """
        <widget type="ftw.referencewidget.widget.ReferenceBrowserWidget">
            <start>navroot</start>
        </widget>
        """
        widget_node = etree.fromstring(xml)
        params = {}

        self.handler.read(widget_node, params)

        self.assertEqual('navroot', params.get('start'))

    def test_read_boolean_attribute(self):
        """Test reading a boolean attribute from XML."""
        xml = """
        <widget type="ftw.referencewidget.widget.ReferenceBrowserWidget">
            <override>true</override>
        </widget>
        """
        widget_node = etree.fromstring(xml)
        params = {}

        self.handler.read(widget_node, params)

        self.assertTrue(params.get('override'))

    def test_read_multiple_attributes(self):
        """Test reading multiple attributes from XML."""
        xml = """
        <widget type="ftw.referencewidget.widget.ReferenceBrowserWidget">
            <selectable>
                <element>Image</element>
            </selectable>
            <start>parent</start>
            <override>true</override>
            <allow_nonsearched_types>false</allow_nonsearched_types>
        </widget>
        """
        widget_node = etree.fromstring(xml)
        params = {}

        self.handler.read(widget_node, params)

        self.assertEqual(['Image'], params.get('selectable'))
        self.assertEqual('parent', params.get('start'))
        self.assertTrue(params.get('override'))
        self.assertFalse(params.get('allow_nonsearched_types'))


class TestReferenceBrowserWidgetHandlerWrite(FunctionalTestCase):
    """Tests for writing widget parameters to XML (requires adapters)."""

    def setUp(self):
        super().setUp()
        self.handler = ReferenceBrowserWidgetExportImportHandler()

    def test_write_list_attribute(self):
        """Test writing a list attribute to XML."""
        widget_node = etree.Element('widget')
        params = {'selectable': ['Document', 'News Item']}

        self.handler.write(widget_node, params)

        selectable_node = widget_node.find('selectable')
        self.assertIsNotNone(selectable_node)
        elements = selectable_node.findall('element')
        self.assertEqual(2, len(elements))
        self.assertEqual('Document', elements[0].text)
        self.assertEqual('News Item', elements[1].text)

    def test_write_textline_attribute(self):
        """Test writing a text attribute to XML."""
        widget_node = etree.Element('widget')
        params = {'start': 'navroot'}

        self.handler.write(widget_node, params)

        start_node = widget_node.find('start')
        self.assertIsNotNone(start_node)
        self.assertEqual('navroot', start_node.text)

    def test_write_boolean_attribute(self):
        """Test writing a boolean attribute to XML."""
        widget_node = etree.Element('widget')
        params = {'override': True}

        self.handler.write(widget_node, params)

        override_node = widget_node.find('override')
        self.assertIsNotNone(override_node)
        self.assertEqual('True', override_node.text)

    def test_write_skips_default_values(self):
        """Test that default values are not written to XML."""
        widget_node = etree.Element('widget')
        params = {
            'selectable': [],
            'start': '',
            'override': False,
        }

        self.handler.write(widget_node, params)

        self.assertEqual(0, len(widget_node))

    def test_write_only_non_default_values(self):
        """Test that only non-default values are written to XML."""
        widget_node = etree.Element('widget')
        params = {
            'selectable': ['Image'],
            'start': '',
            'override': False,
        }

        self.handler.write(widget_node, params)

        self.assertEqual(1, len(widget_node))
        selectable_node = widget_node.find('selectable')
        self.assertIsNotNone(selectable_node)

    def test_roundtrip_list_attribute(self):
        """Test roundtrip read/write for list attributes."""
        original_params = {'selectable': ['Document', 'News Item', 'Event']}
        widget_node = etree.Element('widget')

        self.handler.write(widget_node, original_params)

        read_params = {}
        self.handler.read(widget_node, read_params)

        self.assertEqual(original_params['selectable'], read_params['selectable'])

    def test_roundtrip_complex_configuration(self):
        """Test roundtrip for complex widget configuration."""
        original_params = {
            'selectable': ['Image', 'File'],
            'nonselectable': ['Folder'],
            'start': 'navroot',
            'override': True,
            'allow_nonsearched_types': True,
            'block_traversal': ['File'],
            'allow_traversal': ['Folder'],
            'explicit_type_filter': ['Image'],
        }
        widget_node = etree.Element('widget')

        self.handler.write(widget_node, original_params)

        read_params = {}
        self.handler.read(widget_node, read_params)

        for key, value in original_params.items():
            self.assertEqual(value, read_params.get(key), f'Mismatch for {key}')


class TestHandlerRegistration(FunctionalTestCase):
    """Tests for the handler ZCML registration."""

    def test_handler_is_registered_as_utility(self):
        """Test that the handler is registered as a named utility."""
        handler = queryUtility(
            IWidgetExportImportHandler,
            name='ftw.referencewidget.widget.ReferenceBrowserWidget'
        )
        self.assertIsNotNone(handler)

    def test_registered_handler_is_correct_type(self):
        """Test that the registered handler is the correct type."""
        handler = queryUtility(
            IWidgetExportImportHandler,
            name='ftw.referencewidget.widget.ReferenceBrowserWidget'
        )
        self.assertIsInstance(handler, ReferenceBrowserWidgetExportImportHandler)


WIDGET_PARAMS_MODEL_SOURCE = """
<model xmlns:i18n="http://xml.zope.org/namespaces/i18n"
       xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
       xmlns:indexer="http://namespaces.plone.org/supermodel/indexer"
       xmlns:form="http://namespaces.plone.org/supermodel/form"
       xmlns:security="http://namespaces.plone.org/supermodel/security"
       xmlns:users="http://namespaces.plone.org/supermodel/users"
       xmlns:lingua="http://namespaces.plone.org/supermodel/lingua"
       xmlns="http://namespaces.plone.org/supermodel/schema">
<schema>
    <field name="single_image_ref" type="z3c.relationfield.schema.RelationChoice">
      <description>An image reference with widget params</description>
      <required>False</required>
      <title>Image Reference</title>
      <form:widget type="ftw.referencewidget.widget.ReferenceBrowserWidget">
        <selectable>
          <element>Image</element>
        </selectable>
        <start>navroot</start>
        <override>True</override>
      </form:widget>
    </field>
    <field name="multi_image_ref" type="z3c.relationfield.schema.RelationChoice">
      <description>An image reference with widget params</description>
      <required>False</required>
      <title>Image Reference</title>
      <form:widget type="ftw.referencewidget.widget.ReferenceBrowserWidget">
        <selectable>
          <element>Image</element>
        </selectable>
        <start>navroot</start>
        <override>True</override>
      </form:widget>
    </field>
</schema>
</model>
"""


class TestWidgetParametersFromSchema(FunctionalTestCase):
    """Integration tests for widget parameters parsed from XML schema."""

    def setUp(self):
        super().setUp()
        self.setup_fti()
        self.grant('Manager')
        self.fti = self.portal.portal_types.get('SampleContent')
        self.original_model_source = self.fti.model_source
        self.fti.model_source = WIDGET_PARAMS_MODEL_SOURCE
        self.fti.lookupModel()

    def tearDown(self):
        super().tearDown()
        self.fti.model_source = self.original_model_source
        self.fti.lookupModel()

    def test_widget_parameters_are_parsed_from_xml(self):
        """Test that widget parameters are correctly parsed from XML schema."""
        from plone.autoform.interfaces import WIDGETS_KEY
        from plone.autoform.widgets import ParameterizedWidget

        schema = self.fti.lookupSchema()
        widgets = schema.queryTaggedValue(WIDGETS_KEY, {})

        self.assertIn('single_image_ref', widgets)
        widget = widgets['single_image_ref']
        self.assertIsInstance(widget, ParameterizedWidget)
        self.assertEqual(['Image'], widget.params.get('selectable'))
        self.assertEqual('navroot', widget.params.get('start'))
        self.assertTrue(widget.params.get('override'))

    @browsing
    def test_single_image_reference_widget_renders_selectable_types_as_image_only(self, browser):
        page = create(Builder('refwidget sample content').titled('Document'))
        transaction.commit()

        browser.login().visit(page, view='@@edit')

        widget = browser.css(
            '#formfield-form-widgets-single_image_ref .reference-widget-app'
        ).first
        selectable_types = widget.attrib.get('data-selectabletypes')

        self.assertIsNotNone(selectable_types)
        self.assertEqual('["Image"]', selectable_types)

    @browsing
    def test_multiple_image_reference_widget_renders_selectable_types_as_image_only(self, browser):
        page = create(Builder('refwidget sample content').titled('Document'))
        transaction.commit()

        browser.login().visit(page, view='@@edit')

        widget = browser.css(
            '#formfield-form-widgets-multi_image_ref .reference-widget-app'
        ).first
        selectable_types = widget.attrib.get('data-selectabletypes')

        self.assertIsNotNone(selectable_types)
        self.assertEqual('["Image"]', selectable_types)
