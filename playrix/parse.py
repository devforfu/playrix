import os
import zipfile
from pathlib import Path
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
        num_of_workers = num_of_workers or cpu_count()
        with Pool(num_of_workers) as pool:
            content = pool.map(parse_archive, self.files)
        return content
