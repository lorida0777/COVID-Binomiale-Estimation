
# 🦠 Estimation de Probabilité COVID-19 à partir de Symptômes

Ce projet permet à un utilisateur de cocher des symptômes cliniques et d'obtenir une estimation de la probabilité d'être atteint du COVID-19, à l'aide d'un modèle probabiliste basé sur la loi de Bayes.

---

## 📌 Objectif

Estimer la probabilité d'infection COVID-19 en fonction des symptômes renseignés par l'utilisateur, selon les données d'observation issues d'un dataset réel.

---

## 📊 Données utilisées

- **Source** : [Mendeley Data - COVID19 Symptoms Dataset](https://data.mendeley.com/datasets/4ddz9385xp/1)
- **Colonnes importantes** :
  - `Fever`, `Dry_Cough`, `Tiredness`, `Sore_Throat`, `Chest_Pain_Pressure`, `Taste_Smell_Loss`, `Breathing_Problem`
  - `Covid_Test_Result` (0 = Négatif, 1 = Positif)

---

## 🧠 Méthode utilisée

- **Modèle :** Naive Bayes binaire
- **Principe :**
  - Chaque symptôme est une variable binaire (présent ou absent).
  - Estimation de :
    \[
    P(\text{COVID} \mid \text{symptômes}) = \frac{P(\text{symptômes} \mid \text{COVID}) \cdot P(\text{COVID})}{P(\text{symptômes})}
    \]
  - Hypothèse d’indépendance entre les symptômes (Naive Bayes)
  - Lissage de Laplace appliqué pour éviter `log(0)`

---

## 🚀 Utilisation

### 1. Prérequis

Installez les bibliothèques nécessaires :

```bash
pip install streamlit pandas
````

### 2. Lancer l’application

```bash
streamlit run covid.py
```

### 3. Interface utilisateur

* Cochez les symptômes que vous ressentez.
* Le système calcule la probabilité d’être COVID positif.
* Un message vous informe du risque estimé.

---

## 📁 Arborescence du projet

```
covid-probability-app/
├── covid.py               # Code principal de l'application Streamlit
├── COVID19_symptoms.csv   # Fichier de données depuis Mendeley
└── README.md              # Ce fichier d'explication
```

---

## ✍️ Auteur

* **Nom :** \[ANDRIATSIFERANA No Kanto Lorida]
* **Projet académique :** Estimation probabiliste avec la loi de Bayes
* **Langage :** Python + Streamlit

