import graphviz_analysis

def test_render_gvz():
    
    g = """
    digraph {
    "order rate" -> "inventory" [arrowhead = vee]
    "inventory"->"order rate"[arrowhead = tee] 
    "desired inventory" -> "order rate"[arrowhead = vee] 
    "adjustment time" -> "order rate"[arrowhead = tee] }
    """

    assert graphviz_analysis.render_gvz(g, "test") == None 
