import streamlit as st
import spacy
import subprocess

# ---- Set Streamlit Page Config FIRST ----
st.set_page_config(page_title="HealthBot 🩺", layout="centered")

# ---- Load spaCy Model with Safe Fallback ----
def load_spacy_model(model_name="en_core_web_sm"):
    try:
        return spacy.load(model_name)
    except OSError:
        st.warning(f"spaCy model '{model_name}' not found. Downloading...")
        subprocess.run(["python", "-m", "spacy", "download", model_name], check=True)
        return spacy.load(model_name)

nlp = load_spacy_model()

# ---- Dummy Symptom Database ----
SYMPTOMS_DB = {
    "fever": {
        "precautions": ["Drink fluids", "Rest well"],
        "medicines": ["Paracetamol"],
        "tips": ["Avoid cold drinks", "Monitor temperature"]
    },
    "cough": {
        "precautions": ["Stay hydrated", "Use a humidifier"],
        "medicines": ["Cough syrup"],
        "tips": ["Avoid allergens", "Use lozenges"]
    },
    "headache": {
        "precautions": ["Rest in a quiet room", "Drink water"],
        "medicines": ["Ibuprofen", "Paracetamol"],
        "tips": ["Avoid screen time", "Apply cold compress"]
    },
    "cold": {
        "precautions": ["Stay warm", "Drink hot fluids"],
        "medicines": ["Antihistamines"],
        "tips": ["Use saline drops", "Rest well"]
    },
    "sore throat": {
        "precautions": ["Gargle with salt water", "Avoid spicy food"],
        "medicines": ["Lozenges"],
        "tips": ["Drink warm liquids", "Use humidifier"]
    },
    "fatigue": {
        "precautions": ["Get enough sleep", "Reduce stress"],
        "medicines": ["Vitamin supplements"],
        "tips": ["Take short naps", "Eat balanced meals"]
    },
    "nausea": {
        "precautions": ["Eat light meals", "Avoid strong odors"],
        "medicines": ["Antiemetics"],
        "tips": ["Sip ginger tea", "Rest after eating"]
    },
    "vomiting": {
        "precautions": ["Stay hydrated", "Avoid solid foods initially"],
        "medicines": ["Antiemetics"],
        "tips": ["Eat bland foods", "Rest"]
    },
    "diarrhea": {
        "precautions": ["Drink oral rehydration solution", "Avoid dairy"],
        "medicines": ["ORS", "Loperamide"],
        "tips": ["Eat bananas", "Avoid spicy foods"]
    },
    "constipation": {
        "precautions": ["Increase fiber intake", "Drink more water"],
        "medicines": ["Laxatives"],
        "tips": ["Exercise regularly", "Eat fruits"]
    },
    "back pain": {
        "precautions": ["Use proper posture", "Avoid heavy lifting"],
        "medicines": ["Pain relievers"],
        "tips": ["Apply heat/cold", "Do stretching exercises"]
    },
    "chest pain": {
        "precautions": ["Rest", "Avoid exertion"],
        "medicines": ["Aspirin (if prescribed)"],
        "tips": ["Seek medical help if severe", "Monitor symptoms"]
    },
    "shortness of breath": {
        "precautions": ["Sit upright", "Avoid allergens"],
        "medicines": ["Inhalers"],
        "tips": ["Practice deep breathing", "Seek medical help if severe"]
    },
    "rash": {
        "precautions": ["Avoid scratching", "Keep area clean"],
        "medicines": ["Antihistamines", "Topical creams"],
        "tips": ["Use moisturizer", "Wear loose clothing"]
    },
    "dizziness": {
        "precautions": ["Sit or lie down", "Avoid sudden movements"],
        "medicines": ["Meclizine"],
        "tips": ["Drink water", "Rest"]
    },
    "runny nose": {
        "precautions": ["Use tissues", "Wash hands frequently"],
        "medicines": ["Decongestants"],
        "tips": ["Use saline spray", "Stay hydrated"]
    },
    "sneezing": {
        "precautions": ["Avoid allergens", "Use tissues"],
        "medicines": ["Antihistamines"],
        "tips": ["Keep windows closed", "Clean your room"]
    },
    "body ache": {
        "precautions": ["Rest", "Stay hydrated"],
        "medicines": ["Pain relievers"],
        "tips": ["Warm bath", "Gentle stretching"]
    },
    "loss of appetite": {
        "precautions": ["Eat small meals", "Avoid oily foods"],
        "medicines": ["Appetite stimulants (if prescribed)"],
        "tips": ["Eat favorite foods", "Drink juices"]
    },
    "sweating": {
        "precautions": ["Wear light clothes", "Stay cool"],
        "medicines": ["Antiperspirants"],
        "tips": ["Drink water", "Avoid spicy foods"]
    },
    "chills": {
        "precautions": ["Keep warm", "Rest"],
        "medicines": ["Paracetamol"],
        "tips": ["Drink warm fluids", "Monitor temperature"]
    },
    "itching": {
        "precautions": ["Avoid scratching", "Keep skin moisturized"],
        "medicines": ["Antihistamines", "Topical creams"],
        "tips": ["Use cool compress", "Wear cotton clothes"]
    },
    "joint pain": {
        "precautions": ["Rest joints", "Apply ice"],
        "medicines": ["Pain relievers"],
        "tips": ["Gentle exercise", "Stretching"]
    },
    "abdominal pain": {
        "precautions": ["Eat light meals", "Avoid spicy foods"],
        "medicines": ["Antacids", "Pain relievers"],
        "tips": ["Warm compress", "Rest"]
    },
    "sensitivity to light": {
        "precautions": ["Wear sunglasses", "Stay indoors"],
        "medicines": ["Pain relievers"],
        "tips": ["Dim lights", "Rest eyes"]
    },
    "ear pain": {
        "precautions": ["Avoid loud noises", "Keep ears dry"],
        "medicines": ["Pain relievers", "Ear drops"],
        "tips": ["Warm compress", "See a doctor if severe"]
    },
    "eye redness": {
        "precautions": ["Avoid touching eyes", "Use clean towels"],
        "medicines": ["Eye drops"],
        "tips": ["Cold compress", "Rest eyes"]
    },
    "swelling": {
        "precautions": ["Elevate affected area", "Apply ice"],
        "medicines": ["Anti-inflammatories"],
        "tips": ["Rest", "Monitor swelling"]
    },
    "palpitations": {
        "precautions": ["Avoid caffeine", "Practice relaxation"],
        "medicines": ["Beta blockers (if prescribed)"],
        "tips": ["Deep breathing", "Monitor heart rate"]
    }
}

