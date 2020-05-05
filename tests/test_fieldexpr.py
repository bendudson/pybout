from pybout import fieldexpr

def test_field():
    f = fieldexpr.Field("ne")

    assert f.asField() == "ne"
    assert f.asBoutReal("ind") == "ne[ind]"

def test_addition():
    f = fieldexpr.Field("ne")

    assert (f + f).asField() == "(ne+ne)"
    assert (f + f).asBoutReal("i") == "(ne[i]+ne[i])"
    assert (f + 3).asBoutReal("i") == "(ne[i]+3)"
