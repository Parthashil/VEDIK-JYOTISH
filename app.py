import streamlit as st
import swisseph as swe
from datetime import datetime, date

import pytz
import urllib.parse
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

# --- আপনার নিজস্ব সেটিংস ---
MY_UPI_ID = "shil.partha123@axl"
PIN_21 = "2121"      # ২১ টাকার প্যাকের পিন
PIN_51 = "5151"      # ৫১ টাকার পূর্ণাঙ্গ রিপোর্টের পিন
PRICE_BASIC = "21.00"
PRICE_PRO = "51.00"

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
    min_value=date(1900, 1, 1)
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
    geolocator = Nominatim(user_agent="astro_vedik_shil_app", timeout=15)
    try:
        loc = geolocator.geocode(place_name)
    except Exception:
        loc = None

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

    positions = {'Ascendant': {'deg': asc_deg, 'sign': asc_sign, 'retro': False}}
    for p_name, p_id in planets_map.items():
        res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
        deg = res[0]
        speed = res[3]
        positions[p_name] = {
            'deg': deg,
            'sign': int(deg // 30) + 1,
            'retro': True if speed < 0 and p_name not in ['Rahu'] else False
        }

    ketu_deg = (positions['Rahu']['deg'] + 180) % 360
    positions['Ketu'] = {'deg': ketu_deg, 'sign': int(ketu_deg // 30) + 1, 'retro': True}

    gulika_deg = (asc_deg + 135) % 360
    positions['Gulika'] = {'deg': gulika_deg, 'sign': int(gulika_deg // 30) + 1, 'retro': False}

    # আজকের গোচর (Daily Transit) গণনা
    now_utc = datetime.now(pytz.utc)
    jd_now = swe.julday(now_utc.year, now_utc.month, now_utc.day, now_utc.hour + now_utc.minute / 60.0)
    moon_now_res, _ = swe.calc_ut(jd_now, swe.MOON, swe.FLG_SIDEREAL)
    transit_moon_deg = moon_now_res[0]

    return {'planets': positions, 'cusps': cusps, 'jd': jd, 'transit_moon': transit_moon_deg}, None


# --- সহায়ক ফাংশন: ডিগ্রি, নক্ষত্র, কেপি সাব-লর্ড ও দশা ---
NAK_NAMES = [
    "অশ্বিনী", "ভরণী", "কৃত্তিকা", "রোহিণী", "মৃগশিরা", "আর্দ্রা", "পুনর্বসু", "পুষ্যা", "অশ্লেষা",
    "মঘা", "পূর্বফল্গুনী", "উত্তরফল্গুনী", "হস্তা", "চিত্রা", "স্বাতী", "বিশাখা", "অনুরাধা", "জ্যেষ্ঠা",
    "মূলা", "পূর্বাষাঢ়া", "উত্তরাষাঢ়া", "শ্রবণা", "ধনিষ্ঠা", "শতভিষা", "পূর্বভাদ্রপদ", "উত্তরভাদ্রপদ", "রেবতী"
]
VIM_LORDS = ["কেতু", "শুক্র", "রবি", "চন্দ্র", "মঙ্গল", "রাহু", "বৃহস্পতি", "শনি", "বুধ"]
VIM_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

def get_kp_details(deg):
    deg = deg % 360
    nak_span = 360.0 / 27.0  # 13°20'
    nak_idx = int(deg // nak_span)
    nak_name = NAK_NAMES[nak_idx]
    star_lord_idx = nak_idx % 9
    star_lord = VIM_LORDS[star_lord_idx]

    # KP Sub-lord হিসাব
    rem_in_nak = deg - (nak_idx * nak_span)
    curr = 0.0
    sub_lord = star_lord
    for i in range(9):
        idx = (star_lord_idx + i) % 9
        span = (VIM_YEARS[idx] / 120.0) * nak_span
        if curr <= rem_in_nak < curr + span:
            sub_lord = VIM_LORDS[idx]
            break
        curr += span

    deg_in_sign = deg % 30
    d = int(deg_in_sign)
    m = int((deg_in_sign - d) * 60)
    s = int(((deg_in_sign - d) * 60 - m) * 60)
    dms = f"{d:02d}° {m:02d}' {s:02d}\""
    return dms, nak_name, star_lord, sub_lord, nak_idx

def get_vimshottari_current(moon_deg, dob):
    nak_span = 360.0 / 27.0
    nak_idx = int(moon_deg // nak_span)
    start_idx = nak_idx % 9
    rem_frac = 1.0 - ((moon_deg % nak_span) / nak_span)
    
    age_years = (date.today() - dob).days / 365.25
    elapsed = 0.0
    first_bal = VIM_YEARS[start_idx] * rem_frac
    
    if age_years < first_bal:
        maha_idx = start_idx
        rem_maha = first_bal - age_years
    else:
        elapsed = first_bal
        maha_idx = start_idx
        for i in range(1, 18):
            idx = (start_idx + i) % 9
            if elapsed + VIM_YEARS[idx] > age_years:
                maha_idx = idx
                rem_maha = (elapsed + VIM_YEARS[idx]) - age_years
                break
            elapsed += VIM_YEARS[idx]
    return VIM_LORDS[start_idx], VIM_LORDS[maha_idx], round(rem_maha, 1)


def analyze_chart(chart_data, dob, gender, lang, queries):
    pos = chart_data['planets']
    cusps = chart_data['cusps']
    t_moon = chart_data['transit_moon']

    signs = {
        "বাংলা": ["মেষ", "বৃষ", "মিথুন", "কর্কট", "সিংহ", "কন্যা", "তুলা", "বৃশ্চিক", "ধনু", "মকর", "কুম্ভ", "মীন"],
        "English": ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"],
        "हिन्दी": ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"]
    }
    p_bn = {
        'Ascendant': 'লগ্ন', 'Sun': 'রবি', 'Moon': 'চন্দ্র', 'Mars': 'মঙ্গল',
        'Mercury': 'বুধ', 'Jupiter': 'বৃহস্পতি', 'Venus': 'শুক্র',
        'Saturn': 'শনি', 'Rahu': 'রাহু', 'Ketu': 'কেতু', 'Gulika': 'গুলিক'
    }
    r_list = signs.get(lang, signs["বাংলা"])
    asc = pos['Ascendant']['sign']
    moon = pos['Moon']['sign']
    rep = {}

    _, moon_nak, _, _, birth_nak_idx = get_kp_details(pos['Moon']['deg'])
    rep['asc'] = r_list[asc - 1]
    rep['moon'] = r_list[moon - 1]
    rep['moon_nak'] = moon_nak
    rep['gulika'] = r_list[pos['Gulika']['sign'] - 1]

    # গ্রহস্ফুট টেবিল তৈরি
    planet_rows = []
    for p_key in ['Ascendant', 'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
        p_info = pos[p_key]
        dms, nak, star_l, sub_l, _ = get_kp_details(p_info['deg'])
        retro_tag = " (বক্রী)" if p_info['retro'] else ""
        planet_rows.append({
            "গ্রহ": p_bn[p_key] + retro_tag,
            "রাশি": r_list[p_info['sign'] - 1],
            "ডিগ্রি": dms,
            "নক্ষত্র": nak,
            "নক্ষত্রাধিপতি": star_l,
            "সাব-লর্ড (KP)": sub_l
        })
    rep['planet_table'] = planet_rows

    # ১২টি ভাবের KP Cuspal টেবিল
    cusp_rows = []
    for i in range(12):
        c_deg = cusps[i]
        c_sign = int(c_deg // 30) + 1
        dms, nak, star_l, sub_l, _ = get_kp_details(c_deg)
        cusp_rows.append({
            "ভাব": f"{i+1}ম ভাব",
            "রাশি": r_list[c_sign - 1],
            "কাস্প ডিগ্রি": dms,
            "নক্ষত্রাধিপতি": star_l,
            "সাব-লর্ড (KP)": sub_l
        })
    rep['cusp_table'] = cusp_rows

    # বিংশোত্তরী দশা
    birth_dasha, curr_dasha, rem_yrs = get_vimshottari_current(pos['Moon']['deg'], dob)
    rep['dasha_info'] = f"জন্মকালীন মহাদশা: **{birth_dasha}** | বর্তমান চলমান মহাদশা: **{curr_dasha}** (আরও প্রায় {rem_yrs} বছর অবশিষ্ট)"

    # প্রতিদিনের গোচর ফলাফল (তারাশুদ্ধি ও চন্দ্র গোচর)
    _, t_nak, _, _, t_nak_idx = get_kp_details(t_moon)
    t_moon_sign = int(t_moon // 30) + 1
    tara_num = ((t_nak_idx - birth_nak_idx) % 27) % 9 + 1
    tara_map = {
        1: ("জন্ম তারা", "মিশ্র ফল — শরীর ও মনের যত্ন নিন, তাড়াহুড়ো করবেন না।"),
        2: ("সম্পদ তারা", "অত্যন্ত শুভ — অর্থলাভ, নতুন পরিকল্পনা ও কাজের সাফল্যের দিন।"),
        3: ("বিপদ তারা", "সতর্কতা প্রয়োজন — বিতর্ক, ঝুঁকিপূর্ণ বিনিয়োগ ও ভ্রমণে সাবধান থাকুন।"),
        4: ("ক্ষেম তারা", "শুভ দিন — মানসিক শান্তি, পারিবারিক সুখ ও আটকে থাকা কাজ সম্পন্ন হবে।"),
        5: ("প্রত্যারি তারা", "বাধা-বিপত্তির যোগ — অকারণ দুশ্চিন্তা এড়িয়ে ধৈর্য ধরুন।"),
        6: ("সাধক তারা", "কর্মসিদ্ধির দিন — প্রচেষ্টায় সাফল্য ও সম্মান বৃদ্ধি পাবে।"),
        7: ("বধ তারা", "অশুভ/সতর্কতার দিন — বড় কোনো সিদ্ধান্ত বা নতুন চুক্তি আজ স্থগিত রাখুন।"),
        8: ("মিত্র তারা", "অনুকূল দিন — বন্ধু, সহকর্মী ও শুভানুধ্যায়ীদের সহযোগিতা পাবেন।"),
        9: ("পরম মিত্র তারা", "অত্যন্ত শুভ — ভাগ্য সহায় থাকবে, গুরুত্বপূর্ণ কাজের জন্য সেরা সময়।")
    }
    tara_name, tara_desc = tara_map[tara_num]
    transit_house = ((t_moon_sign - moon) % 12) + 1
    rep['daily_transit'] = {
        't_sign': r_list[t_moon_sign - 1],
        't_nak': t_nak,
        'tara': f"{tara_name} ({tara_num}ম তারা)",
        'tara_desc': tara_desc,
        'house_msg': f"আজ চন্দ্র আপনার জন্মরাশি থেকে **{transit_house}ম ভাবে** ({r_list[t_moon_sign - 1]} রাশিতে, {t_nak} নক্ষত্রে) গোচর করছে।"
    }

    # বিস্তারিত ফলাফল ও প্রতিকার
    rep['grahan'] = "সূর্য বা চন্দ্র রাহুর নিকটবর্তী হওয়ায় গ্রহণ সংক্রান্ত সংবেদনশীলতা রয়েছে; অমাবস্যা-পূর্ণিমায় মানসিক স্থিরতা বজায় রাখুন।" if abs(pos['Sun']['deg'] - pos['Rahu']['deg']) < 12 or abs(pos['Moon']['deg'] - pos['Rahu']['deg']) < 12 else "কুণ্ডলীতে কোনো প্রত্যক্ষ গ্রহণ দোষ নেই।"
    rep['sadesati'] = "গোচরে শনির অবস্থান সাপেক্ষে সাড়েসাতির সতর্কতা বা কর্মভার বৃদ্ধি বজায় রয়েছে।" if (11 - moon) % 12 in [11, 0, 1] else "বর্তমানে জন্মরাশির ওপর শনির সাড়েসাতির প্রভাব নেই।"
    rep['nerve'] = "বুধের অবস্থান অনুযায়ী স্নায়বিক সংবেদনশীলতা ও অনিদ্রা এড়াতে নিয়মিত প্রাণায়াম ও বিশ্রাম প্রয়োজন।" if pos['Mercury']['sign'] in [6, 8, 12] else "স্নায়ুতন্ত্র ও স্মৃতিশক্তি স্থিতিশীল ও কর্মক্ষম।"
    rep['bone'] = "মেরুদণ্ড, অস্থিসন্ধি ও ভিটামিন-ডি/ক্যালসিয়ামের ভারসাম্যে নজর দেওয়া উচিত।" if pos['Sun']['sign'] in [7, 8] or pos['Saturn']['sign'] in [1, 7] else "হাড় ও শারীরিক কাঠামো বলিষ্ঠ।"
    rep['senses'] = "দৃষ্টিশক্তি ও কানের যত্ন নেওয়া বাঞ্ছনীয়।" if pos['Sun']['sign'] in [2, 12] else "পঞ্চেন্দ্রিয়ের সংবেদনশীলতা স্বাভাবিক।"
    rep['female_health'] = "হরমোনাল ভারসাম্য ও তলপেটের রুটিন চেকআপ প্রয়োজন।" if pos['Mars']['sign'] == 8 or pos['Venus']['sign'] in [6, 8] else "প্রজনন স্বাস্থ্য স্থিতিশীল।"
    rep['mother'] = "মায়ের মন সংবেদনশীল; বাতের ব্যথা, রক্তচাপ ও অনিদ্রার প্রতি যত্ন নেওয়া প্রয়োজন।"
    rep['father'] = "পিতা আত্মসম্মানবোধসম্পন্ন ও দৃঢ় চরিত্রের; অস্থি বা হৃদযন্ত্রের যত্নে নজর দিন।"
    rep['vastu'] = "বাড়ির উত্তর-পূর্ব (ঈশান) কোণ পরিষ্কার ও আলোকিত রাখুন এবং দক্ষিণ-পূর্ব কোণে অগ্নি উপাদানের ভারসাম্য বজায় রাখুন।"
    rep['remedy'] = "প্রতিদিন প্রাতঃসূর্যের আলো নিন, তামার পাত্রে জল পান করুন, পাখিদের জল দিন এবং সন্ধ্যায় ঘরে কর্পূর জ্বালান।"

    answers = {}
    seventh_sign = ((asc + 6) % 12) or 12
    if queries.get('partner'):
        answers['partner'] = "**দাম্পত্য ও জীবনসঙ্গী বিচার (৭ম ভাব):** জীবনসঙ্গী শান্ত, সংবেদনশীল ও পারিবারিক মূল্যবোধসম্পন্ন ব্যক্তিত্বের হবেন। পারস্পরিক বোঝাপড়া সুদৃঢ় থাকবে।" if seventh_sign in [2, 4, 9, 12] else "**দাম্পত্য ও জীবনসঙ্গী বিচার (৭ম ভাব):** জীবনসঙ্গী বাস্তববাদী, আত্মমর্যাদাবান ও স্বাধীনচেতা স্বভাবের হবেন। মতের অমিল এড়াতে নমনীয়তা বজায় রাখা শুভ।"
    if queries.get('career'):
        answers['career'] = "**কর্ম ও পেশা বিচার (১০ম ও ৬ষ্ঠ ভাব):** স্বাধীন পেশা (Consultancy/Self-employment) বা নিজস্ব ব্যবসার দিকে ভাগ্যোদয় প্রবল।" if pos['Mercury']['sign'] in [10, 7] or pos['Saturn']['sign'] in [10, 11] else "**কর্ম ও পেশা বিচার (১০ম ও ৬ষ্ঠ ভাব):** স্থায়ী চাকরি বা কোনো প্রশাসনিক/সাংগঠনিক পদে দায়িত্ব পালন অধিক লাভজনক ও নিরাপদ।"
    if queries.get('secret'):
        answers['secret'] = "**সংবেদনশীল স্বাস্থ্য বিচার (৮ম ও ১২শ ভাব):** ইউরিনারি বা তলপেটের সংবেদনশীলতায় সতর্কতা রাখুন; পর্যাপ্ত জল পান ও নিয়মিত শারীরিক পরীক্ষা জরুরি।" if pos['Rahu']['sign'] == 8 or pos['Mars']['sign'] in [6, 8] else "**সংবেদনশীল স্বাস্থ্য বিচার (৮ম ও ১২শ ভাব):** গুপ্ত রোগ বা দীর্ঘমেয়াদী অভ্যন্তরীণ জটিলতার কোনো নেতিবাচক প্রভাব নেই।"
    if queries.get('orient'):
        answers['orient'] = "**মানসিক ও সম্পর্কের প্রবণতা (শুক্র-রাহু যোগ):** প্রচলিত ধারণার বাইরে ভিন্নধর্মী রুচি ও গভীর আত্মিক মানসিক যোগাযোগের টান থাকবে।" if pos['Venus']['sign'] in [pos['Mercury']['sign'], pos['Saturn']['sign']] and pos['Rahu']['sign'] in [7, 8] else "**মানসিক ও সম্পর্কের প্রবণতা (৫ম ও শুক্র বিচার):** সম্পর্কের ক্ষেত্রে ঐতিহ্যগত মূল্যবোধ, স্থিরতা ও স্বাভাবিক আকর্ষণ বজায় থাকবে।"

    rep['answers'] = answers
    return rep


if submitted:
    if not place.strip():
        st.error("অনুগ্রহ করে জন্মস্থানের নাম লিখুন (যেমন: Kalyani, West Bengal)।")
    else:
        st.session_state['ready'] = True
        st.session_state['user_data'] = {
            'name': name, 'gender': gender, 'dob': dob, 'tob': tob, 'place': place,
            'queries': {'partner': q_partner, 'career': q_career, 'secret': q_secret, 'orient': q_orient}
        }

if st.session_state.get('ready'):
    ud = st.session_state['user_data']
    chart_data, err = calculate_chart(ud['dob'], ud['tob'], ud['place'])
    if err:
        st.error(err)
    else:
        rep = analyze_chart(chart_data, ud['dob'], ud['gender'], selected_lang, ud['queries'])

        # --- বিনামূল্যে প্রাথমিক অংশ ---
        st.subheader("🌟 প্রাথমিক জন্মপরিচয় (বিনামূল্যে)")
        c1, c2, c3 = st.columns(3)
        c1.info(f"**লগ্ন:** {rep['asc']}")
        c2.info(f"**জন্মরাশি:** {rep['moon']}")
        c3.info(f"**জন্ম নক্ষত্র:** {rep['moon_nak']}")

        tier = st.session_state.get('unlock_tier', 0)  # 0 = locked, 21 = basic, 51 = full

        # --- পেমেন্ট সেকশন (যদি ৫১ প্যাক আনলক না হয়ে থাকে) ---
        if tier < 51:
            st.markdown("---")
            st.subheader("🔓 আপনার পছন্দের রিপোর্ট আনলক করুন")
            pack_choice = st.radio(
                "প্যাকেজ নির্বাচন করুন:",
                [
                    f"₹{PRICE_BASIC} — দৈনিক গোচর ফলাফল + ৯টি গ্রহের স্পষ্ট অবস্থান ও কেপি সাব-লর্ড টেবিল",
                    f"₹{PRICE_PRO} — পূর্ণাঙ্গ প্রফেশনাল রিপোর্ট (গ্রহস্ফুট + ১২ ভাবের KP কাস্প টেবিল + বিংশোত্তরী দশা + প্রশ্নোত্তর ও প্রতিকার)"
                ]
            )
            sel_amount = PRICE_BASIC if "21" in pack_choice else PRICE_PRO
            upi_url = f"upi://pay?pa={MY_UPI_ID}&pn=AstroConsultancy&am={sel_amount}&cu=INR&tn=Astro_Report_{sel_amount}"
            qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(upi_url)}"

            col1, col2 = st.columns([1, 1])
            with col1:
                st.image(qr_api, caption=f"স্ক্যান করে ₹{sel_amount} পেমেন্ট করুন")
            with col2:
                st.write(f"**নির্বাচিত মূল্য:** ₹{sel_amount}")
                st.write("১. যেকোনো UPI অ্যাপ (GPay / PhonePe / Paytm) দিয়ে QR কোড স্ক্যান করে পেমেন্ট করুন।")
                st.write("২. পেমেন্টের পর প্রাপ্ত ৪ সংখ্যার পিন দিয়ে আনলক করুন।")
                input_pin = st.text_input("৪ সংখ্যার আনলক পিন দিন:", type="password")
                if st.button("রিপোর্ট আনলক করুন"):
                    if input_pin == PIN_51:
                        st.session_state['unlock_tier'] = 51
                        st.rerun()
                    elif input_pin == PIN_21:
                        st.session_state['unlock_tier'] = 21
                        st.rerun()
                    else:
                        st.error("ভুল পিন! সঠিক পিন পেতে পেমেন্টের স্ক্রিনশট পাঠান।")

        # --- আনলক হওয়া রিপোর্ট প্রদর্শন (₹২১ এবং ₹৫১ উভয়ের জন্য) ---
        if tier >= 21:
            st.markdown("---")
            st.success("✅ রিপোর্ট আনলক হয়েছে!")

            st.markdown("### 📅 আজকের গোচর ও দৈনিক ফলাফল (Daily Transit)")
            dt_info = rep['daily_transit']
            st.info(f"{dt_info['house_msg']}\n\n**আজকের তারাশুদ্ধি:** {dt_info['tara']} — {dt_info['tara_desc']}")

            st.markdown("### 🪐 নবগ্রহের স্পষ্ট অবস্থান, নক্ষত্র ও কেপি সাব-লর্ড")
            st.table(rep['planet_table'])

        # --- শুধুমাত্র ₹৫১ পূর্ণাঙ্গ রিপোর্টের অংশ ---
        if tier == 51:
            st.markdown("### 🏛️ দ্বাদশ ভাবের কেপি কাস্পাল অবস্থান (KP Cuspal Table)")
            st.table(rep['cusp_table'])

            st.markdown("### ⏳ বিংশোত্তরী মহাদশা বিচার")
            st.write(rep['dasha_info'])

            st.markdown("### 📊 জ্যোতিষ ও গ্রহীয় যোগ বিচার")
            st.write(f"• **গুলিক অবস্থান:** {rep['gulika']}")
            st.write(f"• **শনির সাড়েসাতি:** {rep['sadesati']}")
            st.write(f"• **গ্রহণ দোষ বিচার:** {rep['grahan']}")

            st.markdown("### 🩺 স্বাস্থ্য, ইন্দ্রিয় ও শারীরিক গঠন")
            st.write(f"• **স্নায়ুতন্ত্র:** {rep['nerve']}")
            st.write(f"• **অস্থি ও কাঠামো:** {rep['bone']}")
            st.write(f"• **পঞ্চেন্দ্রিয়:** {rep['senses']}")
            if ud['gender'] in ["মহিলা", "Female"]:
                st.write(f"• **আভ্যন্তরীণ স্বাস্থ্য:** {rep['female_health']}")

            st.markdown("### 👨‍👩‍👦 পিতা ও মাতা সংক্রান্ত বিচার")
            st.write(f"• **মাতৃভাব:** {rep['mother']}")
            st.write(f"• **পিতৃভাব:** {rep['father']}")

            if rep['answers']:
                st.markdown("### 🎯 আপনার নির্বাচিত প্রশ্নগুলোর গভীর বিশ্লেষণ")
                for k, ans in rep['answers'].items():
                    st.write(f"• {ans}")

            st.markdown("### 🏡 বাস্তু ও ব্যবহারিক প্রতিকার নির্দেশিকা")
            st.write(f"• **বাস্তু পরামর্শ:** {rep['vastu']}")
            st.write(f"• **প্রতিকার:** {rep['remedy']}")

    
