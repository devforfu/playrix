import random

from lxml import etree

from .utils import random_uid, random_level, random_string


class RandomGameEntity:

    def __init__(self, uid=None, level=None):
        self.uid = uid or random_uid()
        self.level = level or random_level()
        self.objects = []

    def build(self, min_obj=1, max_obj=10):
        n = random.randint(min_obj, max_obj)
        objects = [random_string() for _ in range(n)]
        self.objects = objects

    def to_xml(self, pretty=True):
        root = etree.Element('root')
        root.append(etree.Element('var', name='id', value=self.uid))
        root.append(etree.Element('var', name='level', value=str(self.level)))
        if self.objects:
            children = etree.Element('objects')
            for obj in self.objects:
                children.append(etree.Element('object', name=obj))
            root.append(children)
        bytes_array = etree.tostring(root, pretty_print=pretty)
        return bytes_array.decode(encoding='utf-8')
