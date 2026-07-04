"use client"
import Link from "next/link"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { ShieldCheck, User, Calendar, Camera, Phone, Mail, MapPin, Map, Globe, ChevronDown, Lock, Bell, Users, ChevronRight } from "lucide-react"

// Custom Lotus SVG Logo
const LotusIcon = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="currentColor" className={className} xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C12 2 10 6 10 10C10 14 12 18 12 18C12 18 14 14 14 10C14 6 12 2 12 2Z" opacity="0.6"/>
    <path d="M12 22C12 22 16 19 19 15C22 11 22 7 22 7C22 7 18 8 14 11C11.5 12.8 12 22 12 22Z" opacity="0.8"/>
    <path d="M12 22C12 22 8 19 5 15C2 11 2 7 2 7C2 7 6 8 10 11C12.5 12.8 12 22 12 22Z" />
  </svg>
)


const translations: Record<string, Record<string, string>> = {
  English: {
    title: "Let's get to know you better",
    subtitle: "Help us personalize your experience and keep you informed about what matters most.",
    createProfile: "Create Your Profile",
    createSubtitle: "Just a few details to get you started.",
    google: "Sign up with Google",
    or: "OR REGISTER WITH EMAIL",
    fullName: "Full Name",
    fullNamePl: "Enter your full name",
    age: "Age",
    agePl: "Enter your age",
    picture: "Profile Picture",
    upload: "Upload a profile picture",
    maxSize: "JPG, PNG or WEBP. Max size 2MB.",
    choose: "Choose File",
    mobile: "Mobile Number",
    mobilePl: "Enter your mobile number",
    email: "Email (Optional)",
    emailPl: "Enter your email address",
    password: "Create Password",
    city: "City",
    cityPl: "Enter your city",
    state: "State / Province (Optional)",
    statePl: "Enter your state or province",
    prefLang: "Preferred Language",
    privacy: "Your privacy matters",
    privacyDesc: "We only use your information to personalize your experience and keep you safe. You can change this anytime in settings.",
    continueBtn: "Continue",
    update: "You can update these details anytime later.",
    errorMsg: "Please fill in all mandatory fields to continue.",
    feature1Title: "Personalized Experience",
    feature1Desc: "Get alerts and insights relevant to you.",
    feature2Title: "Timely Alerts",
    feature2Desc: "Stay informed about harmful content.",
    feature3Title: "Safer Community",
    feature3Desc: "Together, we build a peaceful digital world.",
    secureNote: "Your information is secure and never shared with anyone."
  },
  Hindi: {
    title: "आइए आपको बेहतर जानें",
    subtitle: "अपने अनुभव को व्यक्तिगत बनाने और महत्वपूर्ण बातों से अवगत रहने में हमारी मदद करें।",
    createProfile: "अपनी प्रोफाइल बनाएं",
    createSubtitle: "शुरू करने के लिए बस कुछ विवरण।",
    google: "Google के साथ साइन अप करें",
    or: "या ईमेल से पंजीकरण करें",
    fullName: "पूरा नाम",
    fullNamePl: "अपना पूरा नाम दर्ज करें",
    age: "आयु",
    agePl: "अपनी आयु दर्ज करें",
    picture: "प्रोफ़ाइल चित्र",
    upload: "एक प्रोफ़ाइल चित्र अपलोड करें",
    maxSize: "JPG, PNG या WEBP. अधिकतम 2MB.",
    choose: "फ़ाइल चुनें",
    mobile: "मोबाइल नंबर",
    mobilePl: "अपना मोबाइल नंबर दर्ज करें",
    email: "ईमेल (वैकल्पिक)",
    emailPl: "अपना ईमेल पता दर्ज करें",
    password: "पासवर्ड बनाएं",
    city: "शहर",
    cityPl: "अपना शहर दर्ज करें",
    state: "राज्य / प्रांत (वैकल्पिक)",
    statePl: "अपना राज्य या प्रांत दर्ज करें",
    prefLang: "पसंदीदा भाषा",
    privacy: "आपकी निजता महत्वपूर्ण है",
    privacyDesc: "हम आपकी जानकारी का उपयोग केवल आपके अनुभव को व्यक्तिगत बनाने और आपको सुरक्षित रखने के लिए करते हैं।",
    continueBtn: "जारी रखें",
    update: "आप बाद में कभी भी इन विवरणों को अपडेट कर सकते हैं।",
    errorMsg: "कृपया जारी रखने के लिए सभी अनिवार्य फ़ील्ड भरें।",
    feature1Title: "व्यक्तिगत अनुभव",
    feature1Desc: "आपके लिए प्रासंगिक अलर्ट और जानकारी प्राप्त करें।",
    feature2Title: "समय पर अलर्ट",
    feature2Desc: "हानिकारक सामग्री के बारे में सूचित रहें।",
    feature3Title: "सुरक्षित समुदाय",
    feature3Desc: "हम एक साथ एक शांतिपूर्ण डिजिटल दुनिया का निर्माण करते हैं।",
    secureNote: "आपकी जानकारी सुरक्षित है और कभी भी किसी के साथ साझा नहीं की जाती है।"
  },

  Kannada: {
    title: "ನಿಮ್ಮನ್ನು ಉತ್ತಮವಾಗಿ ತಿಳಿಯೋಣ",
    subtitle: "ನಿಮ್ಮ ಅನುಭವವನ್ನು ವೈಯಕ್ತೀಕರಿಸಲು ಮತ್ತು ನಿಮಗೆ ಮುಖ್ಯವಾದ ವಿಷಯಗಳ ಬಗ್ಗೆ ತಿಳಿಸಲು ನಮಗೆ ಸಹಾಯ ಮಾಡಿ.",
    createProfile: "ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ರಚಿಸಿ",
    createSubtitle: "ನೀವು ಪ್ರಾರಂಭಿಸಲು ಕೆಲವು ವಿವರಗಳು.",
    google: "Google ನೊಂದಿಗೆ ಸೈನ್ ಅಪ್ ಮಾಡಿ",
    or: "ಅಥವಾ ಇಮೇಲ್ ಮೂಲಕ ನೋಂದಾಯಿಸಿ",
    fullName: "ಪೂರ್ಣ ಹೆಸರು",
    fullNamePl: "ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರನ್ನು ನಮೂದಿಸಿ",
    age: "ವಯಸ್ಸು",
    agePl: "ನಿಮ್ಮ ವಯಸ್ಸನ್ನು ನಮೂದಿಸಿ",
    picture: "ಪ್ರೊಫೈಲ್ ಚಿತ್ರ",
    upload: "ಪ್ರೊಫೈಲ್ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
    maxSize: "JPG, PNG ಅಥವಾ WEBP. ಗರಿಷ್ಠ 2MB.",
    choose: "ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ",
    mobile: "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ",
    mobilePl: "ನಿಮ್ಮ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ",
    email: "ಇಮೇಲ್ (ಐಚ್ಛಿಕ)",
    emailPl: "ನಿಮ್ಮ ಇಮೇಲ್ ವಿಳಾಸವನ್ನು ನಮೂದಿಸಿ",
    password: "ಪಾಸ್‌ವರ್ಡ್ ರಚಿಸಿ",
    city: "ನಗರ",
    cityPl: "ನಿಮ್ಮ ನಗರವನ್ನು ನಮೂದಿಸಿ",
    state: "ರಾಜ್ಯ / ಪ್ರಾಂತ್ಯ (ಐಚ್ಛಿಕ)",
    statePl: "ನಿಮ್ಮ ರಾಜ್ಯ ಅಥವಾ ಪ್ರಾಂತ್ಯವನ್ನು ನಮೂದಿಸಿ",
    prefLang: "ಆದ್ಯತೆಯ ಭಾಷೆ",
    privacy: "ನಿಮ್ಮ ಗೌಪ್ಯತೆ ಮುಖ್ಯವಾಗಿದೆ",
    privacyDesc: "ನಿಮ್ಮ ಅನುಭವವನ್ನು ವೈಯಕ್ತೀಕರಿಸಲು ಮತ್ತು ನಿಮ್ಮನ್ನು ಸುರಕ್ಷಿತವಾಗಿರಿಸಲು ಮಾತ್ರ ನಾವು ನಿಮ್ಮ ಮಾಹಿತಿಯನ್ನು ಬಳಸುತ್ತೇವೆ. ಸೆಟ್ಟಿಂಗ್‌ಗಳಲ್ಲಿ ನೀವು ಇದನ್ನು ಯಾವಾಗ ಬೇಕಾದರೂ ಬದಲಾಯಿಸಬಹುದು.",
    continueBtn: "ಮುಂದುವರಿಸಿ",
    update: "ನೀವು ನಂತರ ಯಾವಾಗಲಾದರೂ ಈ ವಿವರಗಳನ್ನು ನವೀಕರಿಸಬಹುದು.",
    errorMsg: "ಮುಂದುವರಿಯಲು ದಯವಿಟ್ಟು ಎಲ್ಲಾ ಕಡ್ಡಾಯ ಕ್ಷೇತ್ರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ.",
    feature1Title: "ವೈಯಕ್ತಿಕಗೊಳಿಸಿದ ಅನುಭವ",
    feature1Desc: "ನಿಮಗೆ ಸಂಬಂಧಿಸಿದ ಎಚ್ಚರಿಕೆಗಳು ಮತ್ತು ಒಳನೋಟಗಳನ್ನು ಪಡೆಯಿರಿ.",
    feature2Title: "ಸಕಾಲಿಕ ಎಚ್ಚರಿಕೆಗಳು",
    feature2Desc: "ಹಾನಿಕಾರಕ ವಿಷಯದ ಬಗ್ಗೆ ಮಾಹಿತಿ ಹೊಂದಿರಿ.",
    feature3Title: "ಸುರಕ್ಷಿತ ಸಮುದಾಯ",
    feature3Desc: "ಒಟ್ಟಾಗಿ, ನಾವು ಶಾಂತಿಯುತ ಡಿಜಿಟಲ್ ಜಗತ್ತನ್ನು ನಿರ್ಮಿಸುತ್ತೇವೆ.",
    secureNote: "ನಿಮ್ಮ ಮಾಹಿತಿಯು ಸುರಕ್ಷಿತವಾಗಿದೆ ಮತ್ತು ಎಂದಿಗೂ ಯಾರೊಂದಿಗೂ ಹಂಚಿಕೊಳ್ಳುವುದಿಲ್ಲ."
  },
  Tamil: {
    title: "உங்களை பற்றி மேலும் தெரிந்துகொள்ளலாம்",
    subtitle: "உங்கள் அனுபவத்தை தனிப்பயனாக்கவும், முக்கிய தகவல்களைப் பற்றி அறியவும் எங்களுக்கு உதவுங்கள்.",
    createProfile: "உங்கள் சுயவிவரத்தை உருவாக்கவும்",
    createSubtitle: "தொடங்குவதற்கு சில விவரங்கள் மட்டும்.",
    google: "Google மூலம் உள்நுழையவும்",
    or: "அல்லது மின்னஞ்சல் மூலம் பதிவு செய்யவும்",
    fullName: "முழு பெயர்",
    fullNamePl: "உங்கள் முழு பெயரை உள்ளிடவும்",
    age: "வயது",
    agePl: "உங்கள் வயதை உள்ளிடவும்",
    picture: "சுயவிவரப் படம்",
    upload: "சுயவிவரப் படத்தைப் பதிவேற்றவும்",
    maxSize: "JPG, PNG அல்லது WEBP. அதிகபட்சம் 2MB.",
    choose: "கோப்பைத் தேர்ந்தெடுக்கவும்",
    mobile: "மொபைல் எண்",
    mobilePl: "உங்கள் மொபைல் எண்ணை உள்ளிடவும்",
    email: "மின்னஞ்சல் (விருப்பத்திற்குரியது)",
    emailPl: "உங்கள் மின்னஞ்சல் முகவரியை உள்ளிடவும்",
    password: "கடவுச்சொல்லை உருவாக்கவும்",
    city: "நகரம்",
    cityPl: "உங்கள் நகரத்தை உள்ளிடவும்",
    state: "மாநிலம் / மாகாணம் (விருப்பத்திற்குரியது)",
    statePl: "உங்கள் மாநிலம் அல்லது மாகாணத்தை உள்ளிடவும்",
    prefLang: "விருப்பமான மொழி",
    privacy: "உங்கள் தனியுரிமை முக்கியமானது",
    privacyDesc: "உங்கள் அனுபவத்தை தனிப்பயனாக்கவும் உங்களைப் பாதுகாப்பாக வைத்திருக்கவும் மட்டுமே நாங்கள் உங்கள் தகவலைப் பயன்படுத்துகிறோம். அமைப்புகளில் இதை எப்போது வேண்டுமானாலும் மாற்றலாம்.",
    continueBtn: "தொடரவும்",
    update: "இந்த விவரங்களை நீங்கள் பின்னர் எப்போது வேண்டுமானாலும் புதுப்பிக்கலாம்.",
    errorMsg: "தொடர தேவையான அனைத்து புலங்களையும் நிரப்பவும்.",
    feature1Title: "தனிப்பயனாக்கப்பட்ட அனுபவம்",
    feature1Desc: "உங்களுக்கு தொடர்புடைய விழிப்பூட்டல்கள் மற்றும் நுண்ணறிவுகளைப் பெறுங்கள்.",
    feature2Title: "சரியான நேர விழிப்பூட்டல்கள்",
    feature2Desc: "தீங்கு விளைவிக்கும் உள்ளடக்கத்தைப் பற்றி அறிந்திருங்கள்.",
    feature3Title: "பாதுகாப்பான சமூகம்",
    feature3Desc: "ஒன்றாக, நாம் ஒரு அமைதியான டிஜிட்டல் உலகத்தை உருவாக்குகிறோம்.",
    secureNote: "உங்கள் தகவல்கள் பாதுகாப்பானவை மற்றும் யாருடனும் பகிரப்படாது."
  },
  Urdu: {
    title: "آئیے آپ کو بہتر طور پر جانیں",
    subtitle: "اپنے تجربے کو ذاتی بنانے اور اہم معلومات سے باخبر رہنے میں ہماری مدد کریں۔",
    createProfile: "اپنی پروفائل بنائیں",
    createSubtitle: "شروع کرنے کے لیے بس چند تفصیلات۔",
    google: "Google کے ساتھ سائن اپ کریں",
    or: "یا ای میل کے ذریعے رجسٹر کریں",
    fullName: "پورا نام",
    fullNamePl: "اپنا پورا نام درج کریں",
    age: "عمر",
    agePl: "اپنی عمر درج کریں",
    picture: "پروفائل تصویر",
    upload: "پروفائل تصویر اپ لوڈ کریں",
    maxSize: "JPG, PNG یا WEBP. زیادہ سے زیادہ 2MB.",
    choose: "فائل منتخب کریں",
    mobile: "موبائل نمبر",
    mobilePl: "اپنا موبائل نمبر درج کریں",
    email: "ای میل (اختیاری)",
    emailPl: "اپنا ای میل ایڈریس درج کریں",
    password: "پاس ورڈ بنائیں",
    city: "شہر",
    cityPl: "اپنا شہر درج کریں",
    state: "ریاست / صوبہ (اختیاری)",
    statePl: "اپنی ریاست یا صوبہ درج کریں",
    prefLang: "پسندیدہ زبان",
    privacy: "آپ کی پرائیویسی اہم ہے",
    privacyDesc: "ہم آپ کی معلومات کو صرف آپ کے تجربے کو ذاتی بنانے اور آپ کو محفوظ رکھنے کے لیے استعمال کرتے ہیں۔ آپ اسے کسی بھی وقت سیٹنگز میں تبدیل کر سکتے ہیں۔",
    continueBtn: "جاری رکھیں",
    update: "آپ بعد میں کسی بھی وقت ان تفصیلات کو اپ ڈیٹ کر سکتے ہیں۔",
    errorMsg: "جاری رکھنے کے لیے براہ کرم تمام لازمی فیلڈز پُر کریں۔",
    feature1Title: "ذاتی تجربہ",
    feature1Desc: "اپنے لیے متعلقہ الرٹس اور بصیرتیں حاصل کریں۔",
    feature2Title: "بروقت الرٹس",
    feature2Desc: "نقصان دہ مواد کے بارے میں باخبر رہیں۔",
    feature3Title: "محفوظ کمیونٹی",
    feature3Desc: "ہم مل کر ایک پرامن ڈیجیٹل دنیا بناتے ہیں۔",
    secureNote: "آپ کی معلومات محفوظ ہیں اور کبھی کسی کے ساتھ شیئر نہیں کی جاتیں۔"
  },
  Telugu: {
    title: "మిమ్మల్ని మరింత బాగా తెలుసుకుందాం",
    subtitle: "మీ అనుభవాన్ని వ్యక్తిగతీకరించడానికి మరియు ముఖ్యమైన విషయాల గురించి మీకు తెలియజేయడానికి మాకు సహాయపడండి.",
    createProfile: "మీ ప్రొఫైల్‌ను సృష్టించండి",
    createSubtitle: "ప్రారంభించడానికి కేవలం కొన్ని వివరాలు.",
    google: "Googleతో సైన్ అప్ చేయండి",
    or: "లేదా ఇమెయిల్‌తో నమోదు చేయండి",
    fullName: "పూర్తి పేరు",
    fullNamePl: "మీ పూర్తి పేరు నమోదు చేయండి",
    age: "వయస్సు",
    agePl: "మీ వయస్సును నమోదు చేయండి",
    picture: "ప్రొఫైల్ చిత్రం",
    upload: "ప్రొఫైల్ చిత్రాన్ని అప్‌లోడ్ చేయండి",
    maxSize: "JPG, PNG లేదా WEBP. గరిష్టంగా 2MB.",
    choose: "ఫైల్‌ని ఎంచుకోండి",
    mobile: "మొబైల్ నంబర్",
    mobilePl: "మీ మొబైల్ నంబర్‌ను నమోదు చేయండి",
    email: "ఇమెయిల్ (ఐచ్ఛికం)",
    emailPl: "మీ ఇమెయిల్ చిరునామాను నమోదు చేయండి",
    password: "పాస్‌వర్డ్ సృష్టించండి",
    city: "నగరం",
    cityPl: "మీ నగరాన్ని నమోదు చేయండి",
    state: "రాష్ట్రం / ప్రావిన్స్ (ఐచ్ఛికం)",
    statePl: "మీ రాష్ట్రం లేదా ప్రావిన్స్‌ను నమోదు చేయండి",
    prefLang: "ప్రాధాన్య భాష",
    privacy: "మీ గోప్యత ముఖ్యం",
    privacyDesc: "మేము మీ సమాచారాన్ని మీ అనుభవాన్ని వ్యక్తిగతీకరించడానికి మరియు మిమ్మల్ని సురక్షితంగా ఉంచడానికి మాత్రమే ఉపయోగిస్తాము. మీరు సెట్టింగ్‌లలో దీన్ని ఎప్పుడైనా మార్చవచ్చు.",
    continueBtn: "కొనసాగించండి",
    update: "మీరు తర్వాత ఎప్పుడైనా ఈ వివరాలను నవీకరించవచ్చు.",
    errorMsg: "కొనసాగించడానికి దయచేసి అన్ని తప్పనిసరి ఫీల్డ్‌లను పూరించండి.",
    feature1Title: "వ్యక్తిగతీకరించిన అనుభవం",
    feature1Desc: "మీకు సంబంధించిన హెచ్చరికలు మరియు అంతర్దృష్టులను పొందండి.",
    feature2Title: "సకాలంలో హెచ్చరికలు",
    feature2Desc: "హానికరమైన కంటెంట్ గురించి తెలుసుకోండి.",
    feature3Title: "సురక్షితమైన సంఘం",
    feature3Desc: "కలిసి, మనం శాంతియుత డిజిటల్ ప్రపంచాన్ని నిర్మిస్తాము.",
    secureNote: "మీ సమాచారం సురక్షితం మరియు ఎవరితోనూ భాగస్వామ్యం చేయబడదు."
  },
  Malayalam: {
    title: "ഞങ്ങൾക്ക് നിങ്ങളെ കൂടുതൽ അറിയാൻ അവസരം നൽകുക",
    subtitle: "നിങ്ങളുടെ അനുഭവം വ്യക്തിഗതമാക്കാനും പ്രധാനപ്പെട്ട കാര്യങ്ങളെക്കുറിച്ച് നിങ്ങളെ അറിയിക്കാനും ഞങ്ങളെ സഹായിക്കുക.",
    createProfile: "നിങ്ങളുടെ പ്രൊഫൈൽ സൃഷ്ടിക്കുക",
    createSubtitle: "ആരംഭിക്കാൻ കുറച്ച് വിശദാംശങ്ങൾ മാത്രം.",
    google: "Google വഴി സൈൻ അപ്പ് ചെയ്യുക",
    or: "അല്ലെങ്കിൽ ഇമെയിൽ വഴി രജിസ്റ്റർ ചെയ്യുക",
    fullName: "മുഴുവൻ പേര്",
    fullNamePl: "നിങ്ങളുടെ മുഴുവൻ പേരും നൽകുക",
    age: "പ്രായം",
    agePl: "നിങ്ങളുടെ പ്രായം നൽകുക",
    picture: "പ്രൊഫൈൽ ചിത്രം",
    upload: "പ്രൊഫൈൽ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
    maxSize: "JPG, PNG അല്ലെങ്കിൽ WEBP. പരമാവധി 2MB.",
    choose: "ഫയൽ തിരഞ്ഞെടുക്കുക",
    mobile: "മൊബൈൽ നമ്പർ",
    mobilePl: "നിങ്ങളുടെ മൊബൈൽ നമ്പർ നൽകുക",
    email: "ഇമെയിൽ (ഓപ്ഷണൽ)",
    emailPl: "നിങ്ങളുടെ ഇമെയിൽ വിലാസം നൽകുക",
    password: "പാസ്‌വേഡ് സൃഷ്ടിക്കുക",
    city: "നഗരം",
    cityPl: "നിങ്ങളുടെ നഗരം നൽകുക",
    state: "സംസ്ഥാനം / പ്രവിശ്യ (ഓപ്ഷണൽ)",
    statePl: "നിങ്ങളുടെ സംസ്ഥാനം നൽകുക",
    prefLang: "താൽപ്പര്യമുള്ള ഭാഷ",
    privacy: "നിങ്ങളുടെ സ്വകാര്യത പ്രധാനമാണ്",
    privacyDesc: "നിങ്ങളുടെ അനുഭവം വ്യക്തിഗതമാക്കാനും നിങ്ങളെ സുരക്ഷിതമായി സൂക്ഷിക്കാനും മാത്രമാണ് ഞങ്ങൾ നിങ്ങളുടെ വിവരങ്ങൾ ഉപയോഗിക്കുന്നത്. ക്രമീകരണങ്ങളിൽ നിങ്ങൾക്ക് ഇത് എപ്പോൾ വേണമെങ്കിലും മാറ്റാം.",
    continueBtn: "തുടരുക",
    update: "നിങ്ങൾക്ക് പിന്നീട് എപ്പോൾ വേണമെങ്കിലും ഈ വിവരങ്ങൾ അപ്‌ഡേറ്റ് ചെയ്യാം.",
    errorMsg: "തുടരാൻ ദയവായി എല്ലാ നിർബന്ധിത ഫീൽഡുകളും പൂരിപ്പിക്കുക.",
    feature1Title: "വ്യക്തിഗത അനുഭവം",
    feature1Desc: "നിങ്ങൾക്ക് പ്രസക്തമായ അലേർട്ടുകളും വിവരങ്ങളും നേടുക.",
    feature2Title: "സമയബന്ധിതമായ അലേർട്ടുകൾ",
    feature2Desc: "ഹാനികരമായ ഉള്ളടക്കത്തെക്കുറിച്ച് അറിഞ്ഞിരിക്കുക.",
    feature3Title: "സുരക്ഷിതമായ കമ്മ്യൂണിറ്റി",
    feature3Desc: "ഒരുമിച്ച്, നാം സമാധാനപരമായ ഒരു ഡിജിറ്റൽ ലോകം കെട്ടിപ്പടുക്കുന്നു.",
    secureNote: "നിങ്ങളുടെ വിവരങ്ങൾ സുരക്ഷിതമാണ്, അത് ഒരിക്കലും ആരുമായും പങ്കിടില്ല."
  },
  Marathi: {
    title: "आम्हाला तुम्हाला अधिक चांगल्या प्रकारे जाणून घेऊ द्या",
    subtitle: "तुमचा अनुभव वैयक्तिकृत करण्यात आणि महत्त्वाच्या गोष्टींबद्दल तुम्हाला माहिती देण्यात आम्हाला मदत करा.",
    createProfile: "तुमची प्रोफाइल तयार करा",
    createSubtitle: "सुरुवात करण्यासाठी फक्त काही तपशील.",
    google: "Google सह साइन अप करा",
    or: "किंवा ईमेलसह नोंदणी करा",
    fullName: "पूर्ण नाव",
    fullNamePl: "तुमचे पूर्ण नाव प्रविष्ट करा",
    age: "वय",
    agePl: "तुमचे वय प्रविष्ट करा",
    picture: "प्रोफाइल चित्र",
    upload: "प्रोफाइल चित्र अपलोड करा",
    maxSize: "JPG, PNG किंवा WEBP. कमाल 2MB.",
    choose: "फाईल निवडा",
    mobile: "मोबाईल नंबर",
    mobilePl: "तुमचा मोबाईल नंबर प्रविष्ट करा",
    email: "ईमेल (पर्यायी)",
    emailPl: "तुमचा ईमेल पत्ता प्रविष्ट करा",
    password: "पासवर्ड तयार करा",
    city: "शहर",
    cityPl: "तुमचे शहर प्रविष्ट करा",
    state: "राज्य / प्रांत (पर्यायी)",
    statePl: "तुमचे राज्य प्रविष्ट करा",
    prefLang: "पसंतीची भाषा",
    privacy: "तुमची गोपनीयता महत्त्वाची आहे",
    privacyDesc: "आम्ही तुमची माहिती केवळ तुमचा अनुभव वैयक्तिकृत करण्यासाठी आणि तुम्हाला सुरक्षित ठेवण्यासाठी वापरतो. तुम्ही हे सेटिंग्जमध्ये कधीही बदलू शकता.",
    continueBtn: "पुढे जा",
    update: "तुम्ही हे तपशील नंतर कधीही अपडेट करू शकता.",
    errorMsg: "पुढे जाण्यासाठी कृपया सर्व अनिवार्य फील्ड भरा.",
    feature1Title: "वैयक्तिकृत अनुभव",
    feature1Desc: "तुमच्यासाठी संबंधित सूचना आणि माहिती मिळवा.",
    feature2Title: "वेळेवर सूचना",
    feature2Desc: "हानीकारक सामग्रीबद्दल माहिती मिळवा.",
    feature3Title: "सुरक्षित समुदाय",
    feature3Desc: "एकत्रितपणे, आपण एक शांततापूर्ण डिजिटल जग तयार करतो.",
    secureNote: "तुमची माहिती सुरक्षित आहे आणि ती कोणाशीही सामायिक केली जात नाही."
  }
,
  Bengali: {
    title: "আসুন আপনার সম্পর্কে আরও জানি",
    subtitle: "আপনার অভিজ্ঞতা কাস্টমাইজ করতে আমাদের সাহায্য করুন।",
    createProfile: "আপনার প্রোফাইল তৈরি করুন",
    createSubtitle: "শুরু করার জন্য কয়েকটি বিবরণ।",
    google: "Google দিয়ে সাইন আপ করুন",
    or: "অথবা ইমেল দিয়ে নিবন্ধন করুন",
    fullName: "পুরো নাম",
    fullNamePl: "আপনার পুরো নাম লিখুন",
    age: "বয়স",
    agePl: "আপনার বয়স লিখুন",
    picture: "প্রোফাইল ছবি",
    upload: "একটি প্রোফাইল ছবি আপলোড করুন",
    maxSize: "JPG, PNG বা WEBP. সর্বোচ্চ ২MB।",
    choose: "ফাইল বাছুন",
    mobile: "মোবাইল নম্বর",
    mobilePl: "আপনার মোবাইল নম্বর লিখুন",
    email: "ইমেল (ঐচ্ছিক)",
    emailPl: "আপনার ইমেল ঠিকানা লিখুন",
    password: "পাসওয়ার্ড তৈরি করুন",
    city: "শহর",
    cityPl: "আপনার শহর লিখুন",
    state: "রাজ্য / প্রদেশ (ঐচ্ছিক)",
    statePl: "আপনার রাজ্য লিখুন",
    prefLang: "পছন্দের ভাষা",
    privacy: "আপনার গোপনীয়তা গুরুত্বপূর্ণ",
    privacyDesc: "আমরা আপনার তথ্য শুধুমাত্র আপনার অভিজ্ঞতা ব্যক্তিগত করতে ব্যবহার করি।",
    continueBtn: "চালিয়ে যান",
    update: "আপনি পরে যেকোনো সময় এই বিবরণ আপডেট করতে পারেন।",
    errorMsg: "দয়া করে সব আবশ্যক তথ্য পূরণ করুন।",
    feature1Title: "ব্যক্তিগত অভিজ্ঞতা",
    feature1Desc: "আপনার জন্য প্রাসঙ্গিক অ্যালার্ট পান।",
    feature2Title: "সময়মত অ্যালার্ট",
    feature2Desc: "ক্ষতিকারক কন্টেন্ট সম্পর্কে জানুন।",
    feature3Title: "নিরাপদ সম্প্রদায়",
    feature3Desc: "একসাথে আমরা একটি শান্তিপূর্ণ ডিজিটাল বিশ্ব গড়ে তুলি।",
    secureNote: "আপনার তথ্য সুরক্ষিত এবং কখনও শেয়ার করা হয় না।"
  }
};

