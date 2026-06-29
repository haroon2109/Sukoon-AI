export type VerdictType = "verified" | "misleading" | "false" | "🟢 Verified" | "🟡 Needs Context" | "🟠 Misleading" | "🔴 False" | "⚪ Unable to Verify";

export interface VerificationRecord {
  id: string;
  verdict: VerdictType;
  confidenceScore: number;
  claimSummary: string;
  evidenceFound?: string;
  aiExplanation?: string;
  actualFacts?: string;
  sourceCitations?: string[];
  peaceMessage?: string;
  mediaType?: "image" | "video";
  mediaUrl?: string;
}

export const mockVerifications: VerificationRecord[] = [
  {
    id: "v_101",
    verdict: "false",
    confidenceScore: 99,
    claimSummary: "RBI has issued new Rs 1000 notes and banned Rs 2000 notes immediately.",
    evidenceFound: "Database match found on the subject.",
    aiExplanation: "The AI has analyzed the evidence and found the claim to be verified based on the provided context.",
    mediaType: "image",
    mediaUrl: "/images/indian_currency.png"
  },
  {
    id: "v_102",
    verdict: "misleading",
    confidenceScore: 92,
    claimSummary: "Video shows heavy flooding and bridge collapse in Mumbai today due to monsoons.",
    actualFacts: "The video is authentic but it is from 2017 floods in a different state. Mumbai is currently experiencing normal monsoon showers with no reported bridge collapses.",
    sourceCitations: ["ndma.gov.in", "twitter.com/mybmc"],
    peaceMessage: "Stay calm. This footage is years old. Your city's infrastructure is currently secure. Rely on the BMC and local news for real-time weather updates.",
    mediaType: "image",
    mediaUrl: "/images/flood_mumbai.png"
  },
  {
    id: "v_103",
    verdict: "verified",
    confidenceScore: 98,
    claimSummary: "Government has announced a new PM Surya Ghar Muft Bijli Yojana for rooftop solar panels.",
    actualFacts: "This claim is true. The Indian Government recently launched the PM Surya Ghar scheme offering subsidies for installing rooftop solar panels to provide up to 300 units of free electricity.",
    sourceCitations: ["pmsuryaghar.gov.in", "pib.gov.in"],
    peaceMessage: "This is a legitimate government initiative. You can safely explore the official portal to check your eligibility for the solar subsidy.",
    mediaType: "image",
    mediaUrl: "/images/rooftop_solar.png"
  },
  {
    id: "v_104",
    verdict: "false",
    confidenceScore: 97,
    claimSummary: "Drinking hot lemon water cures COVID-19 and kills the virus in the throat.",
    actualFacts: "There is absolutely no scientific evidence that drinking hot lemon water cures COVID-19 or any viral infection. It can soothe a sore throat but does not kill the virus.",
    sourceCitations: ["who.int/mythbusters", "mohfw.gov.in"],
    peaceMessage: "Please rely on verified medical professionals for health advice. Home remedies are comforting but they are not cures for viruses.",
    mediaType: "image",
    mediaUrl: "/images/hot_lemon_water.png"
  },
  {
    id: "v_105",
    verdict: "misleading",
    confidenceScore: 89,
    claimSummary: "Supreme Court has cancelled all pending traffic challans for 2024.",
    actualFacts: "The Supreme Court has not issued a blanket cancellation of traffic challans. Certain states occasionally hold Lok Adalats to settle pending challans at a reduced penalty, but they are not 'cancelled' automatically.",
    sourceCitations: ["sci.gov.in", "echallan.parivahan.gov.in"],
    peaceMessage: "Don't fall for this viral text. You should check your vehicle status on the official Parivahan website and settle dues through proper channels.",
    mediaType: "image",
    mediaUrl: "/images/traffic_challan.png"
  },
  {
    id: "v_106",
    verdict: "false",
    confidenceScore: 99,
    claimSummary: "UNESCO has declared India's National Anthem as the best in the world.",
    actualFacts: "UNESCO has explicitly clarified multiple times over the past decade that it has never held any such competition or made any such declaration about any national anthem.",
    sourceCitations: ["unesco.org", "google.com"],
    peaceMessage: "We can be proud of our National Anthem without needing fake international awards. This is a very old internet hoax.",
    mediaType: "image",
    mediaUrl: "/images/unesco_anthem.png"
  },
  {
    id: "v_107",
    verdict: "verified",
    confidenceScore: 96,
    claimSummary: "Aadhaar cards must be updated every 10 years for biometrics and address proof.",
    actualFacts: "This is true. UIDAI recommends updating Aadhaar details, especially biometrics and demographic data, every 10 years to ensure accuracy.",
    sourceCitations: ["uidai.gov.in"],
    peaceMessage: "This is a standard administrative procedure. You can easily update your details online or at your nearest Aadhaar Seva Kendra.",
    mediaType: "image",
    mediaUrl: "/images/biometric_scan.png"
  },
  {
    id: "v_108",
    verdict: "false",
    confidenceScore: 98,
    claimSummary: "A new Whatsapp tracking rule means three blue ticks indicate the government is reading your messages.",
    actualFacts: "WhatsApp uses end-to-end encryption. The government cannot read your messages. There is no 'three blue ticks' feature on WhatsApp; two blue ticks simply mean the message was read by the recipient.",
    sourceCitations: ["whatsapp.com/security", "pib.gov.in"],
    peaceMessage: "Your private conversations remain secure and encrypted. Please do not spread fear about surveillance based on fake tick marks.",
    mediaType: "image",
    mediaUrl: "/images/whatsapp_ticks.png"
  },
  {
    id: "v_109",
    verdict: "misleading",
    confidenceScore: 91,
    claimSummary: "Video shows massive protests happening right now at India Gate against new labor laws.",
    actualFacts: "The video shows a real protest, but it took place in 2012, not today. Current live feeds of India Gate show normal tourist activity and no protests.",
    sourceCitations: ["delhipolice.gov.in", "boomlive.in"],
    peaceMessage: "It's easy to get anxious when seeing protest footage. Rest assured, the current situation in the capital is peaceful and normal.",
    mediaType: "image",
    mediaUrl: "/images/protest_india_gate.png"
  },
  {
    id: "v_110",
    verdict: "verified",
    confidenceScore: 99,
    claimSummary: "The newly inaugurated Chenab Bridge in Jammu & Kashmir is the highest railway bridge in the world.",
    actualFacts: "This claim is true. At 359 meters above the river bed, the Chenab Railway Bridge is officially the highest railway bridge globally, surpassing the Eiffel Tower in height.",
    sourceCitations: ["indianrailways.gov.in"],
    peaceMessage: "This is a verified engineering marvel. You can confidently share this positive news about India's infrastructure development."
  },
  {
    id: "v_111",
    verdict: "false",
    confidenceScore: 98,
    claimSummary: "The Indian government is providing free laptops to all students in 2024 via a specific link.",
    actualFacts: "There is no central government scheme giving free laptops to all students via WhatsApp links. These links are phishing scams designed to steal personal data.",
    sourceCitations: ["pib.gov.in/factcheck", "cybercrime.gov.in"],
    peaceMessage: "Protect your personal information. Never click on unverified links offering free electronics. Report the sender to help stop the scam."
  },
  {
    id: "v_112",
    verdict: "misleading",
    confidenceScore: 94,
    claimSummary: "TATA group is offering a free car to celebrate Ratan Tata's birthday. Click link to claim.",
    actualFacts: "TATA group has repeatedly denied running any such promotion. The accompanying image of a car giveaway is from a completely unrelated dealership event in 2019.",
    sourceCitations: ["tata.com/newsroom", "twitter.com/tatacompanies"],
    peaceMessage: "This is a common phishing tactic. Corporate giveaways are never conducted through random WhatsApp forwards. Stay safe online."
  },
  {
    id: "v_113",
    verdict: "verified",
    confidenceScore: 95,
    claimSummary: "ISRO has successfully launched the Aditya-L1 mission to study the Sun.",
    actualFacts: "True. The Indian Space Research Organisation (ISRO) successfully launched the Aditya-L1 solar observatory mission from Sriharikota.",
    sourceCitations: ["isro.gov.in"],
    peaceMessage: "This is verified factual news. It's a great moment for Indian space exploration that you can proudly share."
  },
  {
    id: "v_114",
    verdict: "false",
    confidenceScore: 99,
    claimSummary: "Eating onions and sleeping with them in your socks cures all diseases by drawing out toxins.",
    actualFacts: "This is an old myth with zero scientific backing. Onions do not draw 'toxins' out of the body through the feet, nor do they cure diseases.",
    sourceCitations: ["who.int", "healthline.com"],
    peaceMessage: "While onions are a healthy food, they aren't magical cures. Always consult a real doctor for medical issues rather than relying on folklore."
  },
  {
    id: "v_115",
    verdict: "misleading",
    confidenceScore: 90,
    claimSummary: "A new toll tax rule states that if your waiting time is over 3 minutes, the toll is free.",
    actualFacts: "The NHAI issued guidelines in 2021 stating that toll plazas should ensure service times of under 10 seconds per vehicle. There is a 'yellow line' rule, but there is no official '3-minute' blanket free rule.",
    sourceCitations: ["nhai.gov.in", "pib.gov.in"],
    peaceMessage: "While NHAI strives to reduce wait times, demanding a free pass after 3 minutes based on this forward may lead to unnecessary conflicts at toll booths."
  },
  {
    id: "v_116",
    verdict: "false",
    confidenceScore: 100,
    claimSummary: "The RBI governor has resigned immediately following a secret government meeting.",
    actualFacts: "The RBI Governor has not resigned. The official RBI website and major financial news outlets confirm he is still actively discharging his duties.",
    sourceCitations: ["rbi.org.in", "reuters.com/india"],
    peaceMessage: "Financial rumors are designed to cause market panic. Take a breath. Our economic institutions are functioning normally."
  },
  {
    id: "v_117",
    verdict: "verified",
    confidenceScore: 96,
    claimSummary: "FASTag KYC must be updated to avoid deactivation of the tag.",
    actualFacts: "True. The National Highways Authority of India (NHAI) has mandated the update of KYC details for FASTags to ensure seamless toll collection.",
    sourceCitations: ["nhai.gov.in", "hmis.nhai.org"],
    peaceMessage: "This is a legitimate requirement. Ensure your vehicle's FASTag KYC is complete to avoid any travel disruptions."
  },
  {
    id: "v_118",
    verdict: "misleading",
    confidenceScore: 88,
    claimSummary: "This specific brand of packaged salt contains crushed glass and stones.",
    actualFacts: "The viral video showing 'glass' dissolving in water is actually just large salt crystals taking time to dissolve. FSSAI has tested the specific brand and found it safe for consumption.",
    sourceCitations: ["fssai.gov.in", "google.com"],
    peaceMessage: "Don't let food panic ruin your day. The food safety authorities monitor these brands, and the 'glass' is simply natural sea salt."
  },
  {
    id: "v_119",
    verdict: "false",
    confidenceScore: 97,
    claimSummary: "Holding your breath for 10 seconds is a reliable test to prove you don't have lung damage or COVID.",
    actualFacts: "Holding your breath does not diagnose lung health or any viral infection. Many people with severe lung conditions can hold their breath, while healthy people may struggle.",
    sourceCitations: ["who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters"],
    peaceMessage: "Please do not use unverified breath tests for medical diagnoses. If you feel unwell, visit a local clinic for proper testing."
  },
  {
    id: "v_120",
    verdict: "verified",
    confidenceScore: 99,
    claimSummary: "The UPI transaction limit for educational and medical institutions has been increased to Rs 5 lakh.",
    actualFacts: "This is true. The RBI raised the limit for UPI payments to hospitals and educational institutions from Rs 1 lakh to Rs 5 lakh to facilitate larger essential payments.",
    sourceCitations: ["rbi.org.in", "npci.org.in"],
    peaceMessage: "This is official financial policy. It's safe to utilize this higher limit for your essential medical or educational needs."
  }
];

export const getRandomVerification = (): VerificationRecord => {
  const randomIndex = Math.floor(Math.random() * mockVerifications.length);
  return mockVerifications[randomIndex];
};
