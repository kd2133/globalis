# app.py
# Streamlit-UI für den Global Sentiment Index (GSI)

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from data_loader import load_data
from models.gsi_score import calculate_gsi_impact
from models.gsi_weighted import calculate_weighted_gsi
from utils.helpers import get_news_contrast

# Seite konfigurieren
st.set_page_config(page_title="Global Sentiment Index", layout="wide")
st.title("🌍 Global Sentiment Index (GSI)")
st.markdown("Erfasst und visualisiert weltweite Stimmungen zu Themen wie Wirtschaft oder Umwelt in Echtzeit.")

# Datenquelle wählen
source = st.selectbox("Datenquelle wählen:", ["db", "json", "csv"], help="Wähle zwischen SQLite, JSON oder CSV.")

# Daten laden
try:
    data = load_data(source=source)
except Exception as e:
    st.error(f"⚠️ Fehler beim Laden der Daten: {e}")
    st.stop()

if not data:
    st.error("⚠️ Keine Daten geladen. Prüfe die Datenquelle (z.B. gsi_data.db, historical_data.json).")
    st.stop()

# Impact Score berechnen
for d in data:
    if d.get('impact_score') is None:
        try:
            result = calculate_gsi_impact(d)
            d['impact_score'] = result["Final Impact Score"]
        except Exception as e:
            st.warning(f"Fehler bei Impact Score für {d.get('topic', 'unbekannt')}: {e}")
            d['impact_score'] = 0.0

# GSI berechnen
try:
    gsi_weighted = calculate_weighted_gsi(data)
except Exception as e:
    st.error(f"⚠️ Fehler bei GSI-Berechnung: {e}")
    gsi_weighted = 0.0

# GSI anzeigen
st.header(f"Global Sentiment Index (Weighted): {gsi_weighted:.2f}")
st.markdown("Der GSI aggregiert Stimmungen über alle Themen, gewichtet nach Social Presence.")

# Sortieroptionen
sort_by = st.selectbox("Sortieren nach:", ["Impact Score", "Social Presence", "Sentiment (Raw)"],
                       help="Sortiere die Tabelle nach gewünschter Spalte.")
sort_order = st.radio("Reihenfolge:", ["Absteigend", "Aufsteigend"], horizontal=True)
sort_column = {"Impact Score": "impact_score", "Social Presence": "social_presence", "Sentiment (Raw)": "sentiment_raw"}[sort_by]
ascending = sort_order == "Aufsteigend"

# Tabelle mit Kontrastfolie
st.header("Themenübersicht")
try:
    df = pd.DataFrame(data)
    required_columns = ["topic", "country", "impact_score", "social_presence", "sentiment_raw", "news_presence"]
    if not all(col in df.columns for col in required_columns):
        st.error(f"⚠️ Daten fehlen erforderliche Spalten: {', '.join(set(required_columns) - set(df.columns))}")
        st.stop()
    # Kontrastfolie berechnen mit Validierung
    def safe_news_contrast(row):
        try:
            social = float(row["social_presence"]) * 100  # Skalierung anpassen, falls nötig
            news = float(row["news_presence"])
            return get_news_contrast(social, news)
        except (ValueError, TypeError, KeyError) as e:
            st.warning(f"Fehler bei Kontrastfolie für {row.get('topic', 'unbekannt')}: {e}")
            return "Unknown"
    df["News Contrast"] = df.apply(safe_news_contrast, axis=1)
except Exception as e:
    st.error(f"⚠️ Fehler beim Erstellen der Tabelle: {e}")
    st.stop()

# Farbskala für Kontrastfolie
def color_contrast(row):
    if row["Kontrastfolie"] == "Underreported: Die Menschen sind betroffen, aber die Medien schweigen ⚠️":
        return ['background-color: #90EE90'] * len(row)  # Hellgrün
    elif row["Kontrastfolie"] == "Overreported: Medien pushen es, aber niemanden juckt es eigentlich ❗":
        return ['background-color: #FFB6C1'] * len(row)  # Hellrot
    elif row["Kontrastfolie"] == "Kein relevantes Thema – low impact, low coverage":
        return ['background-color: #D3D3D3'] * len(row)  # Grau für "low-low"
    elif row["Kontrastfolie"] == "Starkes Thema mit breiter medialer und öffentlicher Aufmerksamkeit ✔️":
        return ['background-color: #ADD8E6'] * len(row)  # Optional: Hellblau für starke Themen
    return [''] * len(row)


df["News Contrast"] = df.apply(safe_news_contrast, axis=1)

df = df[["topic", "country", "impact_score", "social_presence", "sentiment_raw", "news_presence", "News Contrast"]]
df = df.sort_values(by=sort_column, ascending=ascending)
st.dataframe(df.rename(columns={
    "topic": "Thema",
    "country": "Land",
    "impact_score": "Impact Score",
    "social_presence": "Social Presence",
    "sentiment_raw": "Sentiment (Raw)",
    "news_presence": "News Presence",
    "News Contrast": "Kontrastfolie"
}).style.apply(color_contrast, axis=1), use_container_width=True)

# Filter für Länder
countries = sorted(set(d["country"] for d in data))
selected_country = st.selectbox("Land filtern:", ["Alle"] + countries, help="Wähle ein Land oder 'Alle'.")
if selected_country != "Alle":
    filtered_df = df[df["Land"] == selected_country]
    st.header(f"Themen für {selected_country}")
    st.dataframe(filtered_df.style.apply(color_contrast, axis=1), use_container_width=True)

# Balkendiagramm
st.header("Visualisierung: Impact Scores")
fig = px.bar(df, x="topic", y="impact_score", color="country",
             title="Impact Scores nach Thema und Land",
             labels={"impact_score": "Impact Score", "topic": "Thema"},
             color_discrete_sequence=px.colors.qualitative.Plotly,
             hover_data=["social_presence", "sentiment_raw", "news_presence"])

fig.update_layout(
    yaxis=dict(
        range=[0, 110],
        tick0=0,
        dtick=20  # alle 20 Punkte ein Strich
    )
)



fig.update_layout(
    xaxis_tickangle=-45,
    showlegend=True,
    barmode="group"  # Balken gruppieren statt stapeln
)

st.plotly_chart(fig, use_container_width=True)

# Export-Button
if st.button("Daten als CSV exportieren", help="Exportiert die Tabelle als CSV-Datei"):
    try:
        filename = f"data/gsi_export_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        df.to_csv(filename, index=False)
        st.success(f"Daten als '{filename}' exportiert!")
    except Exception as e:
        st.error(f"⚠️ Fehler beim Export: {e}")


