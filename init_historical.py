import json
import os
os.makedirs("data", exist_ok=True)
historical_data = {
    'Inflation': {'min_rel': 0.01, 'med_rel': 0.05, 'max_rel': 0.3, 'history': [0.01, 0.05, 0.1, 0.2, 0.3]},
    'Migration': {'min_rel': 0.01, 'med_rel': 0.05, 'max_rel': 0.4, 'history': [0.01, 0.05, 0.3, 0.41]},
    'Environment': {'min_rel': 0.01, 'med_rel': 0.05, 'max_rel': 0.5, 'history': [0.01, 0.05, 0.5, 0.51]},
    'Energy': {'min_rel': 0.01, 'med_rel': 0.05, 'max_rel': 0.4, 'history': [0.01, 0.05, 0.099, 0.4]},
    'Safety': {'min_rel': 0.01, 'med_rel': 0.05, 'max_rel': 0.4, 'history': [0.01, 0.05, 0.2, 0.4]}
}
with open("data/social_presence_stats.json", "w") as f:
    json.dump(historical_data, f, indent=2)