import os
import zipfile
from pathlib import Path
from collections import namedtuple
from multiprocessing import Pool, cpu_count

import pandas as pd
from lxml import etree
from lxml.etree import XMLSyntaxError


def parse_entity_xml(io):
    """
    Reads content of a single XML file with game entities descriptions and
    returns its content in structured format.
    """
    if os.path.exists(io):
        with open(io) as file:
            content = file.read()
    elif hasattr(io, 'read'):
        content = io.read()
    else:
        content = io

    try:
        tree = etree.fromstring(content)
    except (TypeError, ValueError):
        raise RuntimeError(f'cannot read XML content from {io}')
    except XMLSyntaxError as e:
        raise RuntimeError(f'invalid XML structure: {str(e)}')

    try:
        var1, var2, objects = tree.getchildren()
        uid, level = var1.attrib['value'], var2.attrib['value']
        objects = [obj.attrib['name'] for obj in objects]
        return {'id': uid, 'level': int(level), 'objects': objects}
    except ValueError:
        raise RuntimeError(f'invalid XML structure: missing or extra fields')


def parse_archive(filename):
    """
    Reads content of an archive with XML files and returns it in structured
    format.
    """
    with zipfile.ZipFile(filename, 'r') as arch:
        content = {
            entry: parse_entity_xml(arch.read(entry))
            for entry in arch.namelist()}
    return content


def gather_summary(archive_content):
    level_meta, level_objects = [], []
    for filename, record in archive_content.items():
        uid, level = record['id'], record['level']
        level_meta.append((uid, level))
        for obj in record['objects']:
            level_objects.append((uid, obj))
    return {'meta': level_meta, 'objects': level_objects}


ParsingResult = namedtuple('ParsingResult', ['meta', 'objects'])


class DirectoryParser:
    """
    An instance of the class goes through a directory with zipped XML files
    and parses their content.
    """
    def __init__(self, folder, pattern='*.zip', parallel=True):
        path = Path(folder)

        if not folder.exists():
            raise ValueError(f'file does not exist: {folder}')

        self.folder = path
        self.pattern = pattern
        self.files = list(path.glob(self.pattern))

    @property
    def n_files(self):
        return len(self.files)

    def parse(self, num_of_workers=None):
        with Pool(num_of_workers or cpu_count()) as pool:
            content = pool.map(parse_archive, self.files)
            summary = pool.map(gather_summary, content)

        meta, objects = [], []
        for result in summary:
            meta.extend(result['meta'])
            objects.extend(result['objects'])

        meta_df = pd.DataFrame(meta, columns=['id', 'level'])
        objects_df = pd.DataFrame(objects, columns=['id', 'object_name'])
        return ParsingResult(meta=meta_df, objects=objects_df)
