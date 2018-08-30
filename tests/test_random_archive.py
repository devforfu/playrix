import os
import zipfile
from os.path import exists

from playrix.generate import RandomArchive


def test_generating_random_archive(tmpdir):
    filename = tmpdir.join('archive.zip')

    ra = RandomArchive(filename)
    ra.build()

    assert exists(filename)
    assert os.stat(filename).st_size > 0
    assert archive_has_n_entries(ra.n_entities, filename)


# ----------
# Test utils
# ----------


def archive_has_n_entries(n, filename):
    with zipfile.ZipFile(filename, 'r') as arch:
        return len(arch.namelist()) == n
