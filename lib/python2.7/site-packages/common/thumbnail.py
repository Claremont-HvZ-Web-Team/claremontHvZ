import re

from django.conf import settings

from easy_thumbnails.fields import ThumbnailerImageField

class ThumbnailedModel(object):
    def __getattr__(self, name):
        """
        Handles request to FOO_thumbnail and FOO_thumbnail_TYPE fields.
        """
        match = re.search(r'^(\w+)_thumbnail$', name)

        if match:
            field_name = match.group(1)
            size_name = 'normal'
        else:
            match = re.search(r'^(\w+)_thumbnail_(\w+)$', name)
            if match:
                field_name = match.group(1)
                size_name = match.group(2)
            else:
                raise AttributeError('Attribute %s does not exists' % name)

        size_key = ('%s_%s_%s_thumbnail_size' % (
            self._meta.app_label, self._meta.object_name, size_name)).upper()
        size = getattr(settings, size_key)
        try:
            return getattr(self, field_name).get_thumbnail({'size': size, 'crop': 'center'})
        except IOError:
            return None
