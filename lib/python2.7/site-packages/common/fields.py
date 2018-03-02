from django.db import models
from django.db.models.fields.related import SingleRelatedObjectDescriptor 
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.forms.widgets import Textarea
from django.utils import simplejson

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], ['^common\.fields\.JSONField'])


class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):
    def __get__(self, instance, instance_type=None):
        try:
            return super(AutoSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)
        except self.related.model.DoesNotExist:
            obj = self.related.model(**{self.related.field.name: instance})
            obj.save()
            return obj


class AutoOneToOneField(models.OneToOneField):
    """
    OneToOneField creates dependent object on first request from parent object
    if dependent oject has not created yet.

    More info (in russian): http://softwaremaniacs.org/blog/2007/03/07/auto-one-to-one-field/

    Usage example::

        # in models.py
        class Profile(models.Model):
            user = AutoOneToOneField('auth.User')
            icq = models.IntegerField()

        # in some view
        user = User.objects.create_user('batman', 'batman@gmail.com', 'Robin')
        user.profile.icq = '827873948'
        user.profile.save()
    """

    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(), AutoSingleRelatedObjectDescriptor(related))




class JSONField(models.TextField):
    """
    JSONField allows to store any data which is serialized in JSON under the hood.
    
    Usage example::

        # in models.py
        class Video(models.Model):
            thumbnails = JSONField()

        # in some view
        obj = Video()
        obj.thumbnails = ['1.jpg', '2.jpg']
        obj.save()
    """

    __metaclass__ = models.SubfieldBase

    def contribute_to_class(self, cls, name):
        super(JSONField, self).contribute_to_class(cls, name)

        def get_json(model):
            return self.get_db_prep_value(getattr(model, self.attname))
        setattr(cls, 'get_%s_json' % self.name, get_json)

        def set_json(model, json):
            setattr(model, self.attname, self.to_python(json))
        setattr(cls, 'set_%s_json' % self.name, set_json)

    def formfield(self, **kwargs):
        kwargs['widget'] = JSONWidget(attrs={'class': 'vLargeTextField'})
        return super(JSONField, self).formfield(**kwargs)

    def get_db_prep_value(self, value):
        return simplejson.dumps(value)

    def to_python(self, value):
        if not isinstance(value, basestring):
            return value

        try:
            return simplejson.loads(value, encoding=settings.DEFAULT_CHARSET)
        except ValueError, e:
            # If string could not parse as JSON it's means that it's Python
            # string saved to JSONField.
            return value

    #def south_field_triple(self):

        #from south.modelsinspector import introspector
        #field_class = 'django.db.models.TextField'
        #args, kwargs = introspector(models.TextField)
        #return (field_class, args, kwargs)


class JSONWidget(Textarea):
    """
    Prettify dumps of all non-string JSON data.
    """
    def render(self, name, value, attrs=None):
        if not isinstance(value, basestring) and value is not None:
            value = simplejson.dumps(value, indent=4, sort_keys=True)
        return super(JSONWidget, self).render(name, value, attrs)
