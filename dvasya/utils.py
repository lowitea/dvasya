# coding: utf-8

# $Id: $


def import_object(class_path):
    """Imports object by its full class path.
    @type class_path: str
    @param class_path: object's full class path.

    @rtype object
    @return imported object
    """
    module_name, attr_name = class_path.rsplit('.', 1)
    module = __import__(module_name, fromlist=attr_name)
    return getattr(module, attr_name)
