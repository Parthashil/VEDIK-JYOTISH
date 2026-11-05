import streamlit as st
import swisseph as swe
from datetime import datetime
import pytz
import urllib.parse
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

# --- আপনার নিজস্ব সেটিংস ---
MY_UPI_ID = "shil.partha123@axl"  # আপনার সুরক্ষিত UPI ID
MASTER_PIN = "7890"  # এই ৪ সংখ্যার পিনটি আপনি জানবেন, যা টাকা পাওয়ার পর ক্লায়েন্টকে দেবেন
REPORT_PRICE = "199.00"

st.set_page_config(page_title="Astrology & Health Engine", layout="centered")

# --- ভাষা ডিকশনারি ---
TEXTS = {
    "বাংলা": {
        "title": "🔮 বৈদিক, কেপি ও স্বাস্থ্য-জ্যোতিষ বিশ্লেষণ",
        "subtitle": "কুণ্ডলী বিচার, নির্দিষ্ট প্রশ্নের উত্তর, বাস্তু ও প্রতিকার",
        "form_header": "📝 জাতক/জাতিকার জন্ম বিবরণী",
        "name": "পুরো নাম",
        "gender": "লিঙ্গ",
        "gender_opts": ["পুরুষ", "মহিলা"],
        "dob": "জন্মতারিখ",
        "tob": "জন্মসময় (ঘণ্টা:মিনিট)",
        "place": "জন্মস্থান (শহর, রাজ্য যেমন: Kalyani, West Bengal)",
        "q_header": "🎯 আপনার নির্দিষ্ট প্রশ্ন বেছে নিন (ঐচ্ছিক):",
        "q_partner": "আমার জীবনসঙ্গী কেমন ও কোন স্বভাবের হবে?",
        "q_career": "চাকরি, ব্যবসা না স্বপেশা—কোনটি উপযুক্ত?",
        "q_secret_disease": "কোনো গুপ্ত রোগ বা সংবেদনশীল স্বাস্থ্য ঝুঁকি আছে কি?",
        "q_orientation": "সম্পর্কের রুচি বা গভীর মানসিক আকর্ষণ কেমন থাকবে?",
        "submit_btn": "জন্মছক প্রস্তুত করুন",
        "preview_header": "🔍 প্রাথমিক কুণ্ডলী প্রিভিউ",
        "asc": "লগ্ন",
        "moon_sign": "চন্দ্র রাশি",
        "pay_warn": "⚠️ সম্পূর্ণ স্বাস্থ্য, পারিবারিক বিচার, প্রশ্নের উত্তর ও প্রতিকার পেতে নিচে পেমেন্ট সম্পন্ন করুন।",
        "pay_header": "💳 সম্পূর্ণ রিপোর্ট পেতে পেমেন্ট করুন",
        "pin_lbl": "টাকা পাঠানোর পর প্রাপ্ত ৪ সংখ্যার আনলক পিন (PIN) দিন:",
        "unlock_btn": "রিপোর্ট আনলক করুন",
        "success_unlock": "🎉 পেমেন্ট নিশ্চিত হয়েছে! আপনার সম্পূর্ণ রিপোর্ট নিচে প্রস্তুত:",
        "sec_astro": "📊 জ্যোতিষ ও গ্রহীয় অবস্থা",
        "sec_health": "🩺 স্বাস্থ্য, ইন্দ্রিয় ও শারীরিক গঠন",
        "sec_family": "👨‍👩‍👦 পিতা ও মাতা সংক্রান্ত বিচার",
        "sec_queries": "🎯 আপনার নির্দিষ্ট প্রশ্নের উত্তর",
        "sec_vastu": "🏡 মন, বাস্তু ও প্রতিকার নির্দেশিকা",
        "err_place": "স্থানটি খুঁজে পাওয়া যায়নি। সঠিক বানান লিখুন।"
    },
    "English": {
        "title": "🔮 Vedic, KP & Medical Astrology Engine",
        "subtitle": "Birth Chart, Specific Life Queries, Vastu & Remedies",
        "form_header": "📝 Birth Details",
        "name": "Full Name",
        "gender": "Gender",
        "gender_opts": ["Male", "Female"],
        "dob": "Date of Birth",
        "tob": "Time of Birth (HH:MM)",
        "place": "Birth Place (City, State, e.g. Kalyani, West Bengal)",
        "q_header": "🎯 Select Your Specific Inquiries (Optional):",
        "q_partner": "How will my life partner be (Nature & Character)?",
        "q_career": "Career Path: Job, Business, or Self-Employment?",
        "q_secret_disease": "Any indicators of hidden/sensitive health ailments?",
        "q_orientation": "Nature of relationships & psychological bonding?",
        "submit_btn": "Generate Chart Preview",
        "preview_header": "🔍 Basic Chart Preview",
        "asc": "Ascendant (Lagna)",
        "moon_sign": "Moon Sign (Rashi)",
        "pay_warn": "⚠️ To unlock detailed health, parents, answered queries & remedies, please complete payment.",
        "pay_header": "💳 Unlock Full Report via UPI",
        "pin_lbl": "Enter the 4-digit Unlock PIN provided after payment:",
        "unlock_btn": "Unlock Complete Report",
        "success_unlock": "🎉 Payment verified! Your complete report is ready below:",
        "sec_astro": "📊 Planetary & Astrological Positions",
        "sec_health": "🩺 Health, Senses & Bodily Constitution",
        "sec_family": "👨‍👩‍👦 Mother & Father Analysis (Bhavat Bhavam)",
        "sec_queries": "🎯 Answers to Your Selected Questions",
        "sec_vastu": "🏡 Mind, Vastu & Remedial Blueprint",
        "err_place": "Place not found. Please check spelling."
    },
    "हिन्दी": {
        "title": "🔮 वैदिक, केपी एवं स्वास्थ्य-ज्योतिष विश्लेषण",
        "subtitle": "कुंडली फल, विशिष्ट प्रश्नों के उत्तर, वास्तु एवं अचूक उपाय",
        "form_header": "📝 जातक/जातिका का जन्म विवरण",
        "name": "पूरा नाम",
        "gender": "लिंग",
        "gender_opts": ["पुरुष", "महिला"],
        "dob": "जन्म तिथि",
        "tob": "जन्म समय (घंटा:मिनट)",
        "place": "जन्म स्थान (शहर, राज्य जैसे: Kalyani, West Bengal)",
        "q_header": "🎯 अपने विशिष्ट प्रश्न चुनें (वैकल्पिक):",
        "q_partner": "जीवनसाथी का स्वभाव और व्यक्तित्व कैसा रहेगा?",
        "q_career": "आजीविका: नौकरी, व्यापार अथवा स्वतंत्र पेशा?",
        "q_secret_disease": "क्या किसी गुप्त रोग या आंतरिक स्वास्थ्य समस्या की संभावना है?",
        "q_orientation": "संबंधों में आकर्षण एवं मानसिक प्रकृति कैसी रहेगी?",
        "submit_btn": "जन्म चक्र तैयार करें",
        "preview_header": "🔍 प्राथमिक कुंडली पूर्वावलोकन",
        "asc": "लग्न",
        "moon_sign": "चंद्र राशि",
        "pay_warn": "⚠️ संपूर्ण स्वास्थ्य, पितृ-मातृ विश्लेषण, प्रश्नों के उत्तर व उपाय हेतु कृपया नीचे भुगतान करें।",
        "pay_header": "💳 संपूर्ण रिपोर्ट अनलॉक करने के लिए भुगतान करें",
        "pin_lbl": "भुगतान के बाद प्राप्त 4 अंकों का अनलॉक पिन (PIN) दर्ज करें:",
        "unlock_btn": "रिपोर्ट अनलॉक करें",
        "success_unlock": "🎉 भुगतान सत्यापित हुआ! आपकी पूर्ण रिपोर्ट नीचे प्रस्तुत है:",
        "sec_astro": "📊 ज्योतिषीय एवं ग्रहीय स्थिति",
        "sec_health": "🩺 स्वास्थ्य, इंद्रियां एवं शारीरिक रचना",
        "sec_family": "👨‍👩‍👦 माता एवं पिता का विश्लेषण",
        "sec_queries": "🎯 आपके चयनित प्रश्नों के उत्तर",
        "sec_vastu": "🏡 मन, वास्तु एवं सरल उपाय",
        "err_place": "स्थान का विवरण नहीं मिला। कृपया सही नाम दर्ज करें।"
    }
}

