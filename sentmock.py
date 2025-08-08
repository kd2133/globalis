from utils.helpers import calculate_combined_score

test_cases = [
    (0.01, 0.01, 0.05, 0.3, -0.8, "negativ, min_rel"),      # 50.0
    (0.05, 0.01, 0.05, 0.3, 0.8, "positiv, med_rel"),        # 70.0
    (0.3, 0.01, 0.05, 0.3, -0.8, "negativ, max_rel"),        # 10.0
    (0.3, 0.01, 0.05, 0.3, 0.8, "positiv, max_rel"),         # 90.0
    (0.15, 0.01, 0.05, 0.3, 0.8, "positiv, zw. med/max"),    # 78.0
    (0.15, 0.01, 0.05, 0.3, -0.8, "negativ, zw. med/max"),   # 22.0
    (0.2, 0.01, 0.05, 0.3, 0.8, "positiv, zw. med/max"),     # 82.0
    (0.2, 0.01, 0.05, 0.3, -0.8, "negativ, zw. med/max"),    # 18.0
    (0.05, 0.01, 0.05, 0.3, 0.0, "neutral, med_rel"),        # 50.0
    (0.15, 0.01, 0.05, 0.3, 0.0, "neutral, zw. med/max"),    # 50.0
    (0.3, 0.01, 0.05, 0.3, 0.0, "neutral, max_rel"),         # 50.0
    (2.99, 0.01, 0.05, 3.0, 0.3, "positiv, knapp unter max_rel"),  # 64.97
    (3.0, 0.01, 0.05, 3.0, 0.3, "positiv, max_rel"),         # 65.0
    (6.0, 0.01, 0.05, 3.0, 0.3, "positiv, 2x max_rel"),      # 65.0
    (2.99, 0.01, 0.05, 3.0, -0.3, "negativ, knapp unter max_rel"),  # 35.03
    (3.0, 0.01, 0.05, 3.0, -0.3, "negativ, max_rel"),        # 35.0
]

for pr, minr, medr, maxr, sent, label in test_cases:
    score = calculate_combined_score(pr, minr, medr, maxr, sent)
    print(f"{label}: {score:.2f}")