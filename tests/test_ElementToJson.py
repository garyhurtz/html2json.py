# -*- coding: UTF-8 -*- #
from unittest import TestCase
from html2json import Element


class ElementTestCase(TestCase):

    def test_tag(self):
        dut = Element(u'p')

        expect = {
            u'tag': u'p'
        }

        self.assertEqual(dut.render(), expect)

    def test_text(self):
        dut = Element(u'p', u'some text')

        expect = {
            u'tag': u'p',
            u'text': u'some text'
        }

        self.assertEqual(dut.render(), expect)

    def test_attr(self):
        dut = Element(u'p', u'some text', {u'class': u'some class'})

        expect = {
            u'tag': u'p',
            u'text': u'some text',
            u'attr': {
                u'class': u'some class'
            }
        }

        self.assertEqual(dut.render(), expect)

    def test_compound(self):
        dut = Element(u'ul', u'some text', {u'class': u'some class'})
        dut.child.append(Element(u'li', u'some text', {u'class': u'some class'}))

        expect = {
            u'tag': u'ul',
            u'text': u'some text',
            u'attr': {
                u'class': u'some class'
            },
            u'child': [
                {
                    u'tag': u'li',
                    u'text': u'some text',
                    u'attr': {
                        u'class': u'some class'
                    }
                }
            ]
        }

        self.assertEqual(dut.render(), expect)

    def test_compound2(self):
        dut = Element(u'ul', u'some text', {u'class': u'some class'})
        dut.child.append(Element(u'li', u'some text', {u'class': u'some class'}))
        dut.child.append(Element(u'li', u'some text', {u'class': u'some class'}))

        expect = {
            u'tag': u'ul',
            u'text': u'some text',
            u'attr': {
                u'class': u'some class'
            },
            u'child': [
                {
                    u'tag': u'li',
                    u'text': u'some text',
                    u'attr': {
                        u'class': u'some class'
                    }
                }, {
                    u'tag': u'li',
                    u'text': u'some text',
                    u'attr': {
                        u'class': u'some class'
                    }
                }
            ]
        }

        self.assertEqual(dut.render(), expect)
