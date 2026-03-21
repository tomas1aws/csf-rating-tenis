import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.rating import calculate_new_ratings


def test_mismo_nivel_ganador_sube():
    nuevo_a, nuevo_b = calculate_new_ratings(1000, 1000, a_wins=True)

    assert nuevo_a > 1000
    assert nuevo_b < 1000


def test_upset_gana_debil():
    nuevo_a, nuevo_b = calculate_new_ratings(1200, 800, a_wins=False)

    assert nuevo_b > 800
    assert nuevo_a < 1200