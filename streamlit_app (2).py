# streamlit_app.py
"""
Interactive antibiotic‐effectiveness story
Burtin MIC dataset | Altair + Streamlit
"""
import streamlit as st
import pandas as pd
import altair as alt

# ────────────────────────────────────────────────────────────────
# Page setup
# ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Antibiotic Effectiveness Story", page_icon="🧫")
st.title("Penicillin’s Edge Against Gram‑Positive Pathogens")

# ────────────────────────────────────────────────────────────────
# Data (16 species × 3 antibiotics)
# ────────────────────────────────────────────────────────────────
data = [
    {"Bacteria": "Aerobacter aerogenes",        "Penicillin": 870,  "Streptomycin": 1,    "Neomycin": 1.6,  "Gram_Staining": "negative"},
    {"Bacteria": "Bacillus anthracis",          "Penicillin": 0.001,"Streptomycin": 0.01, "Neomycin": 0.007,"Gram_Staining": "positive"},
    {"Bacteria": "Brucella abortus",            "Penicillin": 1,    "Streptomycin": 2,    "Neomycin": 0.02, "Gram_Staining": "negative"},
    {"Bacteria": "Diplococcus pneumoniae",      "Penicillin": 0.005,"Streptomycin": 11,   "Neomycin": 10,   "Gram_Staining": "positive"},
    {"Bacteria": "Escherichia coli",            "Penicillin": 100,  "Streptomycin": 0.4,  "Neomycin": 0.1,  "Gram_Staining": "negative"},
    {"Bacteria": "Klebsiella pneumoniae",       "Penicillin": 850,  "Streptomycin": 1.2,  "Neomycin": 1,    "Gram_Staining": "negative"},
    {"Bacteria": "Mycobacterium tuberculosis",  "Penicillin": 800,  "Streptomycin": 5,    "Neomycin": 2,    "Gram_Staining": "negative"},
    {"Bacteria": "Proteus vulgaris",            "Penicillin": 3,    "Streptomycin": 0.1,  "Neomycin": 0.1,  "Gram_Staining": "negative"},
    {"Bacteria": "Pseudomonas aeruginosa",      "Penicillin": 850,  "Streptomycin": 2,    "Neomycin": 0.4,  "Gram_Staining": "negative"},
    {"Bacteria": "Salmonella (Eberthella) typhosa","Penicillin":1,  "Streptomycin": 0.4,  "Neomycin": 0.008,"Gram_Staining": "negative"},
    {"Bacteria": "Salmonella schottmuelleri",   "Penicillin": 10,   "Streptomycin": 0.8,  "Neomycin": 0.09, "Gram_Staining": "negative"},
    {"Bacteria": "Staphylococcus albus",        "Penicillin": 0.007,"Streptomycin": 0.1,  "Neomycin": 0.001,"Gram_Staining": "positive"},
    {"Bacteria": "Staphylococcus aureus",       "Penicillin": 0.03, "Streptomycin": 0.03, "Neomycin": 0.001,"Gram_Staining": "positive"},
    {"Bacteria": "Streptococcus fecalis",       "Penicillin": 1,    "Streptomycin": 1,    "Neomycin": 0.1,  "Gram_Staining": "positive"},
    {"Bacteria": "Streptococcus hemolyticus",   "Penicillin": 0.001,"Streptomycin": 14,   "Neomycin": 10,   "Gram_Staining": "positive"},
    {"Bacteria": "Streptococcus viridans",      "Penicillin": 0.005,"Streptomycin": 10,   "Neomycin": 40,   "Gram_Staining": "positive"},
]

df_long = pd.DataFrame(data).melt(
    id_vars=["Bacteria", "Gram_Staining"],
    value_vars=["Penicillin", "Streptomycin", "Neomycin"],
    var_name="Antibiotic",
    value_name="MIC"
)

# ────────────────────────────────────────────────────────────────
# Interactive legend + annotation
# ────────────────────────────────────────────────────────────────
legend_select = alt.selection_multi(fields=["Gram_Staining"], bind="legend")

points = (
    alt.Chart(df_long)
    .encode(
        x=alt.X("Antibiotic:N", title=None),
        y=alt.Y("MIC:Q",
                scale=alt.Scale(type="log"),
                axis=alt.Axis(title="MIC (µg/mL)")),
        color=alt.Color("Gram_Staining:N",
                        scale=alt.Scale(domain=["positive", "negative"],
                                        range=["#4C78A8", "#F58518"]),
                        legend=alt.Legend(title="Gram stain (click to isolate)")),
        tooltip=["Bacteria", "Antibiotic", "MIC", "Gram_Staining"],
        opacity=alt.condition(legend_select, alt.value(1), alt.value(0.15))
    )
    .mark_circle(size=120)
    .add_selection(legend_select)
)

# Annotation highlighting the Gram‑positive Penicillin cluster
ann = pd.DataFrame([
    {"Antibiotic": "Penicillin", "MIC": 0.015,
     "label": "Gram‑positive\nMIC ≤ 0.03 µg/mL"}
])
text = (
    alt.Chart(ann)
    .mark_text(align="left", dx=10, dy=-5, fontSize=12, fontWeight="bold")
    .encode(x="Antibiotic", y="MIC", text="label")
)

chart = (points + text).properties(width=650, height=420)

st.altair_chart(chart, use_container_width=True)

# ────────────────────────────────────────────────────────────────
# Caption (redundant textual encoding)
# ────────────────────────────────────────────────────────────────
st.caption(
    "MIC is log‑scaled—lower values indicate stronger potency. "
    "The annotation shows how Gram‑positive bacteria cluster at sub‑µg/mL Penicillin, "
    "whereas Gram‑negative species require much higher doses."
)
