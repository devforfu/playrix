import pytest
import lxml

from playrix.generate import RandomGameEntity


def test_default_properties():
    go = RandomGameEntity()

    assert isinstance(go.uid, str) and go.uid != ''
    assert isinstance(go.level, int) and go.level > 0
    assert len(go.objects) == 0


def test_generating_random_array_of_objects():
    go = RandomGameEntity()

    go.build()

    assert 1 <= len(go.objects) <= 10
    assert all([bool(obj) for obj in go.objects])


def test_converting_into_xml():
    go = RandomGameEntity()
    go.build(min_obj=5, max_obj=5)

    content = go.to_xml()

    assert content != ''
    assert go.uid in content
    assert str(go.level) in content
    assert all([obj in content for obj in go.objects])
