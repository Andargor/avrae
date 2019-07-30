from utils.argparser import argparse, argquote, argsplit


def test_argsplit():
    assert argsplit("""foo bar "two words" yay!""") == ["foo", "bar", "two words", "yay!"]
    assert argsplit("""'some string here' in quotes""") == ["some string here", "in", "quotes"]
    assert argsplit(""""partial quoted"blocks""") == ["partial quotedblocks"]
    assert argsplit('''"'nested quotes'"''') == ["'nested quotes'"]
    assert argsplit("""-phrase "She said, \\"Hello world\\"" """) == ["-phrase", 'She said, "Hello world"']


def test_argquote():
    assert argquote("foo") == "foo"
    assert argquote("foo bar") == '"foo bar"'
    assert argquote('one "two three"') == '"one \\"two three\\""'
    assert argsplit(argquote('one "two three"')) == ['one "two three"']


def test_argparse():
    args = argparse("""-phrase "hello world" -h argument -t or1 -t or2""")
    assert args.last('phrase') == 'hello world'
    assert args.get('t') == ['or1', 'or2']
    assert args.adv() == 0
    assert args.last('t') == 'or2'
    assert args.last('h', type_=bool) is True
    assert 'argument' in args
    assert args.last('notin', default=5) == 5

    args = argparse("""adv""")
    assert args.adv() == 1

    args = argparse("""adv dis adv""")
    assert args.adv() == 0


def test_argparse_ephem():
    args = argparse("""-d5 1d6 adv1 -d 1""")
    for _ in range(4):
        assert args.join('d', '+', ephem=True) == '1+1d6'
    assert args.last('d', ephem=True) == '1d6'

    # we have consumed all 5 uses of ephem:d
    assert args.join('d', '+', ephem=True) == '1'
    assert args.last('d', ephem=True) == '1'

    # one ephem:adv
    # yes, this looks weird
    assert args.adv(ephem=True)
    assert not args.adv(ephem=True)
