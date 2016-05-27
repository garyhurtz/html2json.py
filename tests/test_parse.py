# -*- coding: UTF-8 -*- #
from unittest import TestCase
from html2json import Element
import os

cwd = os.path.dirname(os.path.realpath(__file__))


class ElementTestCase(TestCase):

    def test_cover(self):

        with open(os.path.join(cwd, u'cover.html'), u'r') as infile:
            html = infile.read()

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'div')
        self.assertEqual(dut.child[0].tag, u'h1')
        self.assertEqual(dut.child[0].text, u'title')
        self.assertEqual(dut.child[1].tag, u'p')
        self.assertEqual(dut.child[1].text, u'content')
        self.assertEqual(dut.child[2].tag, u'figure')
        self.assertEqual(dut.child[2].child[0].tag, u'img')
        self.assertEqual(dut.child[2].child[0].attr[u'src'], u'cover.jpg')

        json = {
            u'tag': u'div',
            u'child': [
                {
                    u'tag': u'h1',
                    u'text': u'title',
                },
                {
                    u'tag': u'p',
                    u'text': u'content',
                },
                {
                    u'tag': u'figure',
                    u'child': [
                        {
                            u'tag': u'img',
                            u'attr': {
                                u'src': u'cover.jpg'
                            }
                        }
                    ]
                }
            ]
        }

        self.assertEqual(dut.render(), json)

    def test_div_tag(self):
        html = u'<div></div>'
        json = {u'tag': u'div'}

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'div')
        self.assertEqual(dut.render(), json)

    def test_div_with_text(self):
        html = u'<div>this is a div</div>'
        json = {
            u'tag': u'div',
            u'text': u'this is a div'
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'div')
        self.assertEqual(dut.text, u'this is a div')

        self.assertEqual(dut.render(), json)

    def test_text_gets_stripped(self):
        html = u'<div>this is a div   </div>'
        json = {
            u'tag': u'div',
            u'text': u'this is a div'
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'div')
        self.assertEqual(dut.text, u'this is a div')

        self.assertEqual(dut.render(), json)

    def test_div_with_id(self):
        html = u'<div id="foo"></div>'
        json = {
            u'tag': u'div',
            u'attr': {u'id': u'foo'}}

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'div')
        self.assertEqual(dut.attr[u'id'], u'foo')

        self.assertEqual(dut.render(), json)

    def test_div_with_id_and_class(self):
        html = u'<div id="foo" class="bar goo"></div>'
        json = {
            u'tag': u'div',
            u'attr': {
                u'id': u'foo',
                u'class': [u'bar', u'goo']
            }
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'div')
        self.assertEqual(dut.attr[u'id'], u'foo')
        self.assertEqual(dut.attr[u'class'], [u'bar', u'goo'])

        self.assertEqual(dut.render(), json)

    def test_div_with_id_and_class_and_text(self):
        html = u'<div id="foo" class="bar goo">this is a div</div>'
        json = {
            u'tag': u'div',
            u'attr': {
                u'id': u'foo',
                u'class': [u'bar', u'goo']
            },
            u'text': u'this is a div'
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'div')
        self.assertEqual(dut.text, u'this is a div')
        self.assertEqual(dut.attr[u'id'], u'foo')
        self.assertEqual(dut.attr[u'class'], [u'bar', u'goo'])

        self.assertEqual(dut.render(), json)

    def test_div_with_child(self):
        html = u'<div><p></p></div>'
        json = {
            u'tag': u'div',
            u'child': [{
                u'tag': u'p'
            }]
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'div')
        self.assertEqual(dut.child[0].tag, u'p')

        self.assertEqual(dut.render(), json)

    def test_ul(self):
        html = u'<ul><li></li><li></li></ul>'
        json = {
            u'tag': u'ul',
            u'child': [
                {
                    u'tag': u'li'
                }, {
                    u'tag': u'li'
                }
            ]
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'ul')
        self.assertEqual(dut.child[0].tag, u'li')
        self.assertEqual(dut.child[1].tag, u'li')

        self.assertEqual(dut.render(), json)

    def test_figure(self):
        html = u'<figure><img src="abc"></figure>'
        json = {
            u'tag': u'figure',
            u'child': [
                {
                    u'tag': u'img',
                    u'attr': {
                        u'src': u'abc'
                    }
                }
            ]
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'figure')
        self.assertEqual(dut.child[0].tag, u'img')

        self.assertEqual(dut.render(), json)

    def test_figure_with_newlines(self):
        html = u'<figure>\n<img src="abc">\n</figure>'
        json = {
            u'tag': u'figure',
            u'child': [
                {
                    u'tag': u'img',
                    u'attr': {
                        u'src': u'abc'
                    }
                }
            ]
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'figure')
        self.assertEqual(dut.child[0].tag, u'img')

        self.assertEqual(dut.render(), json)

    def test_figure_with_newlines_and_spaces(self):
        html = u'<figure>\n      <img src="abc">   \n</figure>'
        json = {
            u'tag': u'figure',
            u'child': [
                {
                    u'tag': u'img',
                    u'attr': {
                        u'src': u'abc'
                    }
                }
            ]
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'figure')
        self.assertEqual(dut.child[0].tag, u'img')

        self.assertEqual(dut.render(), json)

    def test_figure_with_caption(self):
        html = u'<figure><img src="abc"><figcaption>caption</figcaption></figure>'
        json = {
            u'tag': u'figure',
            u'child': [
                {
                    u'tag': u'img',
                    u'attr': {
                        u'src': u'abc'
                    }
                }, {
                    u'tag': u'figcaption',
                    u'text': u'caption'
                }
            ]
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'figure')
        self.assertEqual(dut.child[0].tag, u'img')
        self.assertEqual(dut.child[1].tag, u'figcaption')

        self.assertEqual(dut.render(), json)

    def test_div_with_two_child(self):
        html = u'<div><p></p><p></p></div>'
        json = {
            u'tag': u'div',
            u'child': [{
                u'tag': u'p'
            }, {
                u'tag': u'p'
            }]
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'div')
        self.assertEqual(dut.child[0].tag, u'p')
        self.assertEqual(dut.child[1].tag, u'p')

        self.assertEqual(dut.render(), json)

    def test_div_with_nested_child(self):
        html = u'<div><p><textarea></textarea></p></div>'
        json = {
            u'tag': u'div',
            u'child': [{
                u'tag': u'p',
                u'child': [{
                    u'tag': u'textarea'
                }]
            }]
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'div')
        self.assertEqual(dut.child[0].tag, u'p')
        self.assertEqual(dut.child[0].child[0].tag, u'textarea')

        self.assertEqual(dut.render(), json)

    def test_div_with_two_nested_child(self):
        html = u'<div><p><textarea></textarea></p><p></p></div>'
        json = {
            u'tag': u'div',
            u'child': [{
                u'tag': u'p',
                u'child': [{
                    u'tag': u'textarea'
                }]
            }, {
                u'tag': u'p'
            }]
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'div')
        self.assertEqual(dut.child[0].tag, u'p')
        self.assertEqual(dut.child[0].child[0].tag, u'textarea')
        self.assertEqual(dut.child[1].tag, u'p')

        self.assertEqual(dut.render(), json)

    def test_unary(self):
        html = u''.join(
            [
                u'<div id="1" class="foo bar">',
                u'<h2>sample text</h2>',
                u'<input id="execute" type="button" value="execute"/>',
                u'<img src="photo.jpg" alt="photo"/>',
                u'</div>'
            ]
        )

        json = {
            u'tag': u'div',
            u'attr': {
                u'id': u'1',

                u'class': [u'foo', u'bar']

            },
            u'child': [{
                u'tag': u'h2',
                u'text': u'sample text'
            }, {
                u'tag': u'input',
                u'attr': {
                    u'id': u'execute',
                    u'type': u'button',
                    u'value': u'execute'
                }
            }, {
                u'tag': u'img',
                u'attr': {
                    u'src': u'photo.jpg',
                    u'alt': u'photo'
                }
            }]
        }

        dut = Element.parse(html)

        self.assertEqual(dut.render(), json)

    def test_div_with_inline_tag1(self):
        html = u'<div>this is a <b>div</b></div>'
        json = {
            u'tag': u'div',
            u'text': u'this is a <b>div</b>'
        }

        dut = Element.parse(html)

        self.assertEqual(dut.tag, u'div')
        self.assertEqual(dut.text, u'this is a <b>div</b>')

        self.assertEqual(dut.render(), json)

    def test_div_with_inline_tag2(self):
        html = u'<p>sample text with tag <strong>like</strong> this</p>'
        json = {
            u'tag': u'p',
            u'text': u'sample text with tag <strong>like</strong> this'
        }

        dut = Element.parse(html)

        self.assertEqual(dut.render(), json)

    def test_div_with_inline_tag3(self):
        html = u''.join([
            u'<div id="1" class="foo bar">',
            u'<p>sample text with tag <strong>like</strong> this</p>',
            u'<p><strong>with</strong> inline tag</p>',
            u'</div>'
        ])

        json = {
            u'tag': u'div',
            u'attr': {
                u'id': u'1',
                u'class': [u'foo', u'bar']
            },
            u'child': [{
                u'tag': u'p',
                u'text': u'sample text with tag <strong>like</strong> this'
            }, {
                u'tag': u'p',
                u'text': u'<strong>with</strong> inline tag'
            }]
        }

        dut = Element.parse(html)

        # print dut.render()
        self.assertEqual(dut.render(), json)

    def test_parse_what_the_guy_wants(self):

        json = {
            u'tag': u'div',
            u'attr': {
                u'id': u'1',
                u'class': [u'foo']
            },
            u'child': [{
                u'tag': u'h2',
                u'text': u'sample text with <code>inline tag</code>'
            }, {
                u'tag': u'pre',
                u'attr': {
                    u'id': u'demo',
                    u'class': [u'foo', u'bar']
                }
            }, {
                u'tag': u'pre',
                u'attr': {
                    u'id': u'output',
                    u'class': [u'goo']
                }
            }, {
                u'tag': u'input',
                u'attr': {
                    u'id': u'execute',
                    u'type': u'button',
                    u'value': u'execute'
                }
            }]
        }

        html = u''.join([
            u'<div id="1" class="foo">',
            u'<h2>sample text with <code>inline tag</code></h2>',
            u'<pre id="demo" class="foo bar"></pre>',
            u'<pre id="output" class="goo"></pre>',
            u'<input id="execute" type="button" value="execute"/>',
            u'</div>'
        ])

        dut = Element.parse(html)
        self.assertEqual(dut.render(), json)
