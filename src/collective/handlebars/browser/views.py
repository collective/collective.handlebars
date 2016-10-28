# -*- coding: utf-8 -*-
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from pybars import Compiler
from zope.i18n import translate

import os.path
import sys

try:
    get_distribution('plone.tiles')
except DistributionNotFound:   # pragma: no cover
    class Tile(BrowserView):
        """Fake Tile which is only a BrowserView"""
    class PersistentTile(BrowserView):
        """Fake persistent Tile which is only a BrowserView"""
else:    # pragma: no cover
    from plone.tiles.tile import Tile
    from plone.tiles.tile import PersistentTile


# global handlebars compiler
compiler = Compiler()
HBS_REGISTRY = {}


def package_home(gdict):
    filename = gdict["__file__"]
    return os.path.dirname(filename)


class HandlebarsMixin:

    def get_contents(self):
        """ Get CMS data and put it in a JSON format for hbs inclusion

        :return: dictonary (must not be a JSON structure!
                 The conversion is handled by the templating engine)
        """
        raise NotImplementedError

    def _get_partial_key(self, partial_filename):
        """
        :param partial_filename: full path of partial
               (/home/vagrant/templates/_slideshow.js.hbs)
        :return: key for partial inclusion (_slideshow.js)
        """
        path, filename = os.path.split(partial_filename)
        partial_name, ext = os.path.splitext(filename)
        return partial_name

    def _get_hbs_template(self, hbs_filename):
        """
        :param hbs_filename: full path of partial
               (/home/vagrant/templates/_slideshow.js.hbs)
        :return: compiled hbs template
        """
        if hbs_filename in HBS_REGISTRY:
            compiled_template = HBS_REGISTRY[hbs_filename]
        else:
            with open(hbs_filename) as f:
                hbs_template = unicode(f.read(), 'utf-8')
                compiled_template = compiler.compile(hbs_template)
                HBS_REGISTRY[hbs_filename] = compiled_template
        return compiled_template

    def get_partials(self, hbs_dir):
        """ Get partials for rendering the master hbs_template

        :param hbs_dir: directory of master template
               (/home/vagrant/templates/)
        :return: dictonary with compiled partials templates
                 ({'subitem': <template 'subitem'>})
        """
        return {}

    def get_helpers(self):
        """ Get helpers for rendering the master hbs_template

        :return: dictonary with compiled partials templates
                 ({'list': self.list_items()})
        """
        return {}

    def hbs_snippet(self, filename=None, _prefix=None):
        if filename:
            # first scenario: get snippet from filename
            path = self.get_path_from_prefix(_prefix)
            hbs_file = os.path.join(path, filename)
            if not os.path.isfile(hbs_file):
                raise ValueError('No such file', hbs_file)
        elif hasattr(self, 'index'):  # noqa
            # second scenario: get snippet from zcml
            # reuse filename from tile definition in zcml but read file here
            # otherwise it is interpreted as XML/PT
            hbs_file = self.index.filename
        else:
            raise ValueError('No template found!')

        hbs_template = self._get_hbs_template(hbs_file)
        hbs_dir = os.path.dirname(hbs_file)
        partials = self.get_partials(hbs_dir)
        helpers = self.get_helpers()

        return hbs_template(self.get_contents(),
                            helpers=helpers,
                            partials=partials)

    def get_path_from_prefix(self, _prefix):
        if isinstance(_prefix, str):
            path = _prefix
        else:
            if _prefix is None:
                _prefix = sys._getframe(2).f_globals
            path = package_home(_prefix)
        return path

    def translate(self, msgid, domain=None, mapping=None, context=None,
                  target_language=None, default=None):
        if not target_language:
            target_language = api.portal.get_current_language(context)
        return translate(msgid=msgid,
                         domain=domain,
                         mapping=mapping,
                         context=context,
                         default=default,
                         target_language=target_language)


class HandlebarsBrowserView(BrowserView, HandlebarsMixin):
    """ A simple browserview using hbs as templating engine"""

    def __call__(self, *args, **kwargs):
        return self.hbs_snippet()


class HandlebarsPloneView(BrowserView, HandlebarsMixin):
    """ A hbs view rendered in the content slot of the main template of Plone
    """

    main_template = ViewPageTemplateFile('templates/plone_standard_template.pt')  # noqa

    def __call__(self, *args, **kwargs):
        return self.main_template(*args, **kwargs)


class HandlebarsTile(Tile, HandlebarsMixin):

    def __call__(self, *args, **kwargs):
        return self.hbs_snippet()


# BBB
HandlebarTile = HandlebarsTile


class HandlebarsPersistentTile(PersistentTile, HandlebarsMixin):

    def __call__(self, *args, **kwargs):
        return self.hbs_snippet()

# EOF
