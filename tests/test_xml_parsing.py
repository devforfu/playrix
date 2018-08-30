import shutil
import zipfile
from textwrap import dedent

import pytest

from playrix.parse import parse_archive
from playrix.parse import parse_entity_xml


def test_parsing_valid_xml_file(xml):
    parsed = parse_entity_xml(xml)
    expected_objects = ['first', 'second', 'third']

    assert parsed['id'] == 'unique-string'
    assert parsed['level'] == 1
    assert parsed['objects'] == expected_objects


def test_parsing_zip_archive_with_xml_files(archive):
    expected_files = ['x.xml', 'y.xml', 'z.xml']
    expected_objects = ['first', 'second', 'third']

    files = parse_archive(archive)

    assert len(files) == len(expected_files)
    assert expected_files == sorted(files)
    assert all_has_valid_id(files, expected_files)
    assert all_has_valid_level(files, expected_files)
    assert all_has_valid_objects(files, expected_files, expected_objects)


# ----------
# Test utils
# ----------


def all_has_valid_id(actual, expected):
    return all([actual[name]['id'] == 'unique-string' for name in expected])


def all_has_valid_level(actual, expected):
    return all([actual[name]['level'] == 1 for name in expected])


def all_has_valid_objects(actual, expected, objects):
    return all([actual[name]['objects'] == objects for name in expected])


@pytest.fixture
def xml():
    return dedent('''
    <root>
        <var name='id' value='unique-string' />
        <var name='level' value='1' />
        <objects>
            <object name='first' />
            <object name='second' />
            <object name='third' />
        </objects>
    </root>
    ''')


@pytest.fixture
def archive(xml, tmpdir):
    filename = tmpdir.join('archive.zip')
    xml_file = tmpdir.join('content.xml')
    with zipfile.ZipFile(filename, 'w') as arch:
        with open(xml_file, 'w') as file:
            file.write(xml)
        arch.write(xml_file, 'x.xml')
        arch.write(xml_file, 'y.xml')
        arch.write(xml_file, 'z.xml')
    yield filename
    shutil.rmtree(tmpdir)
