# -*- coding: UTF-8 -*- #
from unittest import TestCase
from html2json import Element
import os
from jinja2 import Environment, FileSystemLoader


class RenderTestCase(TestCase):

    templates_path = os.path.join(os.path.dirname(os.getcwd()), u'templates')

    def setUp(self):
        self.env = Environment(loader=FileSystemLoader(self.templates_path))

    def test_simple_list(self):
        dut = Element(u'ul', u'text', {u'class': u'some class'})
        dut.child.append(Element(u'li', u'text', {u'class': u'some class'}))
        dut.child.append(Element(u'li', u'text', {u'class': u'some class'}))

        result = self.env.get_template(u'json2html.html').render(root=dut.render())

        expect = u'<ul class="some class">text<li class="some class">text</li><li class="some class">text</li></ul>'

        self.assertEqual(result, expect)

    def test_property(self):
        dut = Element(u'ul', u'text', {u'class': u'some class'})
        dut.child.append(Element(u'li', u'text', {u'disable': None}))
        dut.child.append(Element(u'li', u'text', {u'disable': u''}))

        result = self.env.get_template(u'json2html.html').render(root=dut.render())

        expect = u'<ul class="some class">text<li disable>text</li><li disable>text</li></ul>'

        self.assertEqual(result, expect)