export default function OnboardingPage() {
  const router = useRouter()
  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [age, setAge] = useState("")
  const [mobile, setMobile] = useState("")
  const [city, setCity] = useState("")
  const [password, setPassword] = useState("")
  const [language, setLanguage] = useState("English")
  const [error, setError] = useState("")
  const t = translations[language] || translations["English"]

  const handleContinue = async () => {
    if (!fullName.trim() || !email.trim() || !age.trim() || !mobile.trim() || !city.trim() || !password.trim()) {
      setError(t.errorMsg)
      return
    }
    setError("")
    
    try {
      // 1. Register User
      const regRes = await fetch("/api/v1/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email.trim(),
          password: password.trim(),
          organization_name: fullName.trim()
        })
      })

      if (!regRes.ok) {
        const data = await regRes.json()
        setError(data.detail || "Registration failed")
        return
      }

      // 2. Login to get token
      const loginRes = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email.trim(),
          password: password.trim()
        })
      })

      if (!loginRes.ok) {
        setError("Login after registration failed")
        return
      }

      const loginData = await loginRes.json()

      // Store token securely in cookie
      const Cookies = (await import('js-cookie')).default
      Cookies.set('sukoon_token', loginData.access_token, { 
          expires: 7, 
          secure: process.env.NODE_ENV === 'production',
          sameSite: 'strict'
      })

      // Store safe preferences in localStorage
      localStorage.setItem('sukoon_language', language)
      
      router.push('/dashboard')
    } catch (err) {
      setError("An error occurred during registration.")
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col md:flex-row font-sans">
       
       {/* Left Column (Information) */}
       <div className="w-full md:w-[45%] lg:w-[40%] bg-[#F8FAFC] p-8 lg:p-12 xl:p-16 flex flex-col min-h-screen border-r border-slate-200">
          
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 mb-16 hover:opacity-90 transition-opacity w-fit">
            <LotusIcon className="w-8 h-8 text-emerald-600" />
            <div className="flex flex-col">
              <span className="text-[17px] font-semibold tracking-tight text-slate-800 leading-none">Sukoon <span className="font-bold text-emerald-600">AI</span></span>
              <span className="text-[8px] text-slate-500 font-medium tracking-wide mt-1">Verified Peace. Digital Harmony.</span>
            </div>
          </Link>

          {/* Heading */}
          <div className="mb-10">
             <h1 className="text-[32px] lg:text-[40px] font-bold text-slate-800 leading-[1.15] mb-4">
                {t.title}
             </h1>
             <p className="text-[13px] text-slate-500 font-medium leading-relaxed max-w-[320px]">
                {t.subtitle}
             </p>
          </div>

          {/* Illustration Area */}
          <div className="relative w-full max-w-[340px] h-[220px] mb-8 mx-auto md:mx-0 flex items-center justify-center">
             <img src="/man_laptop.png" alt="Onboarding Hero" className="w-[120%] h-[120%] object-contain -ml-8 mix-blend-multiply" />
             <div className="absolute top-10 right-4 w-12 h-12 bg-white rounded-full shadow-lg border border-slate-100 flex items-center justify-center text-emerald-600 z-10 hidden sm:flex">
                <User className="w-6 h-6" />
             </div>
          </div>

          {/* Feature Highlight Box */}
          <div className="bg-[#f0fdf4] rounded-2xl p-6 border border-[#dcfce7] mb-auto">
             <div className="space-y-5">
                <div className="flex items-start gap-4">
                   <div className="w-8 h-8 rounded-full bg-white text-emerald-600 flex items-center justify-center shrink-0 shadow-sm border border-emerald-50">
                      <ShieldCheck className="w-4 h-4" />
                   </div>
                   <div>
                      <h4 className="text-[12px] font-bold text-slate-800 mb-0.5">{t.feature1Title}</h4>
                      <p className="text-[10px] font-medium text-slate-500 leading-relaxed">{t.feature1Desc}</p>
                   </div>
                </div>

                <div className="flex items-start gap-4">
                   <div className="w-8 h-8 rounded-full bg-white text-emerald-600 flex items-center justify-center shrink-0 shadow-sm border border-emerald-50">
                      <Bell className="w-4 h-4" />
                   </div>
                   <div>
                      <h4 className="text-[12px] font-bold text-slate-800 mb-0.5">{t.feature2Title}</h4>
                      <p className="text-[10px] font-medium text-slate-500 leading-relaxed">{t.feature2Desc}</p>
                   </div>
                </div>

                <div className="flex items-start gap-4">
                   <div className="w-8 h-8 rounded-full bg-white text-emerald-600 flex items-center justify-center shrink-0 shadow-sm border border-emerald-50">
                      <Users className="w-4 h-4" />
                   </div>
                   <div>
                      <h4 className="text-[12px] font-bold text-slate-800 mb-0.5">{t.feature3Title}</h4>
                      <p className="text-[10px] font-medium text-slate-500 leading-relaxed">{t.feature3Desc}</p>
                   </div>
                </div>
             </div>
          </div>

          {/* Footer Note */}
          <div className="mt-8 flex items-start gap-3">
             <Lock className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
             <p className="text-[11px] font-medium text-slate-500 leading-relaxed">
                {t.secureNote}
             </p>
          </div>
       </div>

       {/* Right Column (Form) */}
       <div className="flex-1 p-4 sm:p-8 md:p-12 flex items-center justify-center bg-slate-50">
          <div className="w-full max-w-[640px] bg-white rounded-[2rem] shadow-sm border border-slate-200 p-8 sm:p-10">
             
             {/* Form Header */}
             <div className="flex items-center gap-5 mb-8">
                <div className="w-14 h-14 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
                   <User className="w-6 h-6 stroke-[2]" />
                </div>
                <div>
                   <h2 className="text-[22px] font-bold text-slate-800 mb-1">{t.createProfile}</h2>
                   <p className="text-[13px] text-slate-500 font-medium">{t.createSubtitle}</p>
                </div>
             </div>

             {/* Google OAuth */}
             <button type="button" onClick={() => { localStorage.setItem('sukoon_name', 'Google User'); router.push('/dashboard') }} className="w-full bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-[13px] font-bold py-3.5 rounded-xl flex items-center justify-center gap-3 transition-colors shadow-sm mb-8">
                <svg viewBox="0 0 24 24" className="w-5 h-5">
                   <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                   <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                   <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                   <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                {t.google}
             </button>

             {/* OAuth Divider */}
             <div className="relative mb-8">
                <div className="absolute inset-0 flex items-center">
                   <div className="w-full border-t border-slate-200"></div>
                </div>
                <div className="relative flex justify-center text-[11px] font-bold">
                   <span className="bg-white px-3 text-slate-400 tracking-wider">{t.or}</span>
                </div>
             </div>

             {/* Form Fields */}
             <div className="space-y-6">
                
                {/* Row 1: Name & Age */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                   <div className="space-y-2">
                      <label className="text-[12px] font-bold text-slate-800 block">{t.fullName} <span className="text-red-500">*</span></label>
                      <div className="relative">
                         <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                            <User className="w-4 h-4 text-slate-400" />
                         </div>
                         <input 
                           type="text" 
                           value={fullName}
                           onChange={(e) => setFullName(e.target.value)}
                           placeholder={t.fullNamePl} 
                           className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" 
                         />
                      </div>
                   </div>
                   <div className="space-y-2">
                      <label className="text-[12px] font-bold text-slate-800 block">{t.age} <span className="text-red-500">*</span></label>
                      <div className="relative">
                         <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                            <Calendar className="w-4 h-4 text-slate-400" />
                         </div>
                         <input 
                           type="text" 
                           value={age}
                           onChange={(e) => setAge(e.target.value)}
                           placeholder={t.agePl} 
                           className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" 
                         />
                      </div>
                   </div>
                </div>

                {/* Profile Picture Upload */}
                <div className="space-y-2">
                   <label className="text-[12px] font-bold text-slate-800 block">{t.picture}</label>
                   <div className="flex items-center gap-5">
                      <div className="w-20 h-20 rounded-2xl bg-slate-50 border border-slate-200 border-dashed flex items-center justify-center text-slate-400 shrink-0 hover:bg-slate-100 transition-colors cursor-pointer">
                         <Camera className="w-6 h-6" />
                      </div>
                      <div>
                         <h4 className="text-[12px] font-bold text-slate-800 mb-1">{t.upload}</h4>
                         <p className="text-[10px] text-slate-500 font-medium mb-3">{t.maxSize}</p>
                         <button className="px-4 py-1.5 rounded-md border border-emerald-600 text-emerald-600 text-[11px] font-bold hover:bg-emerald-50 transition-colors">
                            Choose File
                         </button>
                      </div>
                   </div>
                </div>

                {/* Row 2: Mobile & Email */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                   <div className="space-y-2">
                      <label className="text-[12px] font-bold text-slate-800 block">{t.mobile} <span className="text-red-500">*</span></label>
                      <div className="relative">
                         <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                            <Phone className="w-4 h-4 text-slate-400" />
                         </div>
                         <input 
                           type="text" 
                           value={mobile}
                           onChange={(e) => setMobile(e.target.value)}
                           placeholder={t.mobilePl} 
                           className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" 
                         />
                      </div>
                   </div>
                   <div className="space-y-2">
                      <label className="text-[12px] font-bold text-slate-800 block">{t.email}</label>
                      <div className="relative">
                         <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                            <Mail className="w-4 h-4 text-slate-400" />
                         </div>
                          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder={t.emailPl} className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" />
                      </div>
                   </div>
                </div>

                {/* Password */}
                <div className="space-y-2">
                   <label className="text-[12px] font-bold text-slate-800 block">{t.password} <span className="text-red-500">*</span></label>
                   <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                         <Lock className="w-4 h-4 text-slate-400" />
                      </div>
                      <input 
                        type="password" 
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="••••••••" 
                        className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" 
                      />
                   </div>
                </div>

                {/* Row 3: City & State */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                   <div className="space-y-2">
                      <label className="text-[12px] font-bold text-slate-800 block">{t.city} <span className="text-red-500">*</span></label>
                      <div className="relative">
                         <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                            <MapPin className="w-4 h-4 text-slate-400" />
                         </div>
                         <input 
                           type="text" 
                           value={city}
                           onChange={(e) => setCity(e.target.value)}
                           placeholder={t.cityPl} 
                           className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" 
                         />
                      </div>
                   </div>
                   <div className="space-y-2">
                      <label className="text-[12px] font-bold text-slate-800 block">{t.state}</label>
                      <div className="relative">
                         <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                            <Map className="w-4 h-4 text-slate-400" />
                         </div>
                         <input type="text" placeholder={t.statePl} className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" />
                      </div>
                   </div>
                </div>

                {/* Language Dropdown */}
                <div className="space-y-2">
                   <label className="text-[12px] font-bold text-slate-800 block">{t.prefLang}</label>
                   <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                         <Globe className="w-4 h-4 text-slate-500" />
                      </div>
                      <select 
                         aria-label="Preferred Language"
                         value={language}
                         onChange={(e) => setLanguage(e.target.value)}
                         className="w-full pl-10 pr-10 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors appearance-none cursor-pointer"
                      >
                         <option value="Bengali">Bengali</option>
                         <option value="English">English</option>
                         <option value="Hindi">Hindi</option>
                         <option value="Kannada">Kannada</option>
                         <option value="Malayalam">Malayalam</option>
                         <option value="Marathi">Marathi</option>
                         <option value="Tamil">Tamil</option>
                         <option value="Telugu">Telugu</option>
                         <option value="Urdu">Urdu</option>
                      </select>
                      <div className="absolute inset-y-0 right-0 pr-3.5 flex items-center pointer-events-none">
                         <ChevronDown className="w-4 h-4 text-slate-400" />
                      </div>
                   </div>
                </div>

                {/* Privacy Banner */}
                <div className="bg-[#f0fdf4] rounded-xl p-4 border border-[#dcfce7] flex items-start gap-4 mt-8">
                   <div className="w-8 h-8 rounded-full bg-white text-emerald-600 flex items-center justify-center shrink-0 shadow-sm border border-emerald-50">
                      <ShieldCheck className="w-4 h-4" />
                   </div>
                   <div>
                      <h4 className="text-[12px] font-bold text-emerald-800 mb-1">{t.privacy}</h4>
                      <p className="text-[10px] font-medium text-slate-500 leading-relaxed pr-4">
                         {t.privacyDesc}
                      </p>
                   </div>
                </div>

                {/* Action Area */}
                <div className="pt-4 flex flex-col items-center">
                   {error && (
                     <div className="text-red-500 text-xs font-bold mb-3">{error}</div>
                   )}
                   <button onClick={handleContinue} className="w-full max-w-[400px] bg-[#059669] hover:bg-[#047857] text-white text-[13px] font-bold py-3.5 rounded-xl flex items-center justify-center gap-2 transition-colors shadow-md shadow-emerald-600/20">
                      {t.continueBtn} <ChevronRight className="w-4 h-4" />
                   </button>
                   <p className="text-[10px] text-slate-400 font-medium mt-4">
                      {t.update}
                   </p>
                </div>

             </div>
          </div>
       </div>
    </div>
  )
}
