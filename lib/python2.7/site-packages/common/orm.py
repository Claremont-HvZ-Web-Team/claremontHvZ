from collections import defaultdict

from django.contrib.contenttypes.models import ContentType

def iterate(qs, step=5000):
    """
    Reduce memory usage by splitting query into a number of queries using offset, limit
    """

    total = qs.count()
    for start in xrange(0, total, step):
        for obj in qs[start:start + step]:
            yield obj


def load_related(objects, rel_qs, rel_field_name, cache_field_name=None):
    """
    Load in one SQL query the objects from query set (rel_qs)
    which is linked to objects from (objects) via the field (rel_field_name).
    """

    obj_map = dict((x.id, x) for x in objects)
    rel_field = rel_qs.model._meta.get_field(rel_field_name)
    cache_field_name = '%s_cache' % rel_qs.model.__name__.lower()

    rel_objects = rel_qs.filter(**{'%s__in' % rel_field.name: obj_map.keys()})

    temp_map = {}
    for rel_obj in rel_objects:
        pk = getattr(rel_obj, rel_field.attname )
        temp_map.setdefault(pk, []).append(rel_obj)

    for pk, rel_list in temp_map.iteritems():
        setattr(obj_map[pk], cache_field_name, rel_list)


def generic_select_related(qs):
    generics = defaultdict(set)
    for item in qs:
        generics[item.content_type_id].add(item.object_id)

    content_types = ContentType.objects.in_bulk(generics.keys())

    relations = {}
    for ct, fk_list in generics.items():
        ct_model = content_types[ct].model_class()
        relations[ct] = ct_model.objects.in_bulk(list(fk_list))

    for item in qs:
        try:
            setattr(item, '_content_object_cache', 
                    relations[item.content_type_id][item.object_id])
        except KeyError:
            setattr(item, '_content_object_cache', None)
