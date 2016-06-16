# -*- coding: utf-8 -*-
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from pybars import Compiler

import glob
import os.path

try:
    get_distribution('plone.tiles')
except DistributionNotFound:
    class Tile(BrowserView):
        """Fake Tile which is only a BrowserView"""
else:
    from plone.tiles.tile import Tile


# global handlebars compiler
# TODO: Compile all templates at startup?
compiler = Compiler()


class HandlebarMixin:

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
        with open(hbs_filename) as f:
            hbs_template = unicode(f.read(), 'utf-8')
        return compiler.compile(hbs_template)

    def hbs_snippet(self):
        # reuse filename from tile definition in zcml but read file here
        # otherwise it is interpreted as XML/PT
        if not hasattr(self, 'index'):  # noqa
            return ''   # no template specified, should we raise an error?

        hbs_file = self.index.filename
        hbs_dir = os.path.dirname(hbs_file)

        hbs_template = self._get_hbs_template(hbs_file)
        # get all partials from directory, asuming they are prefixed with `_`
        partial_files = glob.glob(hbs_dir + '/_*.hbs')
        partials = {self._get_partial_key(partial_file): self._get_hbs_template(partial_file)   # noqa
                    for partial_file in partial_files}
        return hbs_template(self.get_contents(), partials=partials)


class HandlebarsBrowserView(BrowserView, HandlebarMixin):
    """ A simple browserview using hbs as templating engine"""

    def __call__(self, *args, **kwargs):
        return self.hbs_snippet()


class HandlebarsPloneView(BrowserView, HandlebarMixin):
    """ A hbs view rendered in the content slot of the main template of Plone
    """

    main_template = ViewPageTemplateFile('templates/plone_standard_template.pt')  # noqa

    def __call__(self, *args, **kwargs):
        return self.main_template(*args, **kwargs)


class HandlebarTile(Tile, HandlebarMixin):

    def __call__(self, *args, **kwargs):
        return self.hbs_snippet()

# EOF
