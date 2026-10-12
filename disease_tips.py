"""Treatment / prevention tips. Matching is by keyword in the class name
(e.g. 'Tomato___Late_blight' matches 'late blight')."""

TIPS = {
    "healthy": {
        "cause": "No disease detected.",
        "tips": ["Keep monitoring leaves weekly.",
                 "Maintain balanced fertilizer and proper watering.",
                 "Ensure good spacing and airflow between plants."],
    },
    "late blight": {
        "cause": "Fungus-like pathogen (Phytophthora infestans); spreads in cool, wet weather.",
        "tips": ["Remove and destroy infected plants/leaves immediately.",
                 "Avoid overhead watering; water at the base in the morning.",
                 "Apply a recommended fungicide (copper-based or mancozeb) as per label.",
                 "Rotate crops; do not plant potato/tomato in the same spot next season."],
    },
    "early blight": {
        "cause": "Fungus (Alternaria solani); causes dark rings on older leaves.",
        "tips": ["Remove lower infected leaves.",
                 "Mulch to stop soil splash onto leaves.",
                 "Spray fungicide (chlorothalonil / copper) at first signs.",
                 "Practise 2-3 year crop rotation."],
    },
    "bacterial spot": {
        "cause": "Bacteria (Xanthomonas); spread by rain splash and infected seed.",
        "tips": ["Use disease-free certified seed.",
                 "Spray copper-based bactericide.",
                 "Avoid working in the field when plants are wet.",
                 "Remove crop debris after harvest."],
    },
    "leaf mold": {
        "cause": "Fungus (Passalora fulva); thrives in high humidity.",
        "tips": ["Improve ventilation and reduce humidity.",
                 "Avoid wetting leaves; space plants wider.",
                 "Apply a suitable fungicide if severe.",
                 "Use resistant varieties."],
    },
    "septoria": {
        "cause": "Fungus (Septoria lycopersici); small round spots with dark borders.",
        "tips": ["Remove infected lower leaves.",
                 "Mulch and water at the base.",
                 "Apply fungicide (chlorothalonil / copper).",
                 "Rotate crops and clean up debris."],
    },
    "spider mite": {
        "cause": "Two-spotted spider mites; common in hot, dry conditions.",
        "tips": ["Spray plants with strong water jets to dislodge mites.",
                 "Use neem oil or insecticidal soap.",
                 "Introduce natural predators (predatory mites, ladybugs).",
                 "Avoid dusty, water-stressed conditions."],
    },
    "target spot": {
        "cause": "Fungus (Corynespora cassiicola).",
        "tips": ["Prune to improve airflow.",
                 "Apply fungicide as recommended.",
                 "Remove infected plant debris."],
    },
    "yellow leaf curl": {
        "cause": "Tomato yellow leaf curl virus, spread by whiteflies.",
        "tips": ["Control whiteflies (yellow sticky traps, neem oil).",
                 "Remove and destroy infected plants (no cure for virus).",
                 "Use virus-resistant varieties and insect-proof nets in nurseries."],
    },
    "mosaic virus": {
        "cause": "Viral disease spread by contact, tools and aphids.",
        "tips": ["Remove and destroy infected plants.",
                 "Disinfect tools and wash hands after handling plants.",
                 "Control aphids and weeds.",
                 "Plant resistant varieties."],
    },
    "scab": {
        "cause": "Fungus (Venturia inaequalis).",
        "tips": ["Rake and destroy fallen leaves.",
                 "Prune for airflow.",
                 "Apply fungicide at bud break through petal fall.",
                 "Choose scab-resistant varieties."],
    },
    "black rot": {
        "cause": "Fungal disease (Botryosphaeria / Guignardia).",
        "tips": ["Prune out infected branches, mummified fruit and cankers.",
                 "Apply fungicide before and after bloom.",
                 "Keep orchard/vineyard floor clean."],
    },
    "cedar apple rust": {
        "cause": "Fungus needing both apple and juniper/cedar hosts.",
        "tips": ["Remove nearby juniper/cedar if possible.",
                 "Apply fungicide in spring.",
                 "Plant rust-resistant apple varieties."],
    },
    "powdery mildew": {
        "cause": "Fungal disease forming white powder on leaves.",
        "tips": ["Improve air circulation; avoid excess nitrogen.",
                 "Spray sulfur-based fungicide or potassium bicarbonate.",
                 "Remove heavily infected leaves."],
    },
    "gray leaf spot": {
        "cause": "Fungus (Cercospora zeae-maydis); favors warm, humid weather.",
        "tips": ["Rotate crops and till residue.",
                 "Plant resistant hybrids.",
                 "Apply fungicide at early tasseling if pressure is high."],
    },
    "cercospora": {
        "cause": "Fungus (Cercospora); leaf spot disease.",
        "tips": ["Rotate crops and till residue.",
                 "Use resistant hybrids.",
                 "Apply fungicide if severe."],
    },
    "common rust": {
        "cause": "Fungus (Puccinia sorghi); rusty pustules on leaves.",
        "tips": ["Plant resistant hybrids.",
                 "Apply fungicide early if infection is heavy.",
                 "Avoid late planting."],
    },
    "northern leaf blight": {
        "cause": "Fungus (Exserohilum turcicum); long gray-green lesions.",
        "tips": ["Use resistant hybrids.",
                 "Rotate crops and bury residue.",
                 "Apply foliar fungicide if disease appears before tasseling."],
    },
    "leaf scorch": {
        "cause": "Fungal (Diplocarpon) or environmental stress.",
        "tips": ["Remove infected leaves.",
                 "Water at the base; avoid drought stress.",
                 "Apply fungicide if fungal."],
    },
    "haunglongbing": {
        "cause": "Citrus greening (bacteria spread by psyllids); no cure.",
        "tips": ["Remove infected trees to protect others.",
                 "Control Asian citrus psyllid.",
                 "Use certified disease-free nursery plants.",
                 "Contact your local agriculture department."],
    },
    "citrus greening": {
        "cause": "Bacterial disease spread by psyllids; no cure.",
        "tips": ["Remove infected trees.", "Control psyllids.",
                 "Use certified clean planting material."],
    },
    "esca": {
        "cause": "Fungal trunk disease complex ('black measles') of grapes.",
        "tips": ["Prune in dry weather and seal large cuts.",
                 "Remove and burn infected wood.",
                 "Avoid vine stress."],
    },
    "leaf blight": {
        "cause": "Fungal leaf blight.",
        "tips": ["Remove infected leaves.",
                 "Apply copper-based fungicide.",
                 "Improve spacing and airflow."],
    },
    "blast": {
        "cause": "Fungus (Magnaporthe oryzae), serious in rice.",
        "tips": ["Use resistant varieties.",
                 "Avoid excess nitrogen.",
                 "Apply tricyclazole-type fungicide as per local advice."],
    },
    "brown spot": {
        "cause": "Fungus (Bipolaris oryzae); often linked to nutrient-poor soil.",
        "tips": ["Balance fertilizer (potassium, silicon).",
                 "Use treated seed.",
                 "Apply fungicide if severe."],
    },
    "rust": {
        "cause": "Fungal rust disease.",
        "tips": ["Remove infected leaves.",
                 "Apply fungicide early.",
                 "Plant resistant varieties."],
    },
}

GENERIC = {
    "cause": "Disease identified, but no specific advice is stored for it.",
    "tips": ["Isolate affected plants and remove badly infected leaves.",
             "Avoid overhead watering; keep leaves dry.",
             "Consult your local agriculture extension officer / KVK for the right treatment.",
             "Always follow pesticide label directions."],
}


def pretty(class_name: str):
    """'Tomato___Late_blight' -> ('Tomato', 'Late blight')"""
    parts = class_name.replace("__", "_").split("_")
    if "___" in class_name:
        crop, disease = class_name.split("___", 1)
    else:
        crop, disease = (parts[0], " ".join(parts[1:])) if len(parts) > 1 else ("", class_name)
    return crop.replace("_", " ").strip(), disease.replace("_", " ").strip()


def get_tips(class_name: str):
    name = class_name.lower().replace("_", " ")
    if "healthy" in name:
        return TIPS["healthy"]
    # longest keyword first so 'northern leaf blight' beats 'leaf blight'
    for key in sorted(TIPS, key=len, reverse=True):
        if key != "healthy" and key in name:
            return TIPS[key]
    return GENERIC
