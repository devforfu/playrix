import os
import zipfile

import pandas as pd
from lxml import etree
from lxml.etree import XMLSyntaxError


def parse_entity_xml(io):
    """
    Reads content of XML file with game entities descriptions and returns its
    content in structured format.
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
    with zipfile.ZipFile(filename, 'r') as arch:
        content = {
            entry: parse_entity_xml(arch.read(entry))
            for entry in arch.namelist()}
    return content
