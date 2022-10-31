import diceparser

def test_minmax():
    parser = diceparser.DiceParser()
    assert parser.eval("min", "2d6+1") == 3
    assert parser.eval("max", "2d6+1") == 13