selected_lang = st.selectbox("🌐 Select Language / ভাষা নির্বাচন করুন / भाषा चुनें", ["বাংলা", "English", "हिन्दी"])
T = TEXTS[selected_lang]

st.title(T["title"])
st.write(T["subtitle"])

with st.form("astro_form"):
    st.subheader(T["form_header"])
    name = st.text_input(T["name"])
    gender = st.selectbox(T["gender"], T["gender_opts"])
    dob = st.date_input(
    T["dob"],
    value=datetime.date(1990, 1, 1),
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date.today()
)


    tob = st.time_input(T["tob"])
    place = st.text_input(T["place"])

    st.markdown(f"**{T['q_header']}**")
    q_partner = st.checkbox(T["q_partner"])
    q_career = st.checkbox(T["q_career"])
    q_secret = st.checkbox(T["q_secret_disease"])
    q_orient = st.checkbox(T["q_orientation"])

    submitted = st.form_submit_button(T["submit_btn"])

def calculate_chart(dob, tob, place_name):
    geolocator = Nominatim(user_agent="astro_trilingual_engine")
    loc = geolocator.geocode(place_name)
    if not loc:
        return None, T["err_place"]
    lat, lon = loc.latitude, loc.longitude

    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lat=lat, lng=lon) or "Asia/Kolkata"
    local_tz = pytz.timezone(tz_str)

    dt_str = f"{dob} {tob.strftime('%H:%M')}"
    local_dt = local_tz.localize(datetime.strptime(dt_str, "%Y-%m-%d %H:%M"))
    utc_dt = local_dt.astimezone(pytz.utc)

    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
    asc_deg = ascmc[0]
    asc_sign = int(asc_deg // 30) + 1

    planets_map = {
        'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS,
        'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER, 'Venus': swe.VENUS,
        'Saturn': swe.SATURN, 'Rahu': swe.MEAN_NODE
    }

    positions = {'Ascendant': {'deg': asc_deg, 'sign': asc_sign}}
    for p_name, p_id in planets_map.items():
        res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
        deg = res[0]
        positions[p_name] = {'deg': deg, 'sign': int(deg // 30) + 1}

    ketu_deg = (positions['Rahu']['deg'] + 180) % 360
    positions['Ketu'] = {'deg': ketu_deg, 'sign': int(ketu_deg // 30) + 1}

    gulika_deg = (asc_deg + 135) % 360
    positions['Gulika'] = {'deg': gulika_deg, 'sign': int(gulika_deg // 30) + 1}

    return positions, None

def analyze_chart(pos, gender, lang, queries):
    signs = {
        "বাংলা": ["মেষ", "বৃষ", "মিথুন", "কর্কট", "সিংহ", "কন্যা", "তুলা", "বৃশ্চিক", "ধনু", "মকর", "কুম্ভ", "মীন"],
        "English": ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"],
        "हिन्दी": ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"]
    }
    r_list = signs[lang]
    asc = pos['Ascendant']['sign']
    moon = pos['Moon']['sign']
    rep = {}

    rep['asc'] = r_list[asc - 1]
    rep['moon'] = r_list[moon - 1]
    rep['gulika'] = r_list[pos['Gulika']['sign'] - 1]

    if lang == "বাংলা":
        rep['grahan'] = "সূর্য/চন্দ্র রাহুর প্রভাবে গ্রহণ সংক্রান্ত সংবেদনশীলতা রয়েছে।" if abs(pos['Sun']['deg'] - pos['Rahu']['deg']) < 12 or abs(pos['Moon']['deg'] - pos['Rahu']['deg']) < 12 else "কুণ্ডলীতে কোনো প্রত্যক্ষ গ্রহণ দোষ নেই।"
        rep['sadesati'] = "গোচরে শনির অবস্থান সাপেক্ষে সাড়েসাতির সতর্কতা বা প্রভাব বজায় রয়েছে।" if (11 - moon) % 12 in [11, 0, 1] else "বর্তমানে সাড়েসাতি চলছে না।"
        rep['nerve'] = "স্নায়বিক সংবেদনশীলতা ও অনিদ্রা এড়াতে মানসিক বিশ্রাম প্রয়োজন।" if pos['Mercury']['sign'] in [6, 8, 12] else "স্নায়ুতন্ত্র স্থিতিশীল ও কর্মক্ষম।"
        rep['bone'] = "মেরুদণ্ড, অস্থিসন্ধি ও ক্যালসিয়ামের ভারসাম্যে নজর দেওয়া উচিত।" if pos['Sun']['sign'] in [7, 8] or pos['Saturn']['sign'] in [1, 7] else "হাড় ও শারীরিক কাঠামো বলিষ্ঠ।"
        rep['senses'] = "দৃষ্টিশক্তি ও শ্রবণের যত্ন নেওয়া বাঞ্ছনীয়।" if pos['Sun']['sign'] in [2, 12] else "পঞ্চেন্দ্রিয়ের সংবেদনশীলতা স্বাভাবিক।"
        rep['female_health'] = "হরমোনাল ভারসাম্য ও তলপেটের রুটিন চেকআপ প্রয়োজন।" if pos['Mars']['sign'] == 8 or pos['Venus']['sign'] in [6, 8] else "প্রজনন স্বাস্থ্য স্থিতিশীল।"
        rep['mother'] = "মায়ের মন সংবেদনশীল; বাতের ব্যথা ও অনিদ্রার প্রতি যত্ন নেওয়া প্রয়োজন।"
        rep['father'] = "পিতা আত্মসম্মানবোধসম্পন্ন ও দৃঢ় চরিত্রের; অস্থি বা রক্তচাপে নজর দিন।"
        rep['vastu'] = "বাড়ির উত্তর-পূর্ব (ঈশান) ও দক্ষিণ-পূর্ব কোণ পরিষ্কার রাখুন।"
        rep['remedy'] = "প্রতিদিন প্রাতঃসূর্যের আলো নিন, পাখিদের জল দিন এবং ঘরে কর্পূর জ্বালান।"
    elif lang == "English":
        rep['grahan'] = "Eclipse influence detected via Rahu proximity." if abs(pos['Sun']['deg'] - pos['Rahu']['deg']) < 12 or abs(pos['Moon']['deg'] - pos['Rahu']['deg']) < 12 else "No direct eclipse (Grahan) blemish detected."
        rep['sadesati'] = "Saturn's transit indicates ongoing Sade Sati phase." if (11 - moon) % 12 in [11, 0, 1] else "Currently free from Sade Sati phase."
        rep['nerve'] = "Neurological sensitivity and high stress sensitivity detected." if pos['Mercury']['sign'] in [6, 8, 12] else "Nervous system and cognitive balance stable."
        rep['bone'] = "Pay attention to spine, joints, and Vitamin D/Calcium levels." if pos['Sun']['sign'] in [7, 8] or pos['Saturn']['sign'] in [1, 7] else "Skeletal structure and bone density sound."
        rep['senses'] = "Vision or sensory care advised." if pos['Sun']['sign'] in [2, 12] else "Sensory faculties balanced."
        rep['female_health'] = "Hormonal and pelvic sensitivity indicated; routine checkup recommended." if pos['Mars']['sign'] == 8 or pos['Venus']['sign'] in [6, 8] else "Reproductive vitality stable."
        rep['mother'] = "Mother is deeply emotional; joint/sleep issues require care."
        rep['father'] = "Father is authoritative and disciplined; monitor cardiac/bone wellness."
        rep['vastu'] = "Maintain cleanliness in North-East and South-East areas of the home."
        rep['remedy'] = "Offer water to morning Sun, feed birds, and burn camphor in evenings."
    else:
        rep['grahan'] = "सूर्य/चंद्र पर राहु प्रभाव से ग्रहण दोष की संवेदनशीलता है।" if abs(pos['Sun']['deg'] - pos['Rahu']['deg']) < 12 or abs(pos['Moon']['deg'] - pos['Rahu']['deg']) < 12 else "कुंडली में कोई प्रत्यक्ष ग्रहण दोष नहीं है।"
        rep['sadesati'] = "शनि के गोचर अनुसार साढ़ेसाती का प्रभाव वर्तमान में चल रहा है।" if (11 - moon) % 12 in [11, 0, 1] else "वर्तमान समय में साढ़ेसाती का प्रभाव नहीं है।"
        rep['nerve'] = "स्नायु दुर्बलता एवं अत्यधिक तनाव से बचाव आवश्यक है।" if pos['Mercury']['sign'] in [6, 8, 12] else "तंत्रिका तंत्र संतुलित एवं सशक्त है।"
        rep['bone'] = "रीढ़, जोड़ों एवं कैल्शियम की स्थिति पर ध्यान देना श्रेयस्कर है।" if pos['Sun']['sign'] in [7, 8] or pos['Saturn']['sign'] in [1, 7] else "अस्थि संरचना सशक्त है।"
        rep['senses'] = "नेत्र अथवा कान की देखभाल पर ध्यान दें।" if pos['Sun']['sign'] in [2, 12] else "पंचेंद्रियां संतुलित स्थिति में हैं।"
        rep['female_health'] = "हार्मोनल संतुलन एवं आंतरिक स्वास्थ्य की जांच आवश्यक है।" if pos['Mars']['sign'] == 8 or pos['Venus']['sign'] in [6, 8] else "आंतरिक स्वास्थ्य अनुकूल है।"
        rep['mother'] = "माता का स्वभाव भावुक है; जोड़ों के दर्द व नींद पर ध्यान दें।"
        rep['father'] = "पिता स्वाभिमानी एवं अनुशासित हैं; रक्तचाप व अस्थि स्वास्थ्य पर ध्यान दें।"
        rep['vastu'] = "घर का ईशान एवं आग्नेय कोण स्वच्छ व खुला रखें।"
        rep['remedy'] = "प्रातः सूर्य दर्शन करें, पक्षियों को जल दें तथा संध्या समय कपूर जलाएं।"

    answers = {}
    seventh_sign = ((asc + 6) % 12) or 12
    if queries.get('partner'):
        if lang == "বাংলা":
            answers['partner'] = "জীবনসঙ্গী শান্ত, সংবেদনশীল ও পারিবারিক মূল্যবোধসম্পন্ন ব্যক্তিত্বের হবেন।" if seventh_sign in [2, 4, 9, 12] else "জীবনসঙ্গী বাস্তববাদী, আত্মমর্যাদাবান ও স্বাধীনচেতা স্বভাবের হবেন।"
        elif lang == "English":
            answers['partner'] = "Spouse will be gentle, emotionally supportive and family-oriented." if seventh_sign in [2, 4, 9, 12] else "Spouse will be pragmatic, self-directed, and strongly ambitious."
        else:
            answers['partner'] = "जीवनसाथी शांत, संवेदनशील और पारिवारिक मूल्यों का सम्मान करने वाले होंगे।" if seventh_sign in [2, 4, 9, 12] else "जीवनसाथी स्वाभिमानी, व्यावहारिक और स्वतंत्र विचारों वाले होंगे।"

    if queries.get('career'):
        if lang == "বাংলা":
            answers['career'] = "স্বাধীন পেশা (Consultancy/Self-employment) বা ব্যবসার দিকে ভাগ্যোদয় প্রবল।" if pos['Mercury']['sign'] in [10, 7] or pos['Saturn']['sign'] in [10, 11] else "চাকরি বা কোনো স্থায়ী সাংগঠনিক পদে দায়িত্ব পালন অধিক লাভজনক।"
        elif lang == "English":
            answers['career'] = "High potential in independent practice, consultancy, or business." if pos['Mercury']['sign'] in [10, 7] or pos['Saturn']['sign'] in [10, 11] else "Service, organized corporate employment, or administrative roles yield higher stability."
        else:
            answers['career'] = "स्वतंत्र व्यवसाय, परामर्श कार्य अथवा स्वरोजगार में उन्नति के प्रबल योग हैं।" if pos['Mercury']['sign'] in [10, 7] or pos['Saturn']['sign'] in [10, 11] else "स्थिर नौकरी अथवा संगठनात्मक सेवा कार्य अधिक फलदायी रहेगा।"

    if queries.get('secret'):
        if lang == "বাংলা":
            answers['secret'] = "ইউরিনারি বা তলপেটের সংবেদনশীলতায় সতর্কতা রাখুন; জল বেশি পান করুন।" if pos['Rahu']['sign'] == 8 or pos['Mars']['sign'] in [6, 8] else "গুপ্ত রোগ বা অভ্যন্তরীণ জটিলতার নেতিবাচক প্রভাব নেই।"
        elif lang == "English":
            answers['secret'] = "Pelvic or urinary tract vigilance recommended; maintain hydration." if pos['Rahu']['sign'] == 8 or pos['Mars']['sign'] in [6, 8] else "No prominent afflictions pointing to concealed chronic ailments."
        else:
            answers['secret'] = "मूत्र प्रणाली या आंतरिक अंगों के प्रति सावधानी रखें; भरपूर जल ग्रहण करें।" if pos['Rahu']['sign'] == 8 or pos['Mars']['sign'] in [6, 8] else "किसी गंभीर आंतरिक या गुप्त रोग के नकारात्मक योग नहीं हैं।"

    if queries.get('orient'):
        if lang == "বাংলা":
            answers['orient'] = "প্রচলিত ধারণার বাইরে ভিন্নধর্মী রুচি ও গভীর আত্মিক মানসিক যোগাযোগের টান থাকবে।" if pos['Venus']['sign'] in [pos['Mercury']['sign'], pos['Saturn']['sign']] and pos['Rahu']['sign'] in [7, 8] else "সম্পর্কের ক্ষেত্রে ঐতিহ্যগত মূল্যবোধ ও স্বাভাবিক আকর্ষণ বজায় থাকবে।"
        elif lang == "English":
            answers['orient'] = "Inclination towards non-conventional dynamics and profound emotional depth." if pos['Venus']['sign'] in [pos['Mercury']['sign'], pos['Saturn']['sign']] and pos['Rahu']['sign'] in [7, 8] else "Conventional relationship dynamics and harmonious balance observed."
        else:
            answers['orient'] = "पारंपरिक मान्यताओं से हटकर प्रगाढ़ मानसिक जुड़ाव एवं स्वतंत्र सोच की ओर आकर्षण रहेगा।" if pos['Venus']['sign'] in [pos['Mercury']['sign'], pos['Saturn']['sign']] and pos['Rahu']['sign'] in [7, 8] else "संबंधों में परंपरागत संतुलन एवं सौहार्द बना रहेगा।"

    rep['answers'] = answers
    return rep

if submitted:
    st.session_state['ready'] = True
    st.session_state['user_data'] = {
        'name': name, 'gender': gender, 'dob': dob, 'tob': tob, 'place': place,
        'queries': {'partner': q_partner, 'career': q_career, 'secret': q_secret, 'orient': q_orient}
    }

if st.session_state.get('ready'):
    ud = st.session_state['user_data']
    positions, err = calculate_chart(ud['dob'], ud['tob'], ud['place'])
    if err:
        st.error(err)
    else:
        rep = analyze_chart(positions, ud['gender'], selected_lang, ud['queries'])

        st.subheader(T["preview_header"])
        c1, c2 = st.columns(2)
        c1.info(f"**{T['asc']}:** {rep['asc']}")
        c2.info(f"**{T['moon_sign']}:** {rep['moon']}")
        st.warning(T["pay_warn"])

        if not st.session_state.get('paid'):
            st.markdown("---")
            st.subheader(T["pay_header"])
            
            # আপনার কাস্টম UPI ID দিয়ে সরাসরি QR কোড
            upi_url = f"upi://pay?pa={MY_UPI_ID}&pn=AstroConsultancy&am={REPORT_PRICE}&cu=INR&tn=Kundali_Report"
            qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(upi_url)}"

            col1, col2 = st.columns([1, 1])
            with col1:
                st.image(qr_api, caption="GPay / PhonePe / Paytm")
            with col2:
                st.write(f"**Fee:** ₹{REPORT_PRICE}")
                st.write("১. QR কোড স্ক্যান করে পেমেন্ট করুন।")
                st.write("২. টাকা পাঠানোর পর আমাদের কাছ থেকে প্রাপ্ত ৪ সংখ্যার পিনটি নিচে বসান।")
                
                input_pin = st.text_input(T["pin_lbl"], type="password")
                if st.button(T["unlock_btn"]):
                    if input_pin == MASTER_PIN:
                        st.session_state['paid'] = True
                        st.success(T["success_unlock"])
                        st.rerun()
                    else:
                        st.error("ভুল পিন! সঠিক পিন পেতে পেমেন্টের স্ক্রিনশট পাঠিয়ে যোগাযোগ করুন।")

        if st.session_state.get('paid'):
            st.success(T["success_unlock"])

            st.markdown(f"### {T['sec_astro']}")
            st.write(f"• **Gulika:** {rep['gulika']}")
            st.write(f"• **Sade Sati:** {rep['sadesati']}")
            st.write(f"• **Eclipse (Grahan):** {rep['grahan']}")

            st.markdown(f"### {T['sec_health']}")
            st.write(f"• **Nerves:** {rep['nerve']}")
            st.write(f"• **Bones:** {rep['bone']}")
            st.write(f"• **Senses:** {rep['senses']}")
            if ud['gender'] in ["মহিলা", "Female"]:
                st.write(f"• **Internal/Pelvic Health:** {rep['female_health']}")

            st.markdown(f"### {T['sec_family']}")
            st.write(f"• **Mother:** {rep['mother']}")
            st.write(f"• **Father:** {rep['father']}")

            if rep['answers']:
                st.markdown(f"### {T['sec_queries']}")
                for k, ans in rep['answers'].items():
                    st.write(f"• {ans}")

            st.markdown(f"### {T['sec_vastu']}")
            st.write(f"• **Vastu:** {rep['vastu']}")
            st.write(f"• **Remedies:** {rep['remedy']}")