# ---- Symptom Analyzer ----
def analyze_symptoms(text):
    text = text.lower()
    words = set(text.split())
    results = {"precautions": set(), "medicines": set(), "tips": set()}
    for symptom in SYMPTOMS_DB:
        symptom_words = set(symptom.split())
        # Match if all symptom words are in input, or any single word matches
        if symptom in text or symptom_words & words:
            data = SYMPTOMS_DB[symptom]
            results["precautions"].update(data["precautions"])
            results["medicines"].update(data["medicines"])
            results["tips"].update(data["tips"])
    return results

# ---- Streamlit UI ----
st.title("🩺 HealthBot - Symptom Checker")

st.subheader("Enter your symptoms (e.g., 'I have fever and cough')")
user_input = st.text_area("Symptoms")
severity = st.selectbox("Select severity", ["Mild", "Moderate", "Severe"])

if st.button("Analyze"):
    if user_input.strip():
        result = analyze_symptoms(user_input)
        if severity == "Severe":
            st.warning("Your symptoms are severe. Please consult a doctor immediately.")

        st.success("✅ Analysis Complete")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 🛡️ Precautions")
            for item in sorted(result["precautions"]):
                st.markdown(f"- {item}")
        with col2:
            st.markdown("### 💊 Medicines")
            for item in sorted(result["medicines"]):
                st.markdown(f"- {item}")
        with col3:
            st.markdown("### 💡 Tips")
            for item in sorted(result["tips"]):
                st.markdown(f"- {item}")
    else:
        st.error("Please enter some symptoms.")