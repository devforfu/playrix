import shutil

import pytest

from playrix.parse import DirectoryParser
from playrix.generate import RandomArchive
from playrix.utils import random_string


def test_discovering_archives_from_directory(directory):
    parser = DirectoryParser(directory)

    content = parser.parse()

    assert content is not None


@pytest.fixture
def directory(tmpdir):
    root = tmpdir.mkdir('archives')
    for _ in range(10):
        filename = root.join(f'{random_string()}.zip')
        archive = RandomArchive(filename)
        archive.build()
    yield root
    shutil.rmtree(root)
