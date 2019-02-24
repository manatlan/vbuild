# -*- coding: utf-8 -*-
import vbuild
import pytest


@pytest.mark.skipif(not vbuild.hasClosure, reason="requires closure")
def test_bad():

    s = """
    kk{{_=*juhgj;://\\}$bc(.[hhh]
    """
    with pytest.raises(
        vbuild.VBuildException
    ):  # vbuild.VBuildException: minimize error: [{'type': 'JSC_PARSE_ERROR', 'file': 'Input_0', 'lineno': 2, 'charno': 10, 'error': 'Parse error. Semi-colon expected', 'line': '        kk{{_=*jùhgj;://\\}$bc(.[hhh]'}]
        vbuild.jsmin(s)


@pytest.mark.skipif(not vbuild.hasClosure, reason="requires closure")
def test_min():

    s = """
    async function  jo(...a) {
        var f=(...a) => {let b=`hello`}
    }
    """
    x = vbuild.jsmin(s)
    assert "$jscomp" in x
