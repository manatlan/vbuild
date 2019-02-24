# -*- coding: utf-8 -*-
import vbuild
import pytest

def test_real_files():
    import glob
    for i in glob.glob("tests/vues/*.vue"):
        r=vbuild.render(i)
        assert str(r)

    assert str(vbuild.render( "tests/vues/list.vue"))
    assert str(vbuild.render( "tests/vues/*.vue"))
    assert str(vbuild.render( "tests/*/*.vue"))
    assert str(vbuild.render( "tests/vues/test.vue", "tests/vues/todo.vue" ))
    assert str(vbuild.render( ["tests/vues/test.vue","tests/vues/todo.vue"] ))
    assert str(vbuild.render( glob.glob("tests/vues/*.vue")))


def test_bad_file():
    with pytest.raises(vbuild.VBuildException):
        vbuild.render("unknown_file.vue") # No such file or directory
