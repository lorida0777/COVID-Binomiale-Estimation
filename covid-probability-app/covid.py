import pandas as pd
import streamlit as st
import math
import os

# 🔍 Affiche le chemin courant pour vérifier le fichier
st.write("📂 Chemin courant :", os.getcwd())


# 📊 Chargement des données
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Créer le chemin complet vers le fichier CSV
    csv_path = os.path.join(base_dir, "COVID19_symptoms.csv")
    
    df = pd.read_csv(csv_path)

    # Nettoyage de la colonne "Tiredness"
    if df["Tiredness"].dtype == object:
        df["Tiredness"] = df["Tiredness"].map({
            "Yes": 1, "yes": 1,
            "No": 0, "no": 0,
            1: 1, 0: 0
        })

    # Renommer la colonne cible
    df = df.rename(columns={"Covid_Test_Result": "label"})

    # Supprimer les lignes avec des valeurs manquantes
    df = df.dropna(subset=["label"])

    # Conversion du label en entier
    df["label"] = df["label"].astype(int)

    return df

# 🔁 Chargement
df = load_data()

# 🎯 Liste des symptômes
symptoms = ['Fever', 'Dry_Cough', 'Tiredness', 'Sore_Throat',
            'Chest_Pain_Pressure', 'Taste_Smell_Loss', 'Breathing_Problem']

# 📈 Calcul des proba conditionnelles
prob_symptom_given_pos = {}
prob_symptom_given_neg = {}

for s in symptoms:
    # Lissage de Laplace pour éviter les 0 ou 1 parfaits
    pos_count = df[df.label == 1][s].sum()
    neg_count = df[df.label == 0][s].sum()
    total_pos = len(df[df.label == 1])
    total_neg = len(df[df.label == 0])

    prob_symptom_given_pos[s] = (pos_count + 1) / (total_pos + 2)
    prob_symptom_given_neg[s] = (neg_count + 1) / (total_neg + 2)


# Probabilité a priori
p_pos = df["label"].mean()
p_neg = 1 - p_pos

# 💻 Interface utilisateur
st.title("🦠 Estimation COVID-19 avec vos symptômes")
st.markdown("Cochez les symptômes ressentis pour estimer votre risque selon des données réelles.")

# ✅ Formulaire de sélection
user_checks = {s: st.checkbox(s.replace("_", " ")) for s in symptoms}

# 📚 Bayes naïf
log_prior_pos = math.log(p_pos)
log_prior_neg = math.log(p_neg)

log_likelihood_pos = sum(
    math.log(prob_symptom_given_pos[s]) if user_checks[s] else math.log(1 - prob_symptom_given_pos[s])
    for s in symptoms
)

log_likelihood_neg = sum(
    math.log(prob_symptom_given_neg[s]) if user_checks[s] else math.log(1 - prob_symptom_given_neg[s])
    for s in symptoms
)

log_post_pos = log_prior_pos + log_likelihood_pos
log_post_neg = log_prior_neg + log_likelihood_neg

# 🔁 Normalisation (log-softmax)
max_log = max(log_post_pos, log_post_neg)
p1 = math.exp(log_post_pos - max_log)
p0 = math.exp(log_post_neg - max_log)
proba = p1 / (p1 + p0)

# 📊 Résultat
st.subheader("📋 Résultat :")
st.write(f"**Probabilité estimée d’être COVID positif : {proba * 100:.2f}%**")

if proba > 0.5:
    st.warning("⚠️ Risque élevé – test COVID recommandé.")
else:
    st.success("✅ Risque faible – continuez à faire attention.")
