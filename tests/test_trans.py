# -*- coding: utf-8 -*-
import vbuild
import pytest


def test_1():
    try:
        vbuild.transScript = lambda x: x.upper()
        vbuild.transStyle = lambda x: x + "/*Hello*/"
        vbuild.transHtml = lambda x: x.upper()
        r = vbuild.VBuild("toto.vue", "<template><div></div></template>")
        assert "VUE.COMPONENT('TOTO'" in r.script
        assert (
            '<script type="text/x-template" id="tpl-toto"><DIV DATA-TOTO></DIV></script>'
            in r.html
        )
        assert r.style == "/*Hello*/"
    finally:
        vbuild.transScript = lambda x: x
        vbuild.transStyle = lambda x: x
        vbuild.transHtml = lambda x: x
