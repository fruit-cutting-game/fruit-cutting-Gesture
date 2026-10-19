from src.score_manager import ScoreManager

def test_score_and_combo():
    score = ScoreManager(); score.add_points(10); score.add_points(20)
    assert score.score == 30 and score.combo == 2
