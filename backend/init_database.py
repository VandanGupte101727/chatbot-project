from database import SessionLocal, FAQ, Base, engine
import csv 
import os 

def initialize_sample_data():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Sample FAQs data
    sample_faqs = [
        {
            "question": "fee deadline",
            "answer_en": "The fee deadline for the current semester is September 30, 2024. Late submissions will incur a penalty of ₹100 per day.",
            "answer_hi": "वर्तमान सेमेस्टर के लिए फीस की अंतिम तिथि 30 सितंबर, 2024 है। देर से जमा करने पर ₹100 प्रतिदिन का जुर्माना लगेगा।",
            "answer_ta": "தற்போதைய செமஸ்டருக்கான கட்டண காலக்கெடு செப்டம்பர் 30, 2024. தாமதமாக சமர்ப்பிப்பதற்கு ஒரு நாளைக்கு ₹100 அபராதம் விதிக்கப்படும்.",
            "answer_te": "ప్రస్తుత సెమిస్టర్ కోసం ఫీజు గడువు సెప్టెంబర్ 30, 2024. ఆలస్యం సమర్పణలపై రోజుకు ₹100 పెనాల్టీ విధించబడుతుంది.",
            "answer_ml": "ഇപ്പോഴത്തെ സെമസ്റ്ററിനായുള്ള ഫീസ് ഡെഡ്ലൈൻ സെപ്റ്റംബർ 30, 2024 ആണ്. വൈകി സമർപ്പിക്കുന്നതിന് ദിവസം ₹100 പിഴ ഈടാക്കും.",
            "intent": "fee_deadline",
            "category": "fees"
        },
        {
            "question": "scholarship form",
            "answer_en": "Scholarship forms are available in the student portal under the 'Financial Aid' section. The deadline is October 15, 2024.",
            "answer_hi": "छात्रवृत्ति फॉर्म छात्र पोर्टल के 'वित्तीय सहायता' खंड में उपलब्ध हैं। अंतिम तिथि 15 अक्टूबर, 2024 है।",
            "answer_ta": "பள்ளிப் படிப்புதவி படிவங்கள் மாணவர் போர்ட்டலில் 'நிதியுதவி' பிரிவில் கிடைக்கின்றன. கடைசி நாள் அக்டோபர் 15, 2024.",
            "answer_te": "స్కాలర్షిప్ ఫారమ్లు 'ఫైనాన్షియల్ ఎయిడ్' విభాగంలోని విద్యార్థి పోర్టల్లో లభిస్తాయి. గడువు అక్టోబర్ 15, 2024.",
            "answer_ml": "സ്കോളർഷിപ്പ് ഫോമുകൾ വിദ്യാർത്ഥി പോർട്ടലിലെ 'ഫിനാൻഷ്യൽ എയ്ഡ്' വിഭാഗത്തിൽ ലഭ്യമാണ്. അവസാന തീയതി ഒക്ടോബർ 15, 2024.",
            "intent": "scholarship_form",
            "category": "scholarship"
        }
    ]
    
    for faq_data in sample_faqs:
        existing_faq = db.query(FAQ).filter(FAQ.intent == faq_data["intent"]).first()
        if not existing_faq:
            faq = FAQ(**faq_data)
            db.add(faq)
    
    db.commit()
    db.close()
    print("✅ Database initialized with sample data!")

if __name__ == "__main__":
    initialize_sample_data()