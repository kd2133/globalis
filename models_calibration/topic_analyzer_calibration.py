import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.topic_analyzer import analyze_topic

topics = ["Inflation", "Migration", "Environment", "Energy", "Safety"]

inflation_true = [
    "Prices in supermarkets are rising.",
    "The inflation rate hit a new high.",
    "Central banks are worried about inflation.",
    "Rent and utility costs keep increasing.",
    "Groceries cost more than last year.",
    "Inflation affects everyone's savings.",
    "Wages can't keep up with inflation.",
    "The cost of living is skyrocketing.",
    "Interest rates are rising due to inflation.",
    "People complain about expensive fuel."
]
inflation_false = [
    "Migrants are arriving at the border.",
    "Renewable energies are the future.",
    "Police increased patrols in the city.",
    "Wind power is becoming more popular.",
    "Citizens are concerned about safety at night.",
    "Climate protection is extremely important.",
    "Security measures were improved in public spaces.",
    "Solar panels are being installed in many homes.",
    "Fashion trends change every year.",
    "Traveling broadens the mind."
]

migration_true = [
    "Migrants are arriving at the border.",
    "The government is discussing new migration laws.",
    "Many people are seeking asylum.",
    "Refugees are looking for a safe place.",
    "Immigration numbers are rising.",
    "Families are waiting for their visas.",
    "Newcomers enrich our culture.",
    "Border controls have been tightened.",
    "Integration programs are being expanded.",
    "Citizens debate migration policies."
]
migration_false = [
    "The inflation rate hit a new high.",
    "Wind power is becoming more popular.",
    "Security measures were improved in public spaces.",
    "Prices in supermarkets are rising.",
    "Climate protection is extremely important.",
    "Energy prices are rising.",
    "Police increased patrols in the city.",
    "Solar panels are being installed in many homes.",
    "Reading novels is relaxing.",
    "Gaming is a popular hobby."
]

environment_true = [
    "Renewable energies are the future.",
    "Climate protection is extremely important.",
    "We need to do more for the environment.",
    "Plastic waste pollutes our oceans.",
    "Recycling rates must improve.",
    "Air quality is getting worse.",
    "Wildlife habitats are shrinking.",
    "Deforestation is a global issue.",
    "Sustainable farming is necessary.",
    "Greenhouse gas emissions must be reduced."
]
environment_false = [
    "Central banks are worried about inflation.",
    "Police increased patrols in the city.",
    "The government is discussing new migration laws.",
    "Energy prices are rising.",
    "Migrants are arriving at the border.",
    "Security measures were improved in public spaces.",
    "Interest rates are rising due to inflation.",
    "Fashion trends change every year.",
    "My cat is very playful.",
    "Comedy shows are entertaining."
]

energy_true = [
    "Wind power is becoming more popular.",
    "Energy prices are rising.",
    "Solar panels are being installed in many homes.",
    "Hydroelectric plants supply clean energy.",
    "Electric cars are gaining popularity.",
    "The city built a new wind farm.",
    "Gas prices fluctuate every month.",
    "Smart grids improve energy efficiency.",
    "Battery technology is advancing rapidly.",
    "Renewable energy sources are expanding."
]
energy_false = [
    "Migrants are arriving at the border.",
    "Climate protection is extremely important.",
    "Security measures were improved in public spaces.",
    "Citizens are concerned about safety at night.",
    "Plastic waste pollutes our oceans.",
    "Interest rates are rising due to inflation.",
    "Many people are seeking asylum.",
    "Reading novels is relaxing.",
    "Football is my favorite sport.",
    "Traveling broadens the mind."
]

safety_true = [
    "Police increased patrols in the city.",
    "Security measures were improved in public spaces.",
    "Citizens are concerned about safety at night.",
    "Neighborhood watch groups are active.",
    "Schools installed new security cameras.",
    "Emergency drills are held monthly.",
    "Street lights have been added.",
    "Crime rates are being monitored.",
    "People lock their doors during the day.",
    "Body cams improve policing."
]
safety_false = [
    "Energy prices are rising.",
    "Many people are seeking asylum.",
    "We need to do more for the environment.",
    "Plastic waste pollutes our oceans.",
    "Wind power is becoming more popular.",
    "Interest rates are rising due to inflation.",
    "Groceries cost more than last year.",
    "Fashion trends change every year.",
    "Art inspires creativity.",
    "Gaming is a popular hobby."
]

irrelevant_texts = [
    "Football is my favorite sport.",
    "I love cooking Italian food.",
    "The concert last night was amazing.",
    "My cat is very playful.",
    "Reading novels is relaxing.",
    "Fashion trends change every year.",
    "Gaming is a popular hobby.",
    "Traveling broadens the mind.",
    "Art inspires creativity.",
    "Comedy shows are entertaining.",
    "I went hiking in the mountains.",
    "My friend just bought a new bike.",
    "We watched a movie together.",
    "The weather is nice today.",
    "I enjoy painting landscapes.",
    "My dog loves to play fetch.",
    "I started learning Spanish.",
    "Baking bread is fun.",
    "I visited a museum last weekend.",
    "Board games are great for parties."
]
def print_topic_scores(texts, expected_topic):
    for i, text in enumerate(texts):
        detected_topic = analyze_topic(text)
        match = "✔️" if detected_topic == expected_topic else "❌"
        print(f"{expected_topic}: Text {i+1} -> Detected: {detected_topic} {match}")

print("Inflation (should match):")
print_topic_scores(inflation_true, "Inflation")
print("Inflation (should NOT match):")
print_topic_scores(inflation_false, "Inflation")
print("---------------------------------------------------")
print("Migration (should match):")
print_topic_scores(migration_true, "Migration")
print("Migration (should NOT match):")
print_topic_scores(migration_false, "Migration")
print("---------------------------------------------------")
print("Environment (should match):")
print_topic_scores(environment_true, "Environment")
print("Environment (should NOT match):")
print_topic_scores(environment_false, "Environment")
print("---------------------------------------------------")
print("Energy (should match):")
print_topic_scores(energy_true, "Energy")
print("Energy (should NOT match):")
print_topic_scores(energy_false, "Energy")
print("---------------------------------------------------")
print("Safety (should match):")
print_topic_scores(safety_true, "Safety")
print("Safety (should NOT match):")
print_topic_scores(safety_false, "Safety")



print("---------------------------------------------------")
print("Others (should match):")
for i, text in enumerate(irrelevant_texts):
    detected_topic = analyze_topic(text)
    match = "✔️" if detected_topic == "Other" else "❌"
    print(f"Sonstiges: Text {i+1} -> Detected: {detected_topic} {match}")



# 118 / 120 Texten sind correct (98.33%)