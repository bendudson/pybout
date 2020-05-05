from pybout import Field
from pybout import functions

def test_delp2():
    f = Field("ne")
    g = functions.Delp2(f)
    assert repr(g) == "BoutFunction('Delp2', Field('ne'), include='difops.hxx')"

def test_delp2_asBoutReal():
    f = Field("ne")
    g = functions.Delp2(f)
    assert g.asBoutReal("i") == "Delp2(ne, i)"

def test_delp2_asField():
    f = Field("ne")
    g = functions.Delp2(f)
    assert g.asField() == "Delp2(ne)"

