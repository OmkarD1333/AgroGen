import os
from typing import Dict, Any
from app.config import settings

GEMINI_API_KEY = settings.gemini_api_key or os.getenv("GEMINI_API_KEY", "")


def answer_farmer_query(query: str, language: str = "mr") -> str:
    """
    Generate bilingual farming advice using Gemini or agricultural knowledge rules.
    """
    if GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            prompt = (
                f"You are AgroGen AI, an expert agricultural advisory assistant for farmers in Maharashtra, India. "
                f"Answer the following question clearly and practically in language: {language}.\n\n"
                f"Question: {query}"
            )
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")

    # Fallback contextual replies
    q_lower = query.lower()
    if "खत" in query or "fertilizer" in q_lower:
        if language == "mr":
            return "पिकासाठी नत्र, स्फुरद आणि पालाश (NPK) योग्य प्रमाणात द्या. पेरणीच्या वेळी डीएपी किंवा १०:२६:२६ चा वापर फायदेशीर ठरतो."
        return "Apply balanced NPK fertilization. During sowing, DAP or 10:26:26 provides essential early nutrients."
    elif "रोग" in query or "कीड" in query or "pest" in q_lower or "disease" in q_lower:
        if language == "mr":
            return "कीड व रोग नियंत्रणासाठी पहिल्यांदा निंबोळी अर्क ५% फवारा. तीव्र प्रादुर्भाव असल्यास तज्ञांच्या सल्ल्याने कीटकनाशक वापरा."
        return "For pest control, start with 5% neem extract. In case of severe infestation, use recommended systemic pesticides."
    else:
        if language == "mr":
            return "नमस्कार! मी अ‍ॅग्रोजेन एआय कृषी सल्लागार आहे. आपण पीक व्यवस्थापन, खते, रोग किंवा बाजारभावाबाबत प्रश्न विचारू शकता."
        return "Hello! I am AgroGen AI Agricultural Assistant. You can ask me about crop management, fertilizers, diseases, and market rates."
