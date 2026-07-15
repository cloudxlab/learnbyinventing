#!/usr/bin/env python3
"""Test runner for recommender exercises. Run: python test_exercises.py"""
import sys
import os
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

def test_ex_2_1_cosine_similarity():
    from exercises.ex_2_1_cosine_similarity import cosine_similarity
    # Tests
    me = filled["SandeepGiri"]
    assert abs(cosine_similarity(me, me) - 1.0) < 1e-9        # identical vectors
    assert abs(cosine_similarity(me, filled["Abhishek"]) - 0.8198) < 1e-3
    print("sim(SandeepGiri, Abhishek) =",
          round(cosine_similarity(me, filled["Abhishek"]), 4))

def test_ex_2_4_most_similar():
    from exercises.ex_2_4_most_similar import most_similar
    # Tests
    assert most_similar("SandeepGiri") == "Madhuri"
    for p in ["SandeepGiri", "Abhishek", "Venu", "Gurpreet"]:
        print(p, "->", most_similar(p),
              round(sim[p].drop(p).max(), 3))

def test_ex_3_1_unrated_movies():
    from exercises.ex_3_1_unrated_movies import unrated_movies
    # Tests
    mine = unrated_movies("SandeepGiri")
    assert len(mine) == 10
    assert "Dangal" in mine and "Mughal-e-Azam" in mine
    print("SandeepGiri hasn't rated:", mine)

def test_ex_3_2_recommend():
    from exercises.ex_3_2_recommend import recommend
    # Tests
    recs = recommend("SandeepGiri", 3)
    assert len(recs) == 3
    assert all(m in unrated_movies("SandeepGiri") for m in recs)
    assert recs[0] == "Dangal"
    print("SandeepGiri should watch:", recs)
    print("Abhishek should watch:  ", recommend("Abhishek", 3))

def test_ex_4_1_top5_similar_people():
    from exercises.ex_4_1_top5_similar_people import top5_similar_people
    from exercises.ex_4_1_top5_similar_people import top5_favorites
    from exercises.ex_4_1_top5_similar_people import recommend_by_friends
    # Tests
    assert top5_similar_people("SandeepGiri") == ["Madhuri", "Stuti", "Prabha", "Aakash", "Gurpreet"]
    assert len(top5_favorites("Abhishek")) == 5

    friend_recs = recommend_by_friends("SandeepGiri")
    assert set(friend_recs) == {"Mughal-e-Azam", "Dangal", "Yeh Jawaani Hai Deewani"}
    assert all(m in unrated_movies("SandeepGiri") for m in friend_recs)
    print("friends say:", friend_recs)
    print("weighted votes said:", recommend("SandeepGiri", 3))

def test_ex_4_2_most_similar_movie():
    from exercises.ex_4_2_most_similar_movie import most_similar_movie
    # Tests
    assert S_items.shape == (25, 25)
    assert np.allclose(S_items, S_items.T)
    assert np.allclose(np.diag(S_items), 1)
    assert most_similar_movie("Sholay") == "3 Idiots"
    for movie in ["Sholay", "Dangal", "Pathaan"]:
        print(f"people who liked {movie!r} also liked:",
              most_similar_movie(movie))


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = errors = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {t.__name__}: {e}")
        except Exception as e:
            errors += 1
            print(f"  ERROR {t.__name__}: {type(e).__name__}: {e}")
    total = passed + failed + errors
    print(f"\n{passed}/{total} passed, {failed} failed, {errors} errors")
    sys.exit(0 if failed + errors == 0 else 1)
