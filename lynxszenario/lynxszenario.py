"""
TO-DO: Write a description of what this XBlock is.
Author : Jay Modi
"""

import json, urllib2
from .utils import render_template, load_resource, resource_string
from django.template import Context, Template
from xblock.core import XBlock
from xblock.fields import Scope, Integer, List, String, Boolean, Dict
from xblock.fragment import Fragment


class LynxSzenarioXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    display_name = String(
        display_name="LYNX Szenario Block",
        help="This name appears in the horizontal navigation at the top of the page",
        scope=Scope.settings,
        default="LYNX Szenario Block"
    )

    body_html = String(
        help="HTML code of the block",
        default="<p>Body of the Szenario goes here.</p>", scope=Scope.content
    )

    @XBlock.json_handler
    def get_body_html(self, data, suffix=''):
        return {"body_html": self.body_html}

    @staticmethod
    def generate_html(html):

        result = "<div class=\"lynxszenario_xblock\">"
        result += "<div class='lynxszenario_szenario'>"
        # Assume valid HTML code
        result += html
        result += "</div>"
        result += "</div>"

        return result

    @staticmethod
    def update_student_settings_backend(source, settings):
        """
        Returns dictionary that is source merged with settings
        """
        result = json.loads(source)
        result.update(json.loads(settings))
        return json.dumps(result)

    def student_view(self, context=None):
        """
        The student view
        """
        fragment = Fragment()
        content = {'self': self}

        body_html = unicode(self.generate_html(self.body_html))

        fragment.add_css(load_resource('static/css/lynxszenario.css'))

        fragment.add_content(Template(body_html).render(Context(content)))
        fragment.add_content(render_template('templates/lynxszenario.html', content))

        fragment.add_javascript(unicode(render_template('static/js/lynxszenario_lms.js', content)))
        fragment.initialize_js('LynxSzenarioXBlock')

        return fragment

    def studio_view(self, context=None):
        """
        The studio view
        """

        fragment = Fragment()
        content = json.loads(load_resource("static/studio_settings.json"))
        content['self'] = self

        try:
            urllib2.urlopen(content["CKEDITOR_URL"])
        except urllib2.HTTPError, e:
            content["CKEDITOR_URL"] = ""
        except urllib2.URLError, e:
            content["CKEDITOR_URL"] = ""

        # Load CodeMirror
        fragment.add_javascript(load_resource('static/js/codemirror/lib/codemirror.js'))
        fragment.add_javascript(load_resource('static/js/codemirror/mode/xml/xml.js'))
        fragment.add_javascript(load_resource('static/js/codemirror/mode/htmlmixed/htmlmixed.js'))
        fragment.add_javascript(load_resource('static/js/codemirror/mode/javascript/javascript.js'))
        fragment.add_javascript(load_resource('static/js/codemirror/mode/css/css.js'))
        fragment.add_css(load_resource('static/js/codemirror/lib/codemirror.css'))

        # Load CodeMirror add-ons
        fragment.add_css(load_resource('static/js/codemirror/theme/mdn-like.css'))
        fragment.add_javascript(load_resource('static/js/codemirror/addon/edit/matchbrackets.js'))
        fragment.add_javascript(load_resource('static/js/codemirror/addon/edit/closebrackets.js'))
        fragment.add_javascript(load_resource('static/js/codemirror/addon/search/search.js'))
        fragment.add_javascript(load_resource('static/js/codemirror/addon/search/searchcursor.js'))
        fragment.add_javascript(load_resource('static/js/codemirror/addon/dialog/dialog.js'))
        fragment.add_css(load_resource('static/js/codemirror/addon/dialog/dialog.css'))

        # Load Studio View
        fragment.add_content(render_template('templates/lynxszenario_edit.html', content))
        fragment.add_css(load_resource('static/css/lynxszenario_edit.css'))
        fragment.add_javascript(unicode(render_template('static/js/lynxszenario_edit.js', content)))
        fragment.initialize_js('LynxSzenarioXBlockStudio')

        return fragment

    @staticmethod
    def generate_preview(self, dependencies, html, json, jsa, jsb, css):

        preview = ""

        return preview

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Course author pressed the Save button in Studio
        """

        result = {"submitted": "false", "saved": "false", "message": "", "preview": ""}

        if len(data) > 0:
            # NOTE: No validation going on here; be careful with your code
            self.display_name = data["display_name"]
            self.dependencies = ""
            self.body_html = data["body_html"]

            result["submitted"] = "true"
            result["saved"] = "true"

        return result

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("LynxSzenarioXBlock",
             """<lynxszenario/>
             """),
        ]
