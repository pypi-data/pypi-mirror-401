def test_cursor_start(kb):
    assert kb.cursor_hash(None) == "start"
