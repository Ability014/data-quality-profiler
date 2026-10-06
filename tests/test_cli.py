import json
from dqp.cli import main


def test_profile_text(tmp_path, capsys):
    p = tmp_path / "d.csv"
    p.write_text("id,score\n1,9.5\n2,\n", encoding="utf-8")
    code = main(["profile", str(p)])
    out = capsys.readouterr().out
    assert code == 0
    assert "score" in out


def test_profile_json(tmp_path, capsys):
    p = tmp_path / "d.csv"
    p.write_text("id,score\n1,9.5\n", encoding="utf-8")
    code = main(["profile", str(p), "--format", "json"])
    data = json.loads(capsys.readouterr().out)
    assert code == 0
    assert data["row_count"] == 1


def test_missing_file_is_friendly(tmp_path, capsys):
    code = main(["profile", str(tmp_path / "nope.csv")])
    captured = capsys.readouterr()
    assert code == 1
    assert captured.err.startswith("error:")   # went to stderr, not stdout
    assert captured.out == ""
