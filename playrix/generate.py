import os
import random
import shutil
import zipfile
import tempfile

from lxml import etree

from .utils import random_uid, random_level, random_string


class RandomGameEntity:
    """
    Generates a random game entity.

    The class generates a random set of values and converts them into XML
    format. Note that the process of data generation and building of XML
    content are separated from each other.

    Example:
    >>> entity = RandomGameEntity()
    >>> entity.build()
    >>> xml_content = entity.to_xml()

    Parameters:
        uid: Unique XML file identifier.
        level: Random level value.

    """
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


def default_factory(*args, **kwargs):
    """
    Default generator of random game entities.
    """
    obj = RandomGameEntity()
    obj.build(*args, **kwargs)
    return obj


class RandomArchive:
    """
    Creates a ZIP-archive with randomly generated XML files.

    Parameters:
        filename: Path to the file with generated archive.
        n_entities: Number of XML files to be generated.
        factory: Callable invoked to generate a random game entity.

    """
    def __init__(self, filename, n_entities=100, factory=default_factory):
        self.filename = filename
        self.n_entities = n_entities
        self.factory = factory

    def build(self, *args, **kwargs):
        if os.path.exists(self.filename):
            raise FileExistsError(
                'cannot generate an archive: it is already exists')

        padding = len(str(self.n_entities))
        template = '{i:0%dd}.xml' % padding

        with zipfile.ZipFile(self.filename, 'w') as arch:
            dirname = tempfile.mkdtemp()

            for i in range(self.n_entities):
                obj = self.factory(*args, **kwargs)
                content = obj.to_xml()
                entry_name = template.format(i=i)
                temp_file = os.path.join(dirname, entry_name)
                with open(temp_file, 'w') as xml_file:
                    xml_file.write(content)
                arch.write(temp_file, entry_name)

            shutil.rmtree(dirname)
