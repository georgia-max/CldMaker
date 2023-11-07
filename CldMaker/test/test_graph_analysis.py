from CldMaker import graphviz_analysis


def test_check_syntax():
    g2 = """
        "order rate" -> "inventory" [arrowhead = vee]
        """

    assert graphviz_analysis.check_syntax(g2) == "\"order rate\" -> \"inventory\" [arrowhead = vee]"


def test_check_syntax2():
    # TODO fix this test
    g2 = """
    "order rate" -> "inventory" [arrowhead = vee
    """
    assert graphviz_analysis.check_syntax(g2) == "\"order rate\" -> \"inventory\" [arrowhead = vee]"


def test_clean_graphs():
    # TODO fix this test
    g = """
    digraph {
    "order rate" -> "inventory" [arrowhead = vee]
    "inventory"->"order rate"[arrowhead = tee] 
    "desired inventory" -> "order rate"[arrowhead = vee] 
    "adjustment time" -> "order rate"[arrowhead = tee] }
    """

    g2 = g.replace("\n", "")

    print(graphviz_analysis.clean_graphs(g))

    assert graphviz_analysis.clean_graphs(g) == g2


def test_render_gvz():
    g = """
    digraph {
    "order rate" -> "inventory" [arrowhead = vee]
    "inventory"->"order rate"[arrowhead = tee] 
    "desired inventory" -> "order rate"[arrowhead = vee] 
    "adjustment time" -> "order rate"[arrowhead = tee] }
    """

    assert graphviz_analysis.render_gvz(g, "test", "test", "img_output") is None
