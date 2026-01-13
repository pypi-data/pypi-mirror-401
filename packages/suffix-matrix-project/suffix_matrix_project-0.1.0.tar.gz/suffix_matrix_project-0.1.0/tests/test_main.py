from app.main import suffix_matrix

def test_suffix_matrix():
    s = "ciao$"
    suf_matrix = suffix_matrix(s)
    assert len(suf_matrix) == 5
    assert suf_matrix[0] == "ciao$"
    assert suf_matrix[1] == "iao$"
    assert suf_matrix[2] == "ao$"
    assert suf_matrix[3] == "o$"
    assert suf_matrix[4] == "$"