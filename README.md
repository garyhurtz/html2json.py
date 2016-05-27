# html2json.py

Tools for building HTML and parsing HTML into JSON in Python, and rendering HTML from JSON using [Jinja](https://github.com/pallets/jinja).

The JSON data structure follows that used in [html2json.js and json2html.js](https://github.com/Jxck/html2json), so that the resulting JSON can (for example) be constructed and/or stored on a Python server, passed to the browser via an AJAX call, then rendered using javascript.

The json2html.html Jinja macro is also compatible with [nunjucks](https://mozilla.github.io/nunjucks/), so both server-side and client-side templating are supported. Client-side rendering can also be performed in pure javascript using [json2html.js](https://github.com/Jxck/html2json)).

The code is pretty straight-forward, and can be easily modified to support alternative JSON data structures from other libraries.

## Building HTML

The Element class can be used to build up a data structure that represents an HTML document. Simply instantiate an Element, passing it the tag, text, and any attributes:

    dut = Element(u'p')
    
which can be rendered to JSON:

    dut.render() --> {u'tag': u'p'}

You can add text:

    dut = Element(u'p', u'some text')
    
    dut.render() --> {
            u'tag': u'p', u'text': u'some text'
        }
    
As well as any attributes, such as a class:

    dut = Element(u'p', u'some text', {u'class': u'some class'})
    
    dut.render() --> {
            u'tag': u'p', u'text': u'some text', u'attr': {u'class': u'some class'}
        }

You can also build HTML documents by instantiating and appending child Elements:

    dut = Element(u'ul', u'some text', {u'class': u'some class'})
    dut.child.append(Element(u'li', u'some text', {u'class': u'some class'}))
    
    dut.render() --> {
            u'tag': u'ul', u'text': u'some text', u'attr': {u'class': u'some class'},
            u'child': [
                    {u'tag': u'li', u'text': u'some text', u'attr': {u'class': u'some class'}}
                ]
        }

## Parsing HTML

In addition to allowing you to build up a doucment, the Element also features a *parse(html)* method, which makes it very easy to parse HTML documents into a tree of Elements, which can then be rendered to JSON:

    with open(u'document.html', u'r') as infile:
        html = infile.read()

    dut = Element.parse(html)
    
Assuming the HTML document contains:
    
    <h1>title</h1>

    <p>content</p>

    <figure>
        <img src="cover.jpg">
    </figure>
    
You can then render JSON

    dut.render() --> {
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

Astute readers will notice that there is an extra \<div\> tag in the output. Whats up with that?

If the incoming HTML contains a single root element, the document will be parsed and rendered directly to JSON. If the incoming HTML contains multiple elements at the root level, as in the preceding example, a root element will be instantiated and the HTML will be parsed into children of that element. By default the root element is a \<div\>, although this can be overridden by passing the desired tag to the *parse* method:
 
    dut = Element.parse(html, parent=u'article')
  
If you really wanted the JSON for the file you can easily recover it by accessing the root element's *child* attribute:

    original_elements = dut.get(u'child')
    
which will return a list of parsed elements.

## Rendering HTML

After HTML is parsed into JSON, it can be rendered back to HTML using the Jinja/nunjucks macro contained in the json2html.html template. Simply import this macro, pass the JSON into the context, and watch the HTML magically appear.

You can learn pretty much everything about [Jinja](https://github.com/pallets/jinja) and [nunjucks](https://mozilla.github.io/nunjucks/) on their websites, but in short you set up an environment, tell it which template you want to use, then render the HTML.

Build the HTML:

    dut = Element(u'ul', u'some text', {u'class': u'some class'})
    dut.child.append(Element(u'li', u'some text', {u'class': u'some class'}))
    dut.child.append(Element(u'li', u'some text', {u'class': u'some class'}))

Render the JSON:

    json = dut.render()

Then reconstruct the HTML. With Jinja it looks something like this, and nunjucks is very similar:

    env = Environment(loader=FileSystemLoader(u'template_path'))
    result = env.get_template(u'json2html.html').render(root=json)

Which provides the following HTML:

    <ul class="some class">some text<li class="some class">some text</li><li class="some class">some text</li></ul>

Alternatively, [json2html.js](https://github.com/Jxck/html2json) supports pure javascript rendering of HTML from the JSON:

    html = json2html(json)

