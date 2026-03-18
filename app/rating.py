def expected_score(rating_a: int, rating_b: int) -> float:
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def calculate_new_ratings(rating_a: int, rating_b: int, a_wins: bool, k: int = 32) -> tuple[int, int]:
    expected_a = expected_score(rating_a, rating_b)
    expected_b = expected_score(rating_b, rating_a)

    score_a = 1 if a_wins else 0
    score_b = 0 if a_wins else 1

    new_a = round(rating_a + k * (score_a - expected_a))
    new_b = round(rating_b + k * (score_b - expected_b))

    return new_a, new_b