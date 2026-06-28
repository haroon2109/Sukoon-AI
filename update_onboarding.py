import re

with open('frontend/src/app/onboarding/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

translations = """
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
"""

# Insert translations after exports
content = content.replace('export default function OnboardingPage() {', translations + '\nexport default function OnboardingPage() {')

# Add t mapping inside component
content = content.replace('const [error, setError] = useState("")', 'const [error, setError] = useState("")\n  const t = translations[language] || translations["English"]')

# Replace strings
content = content.replace('"Please fill in all mandatory fields to continue."', 't.errorMsg')
content = content.replace('Let\'s get to<br/>know you better', '{t.title}') 
content = content.replace("Help us personalize your experience and keep you informed about what matters most.", "{t.subtitle}")
content = content.replace(">Personalized Experience<", ">{t.feature1Title}<")
content = content.replace(">Get alerts and insights relevant to you.<", ">{t.feature1Desc}<")
content = content.replace(">Timely Alerts<", ">{t.feature2Title}<")
content = content.replace(">Stay informed about harmful content.<", ">{t.feature2Desc}<")
content = content.replace(">Safer Community<", ">{t.feature3Title}<")
content = content.replace(">Together, we build a peaceful digital world.<", ">{t.feature3Desc}<")

content = content.replace(
    'Your information is secure and<br/>never shared with anyone.', 
    '{t.secureNote}'
)

content = content.replace(">Create Your Profile<", ">{t.createProfile}<")
content = content.replace(">Just a few details to get you started.<", ">{t.createSubtitle}<")
content = content.replace("Sign up with Google", "{t.google}")
content = content.replace("OR REGISTER WITH EMAIL", "{t.or}")

# Form fields
content = content.replace(">Full Name <", ">{t.fullName} <")
content = content.replace('"Enter your full name"', "{t.fullNamePl}")
content = content.replace(">Age <", ">{t.age} <")
content = content.replace('"Enter your age"', "{t.agePl}")
content = content.replace(">Profile Picture<", ">{t.picture}<")
content = content.replace(">Upload a profile picture<", ">{t.upload}<")
content = content.replace(">JPG, PNG or WEBP. Max size 2MB.<", ">{t.maxSize}<")
content = content.replace(">Choose File<", ">{t.choose}<")

content = content.replace(">Mobile Number <", ">{t.mobile} <")
content = content.replace('"Enter your mobile number"', "{t.mobilePl}")
content = content.replace(">Email (Optional)<", ">{t.email}<")
content = content.replace('"Enter your email address"', "{t.emailPl}")
content = content.replace(">Create Password <", ">{t.password} <")
content = content.replace(">City <", ">{t.city} <")
content = content.replace('"Enter your city"', "{t.cityPl}")
content = content.replace(">State / Province (Optional)<", ">{t.state}<")
content = content.replace('"Enter your state or province"', "{t.statePl}")
content = content.replace(">Preferred Language<", ">{t.prefLang}<")

content = content.replace(">Your privacy matters<", ">{t.privacy}<")
content = content.replace("We only use your information to personalize your experience and keep you safe. You can change this anytime in settings.", "{t.privacyDesc}")
content = content.replace("Continue <", "{t.continueBtn} <")
content = content.replace("You can update these details anytime later.", "{t.update}")

with open('frontend/src/app/onboarding/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
