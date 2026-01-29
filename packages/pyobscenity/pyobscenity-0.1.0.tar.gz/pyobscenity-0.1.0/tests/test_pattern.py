from pyobscenity.pattern import PatternParser, BoundaryAssertionNode, LiteralNode, WildcardNode, OptionalNode

def test_pattern_parser_simple():
    parser = PatternParser()
    nodes = parser.parse_pattern("abc")
    assert len(nodes.nodes) == 1
    assert all(node.chars is not None for node in nodes.nodes)
    assert [node.chars for node in nodes.nodes] == [list(map(ord, ['a', 'b', 'c']))]

def test_pattern_parser_boundaries():
    parser = PatternParser()
    nodes1 = parser.parse_pattern("|abc")
    assert nodes1.require_word_boundary_at_start
    assert not nodes1.require_word_boundary_at_end
    assert len(nodes1.nodes) == 2
    assert isinstance(nodes1.nodes[0], BoundaryAssertionNode)
    assert isinstance(nodes1.nodes[1], LiteralNode)
    assert nodes1.nodes[1].chars == list(map(ord, ['a', 'b', 'c']))

    nodes2 = parser.parse_pattern("abc|")
    assert nodes2.require_word_boundary_at_end
    assert not nodes2.require_word_boundary_at_start
    assert len(nodes2.nodes) == 2
    assert isinstance(nodes2.nodes[0], LiteralNode)
    assert isinstance(nodes2.nodes[1], BoundaryAssertionNode)
    assert nodes2.nodes[0].chars == list(map(ord, ['a', 'b', 'c']))

    nodes3 = parser.parse_pattern("|abc|")
    assert len(nodes3.nodes) == 3
    assert isinstance(nodes3.nodes[0], BoundaryAssertionNode)
    assert isinstance(nodes3.nodes[1], LiteralNode)
    assert isinstance(nodes3.nodes[2], BoundaryAssertionNode)
    assert nodes3.nodes[1].chars == list(map(ord, ['a', 'b', 'c']))

    # Test "bad" patterns with multiple boundaries
    try:
        parser.parse_pattern("||abc")
        assert False, "Expected ValueError for multiple starting boundaries"
    except ValueError:
        pass


def test_pattern_parser_additional_cases():
    parser = PatternParser()

    # Ensure no None entries appear in nodes for several patterns
    patterns = ["a?b c", "|a b c", "abc |", "|ab?c|", ""]
    for p in patterns:
        parsed = parser.parse_pattern(p)
        assert None not in parsed.nodes

    # Boundary assertion in the middle should raise
    try:
        parser.parse_pattern("a|bc")
        assert False, "Expected ValueError for boundary in middle"
    except ValueError:
        pass

    # Boundary assertion inside an optional should raise
    try:
        parser.parse_pattern("[|]")
        assert False, "Expected ValueError for boundary inside optional"
    except ValueError:
        pass

    # Multiple boundary assertions in sequence should raise
    try:
        parser.parse_pattern("||abc")
        assert False, "Expected ValueError for multiple starting boundaries"
    except ValueError:
        pass

    try:
        parser.parse_pattern("abc||")
        assert False, "Expected ValueError for multiple trailing boundaries"
    except ValueError:
        pass


def test_pattern_parser_wildcards_and_optionals():
    parser = PatternParser()

    pattern = "[Aa]?c"
    parsed = parser.parse_pattern(pattern)
    print(parsed)
    assert len(parsed.nodes) == 3
    assert isinstance(parsed.nodes[0], OptionalNode)
    assert isinstance(parsed.nodes[1], WildcardNode)
    assert isinstance(parsed.nodes[2], LiteralNode)
    assert set(parsed.nodes[0].child_node.chars) == set(map(ord, ['a', 'A']))
    assert list(parsed.nodes[2].chars) == list(map(ord, ['c']))


def test_pattern_parser_empty_pattern():
    parser = PatternParser()
    parsed = parser.parse_pattern("")
    assert len(parsed.nodes) == 0
    assert not parsed.require_word_boundary_at_start
    assert not parsed.require_word_boundary_at_end

def test_pattern_parser_as_regex():
    parser = PatternParser()
    pattern = "|a?b c|"
    parsed = parser.parse_pattern(pattern)
    regex = parsed.as_regex()
    assert regex == r'\b\x61.\x62\x20\x63\b'