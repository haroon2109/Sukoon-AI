import Link from "next/link";
import { ArrowLeft, Heart, Feather, Flower2, Sparkles, Sun, Star, MoonStar, Cross, Leaf } from "lucide-react";

const quotes = [
  // Hinduism
  { religion: "Hinduism", text: "May there be peace in the heavens, peace in the atmosphere, peace on the earth. Let there be coolness, let there be calmness.", source: "Atharva Veda", icon: <Sun className="w-6 h-6 text-amber-600" /> },
  { religion: "Hinduism", text: "When a man has no desires and is free from longing… then he attains peace.", source: "Bhagavad Gita", icon: <Sun className="w-6 h-6 text-amber-600" /> },
  { religion: "Hinduism", text: "The whole world is one family.", source: "Maha Upanishad", icon: <Sun className="w-6 h-6 text-amber-600" /> },
  { religion: "Hinduism", text: "Let us move together, speak together, let our minds be in harmony.", source: "Rig Veda", icon: <Sun className="w-6 h-6 text-amber-600" /> },
  { religion: "Hinduism", text: "Lead me from the unreal to the real, lead me from darkness to light, lead me from death to immortality. Peace, Peace, Peace.", source: "Brihadaranyaka Upanishad", icon: <Sun className="w-6 h-6 text-amber-600" /> },

  // Islam
  { religion: "Islam", text: "O you who have believed, enter into peace completely and perfectly and do not follow the footsteps of division.", source: "Quran 2:208", icon: <MoonStar className="w-6 h-6 text-emerald-600" /> },
  { religion: "Islam", text: "The servants of the Most Merciful are those who walk upon the earth easily, and when the ignorant address them harshly, they say words of peace.", source: "Quran 25:63", icon: <MoonStar className="w-6 h-6 text-emerald-600" /> },
  { religion: "Islam", text: "Do you know what is better than charity and fasting and prayer? It is keeping peace and good relations between people.", source: "Hadith", icon: <MoonStar className="w-6 h-6 text-emerald-600" /> },
  { religion: "Islam", text: "O mankind, We created you from a male and a female and made you into nations and tribes so that you may know one another.", source: "Qur’an 49:13", icon: <MoonStar className="w-6 h-6 text-emerald-600" /> },
  { religion: "Islam", text: "None of you truly believes until he wishes for his brother what he wishes for himself.", source: "Hadith (Bukhari)", icon: <MoonStar className="w-6 h-6 text-emerald-600" /> },

  // Christianity
  { religion: "Christianity", text: "Blessed are the peacemakers, for they will be called children of God.", source: "Matthew 5:9", icon: <Cross className="w-6 h-6 text-sky-600" /> },
  { religion: "Christianity", text: "Peace I leave with you; my peace I give you. I do not give to you as the world gives. Do not let your hearts be troubled.", source: "John 14:27", icon: <Cross className="w-6 h-6 text-sky-600" /> },
  { religion: "Christianity", text: "If it is possible, as far as it depends on you, live at peace with everyone.", source: "Romans 12:18", icon: <Cross className="w-6 h-6 text-sky-600" /> },
  { religion: "Christianity", text: "Let us therefore make every effort to do what leads to peace and to mutual edification.", source: "Romans 14:19", icon: <Cross className="w-6 h-6 text-sky-600" /> },
  { religion: "Christianity", text: "Make every effort to live in peace with everyone and to be holy; without holiness no one will see the Lord.", source: "Hebrews 12:14", icon: <Cross className="w-6 h-6 text-sky-600" /> },

  // Buddhism
  { religion: "Buddhism", text: "Peace comes from within. Do not seek it without.", source: "Buddha", icon: <Flower2 className="w-6 h-6 text-rose-600" /> },
  { religion: "Buddhism", text: "Better than a thousand hollow words, is one word that brings peace.", source: "Dhammapada", icon: <Flower2 className="w-6 h-6 text-rose-600" /> },
  { religion: "Buddhism", text: "Hatred is never appeased by hatred in this world; by non-hatred alone is hatred appeased. This is a law eternal.", source: "Dhammapada", icon: <Flower2 className="w-6 h-6 text-rose-600" /> },
  { religion: "Buddhism", text: "Those who are free of resentful thoughts surely find peace.", source: "Buddha", icon: <Flower2 className="w-6 h-6 text-rose-600" /> },
  { religion: "Buddhism", text: "Radiate boundless love towards the entire world—above, below, and across—unhindered, without ill will, without enmity.", source: "Metta Sutta", icon: <Flower2 className="w-6 h-6 text-rose-600" /> },

  // Sikhism
  { religion: "Sikhism", text: "No one is my enemy, and no one is a stranger. I get along with everyone.", source: "Guru Granth Sahib", icon: <Heart className="w-6 h-6 text-orange-600" /> },
  { religion: "Sikhism", text: "The world is burning in the fire of desire, O Lord, save it by Your Grace.", source: "Guru Amar Das", icon: <Heart className="w-6 h-6 text-orange-600" /> },
  { religion: "Sikhism", text: "Where there is forgiveness, there is God Himself.", source: "Kabir", icon: <Heart className="w-6 h-6 text-orange-600" /> },
  { religion: "Sikhism", text: "Recognize the whole human race as one.", source: "Guru Gobind Singh", icon: <Heart className="w-6 h-6 text-orange-600" /> },
  { religion: "Sikhism", text: "Before you claim to be a Muslim, a Sikh, a Hindu, or a Christian, be a human first.", source: "Guru Nanak", icon: <Heart className="w-6 h-6 text-orange-600" /> },

  // Jainism
  { religion: "Jainism", text: "All living, sentient creatures should not be slain, nor treated with violence, nor abused, nor tormented.", source: "Acharanga Sutra", icon: <Leaf className="w-6 h-6 text-indigo-600" /> },
  { religion: "Jainism", text: "Non-violence is the highest religion.", source: "Ahimsa Paramo Dharma", icon: <Leaf className="w-6 h-6 text-indigo-600" /> },
  { religion: "Jainism", text: "Do not injure, abuse, oppress, enslave, insult, torment, torture, or kill any creature or living being.", source: "Mahavira", icon: <Leaf className="w-6 h-6 text-indigo-600" /> },
  { religion: "Jainism", text: "Have compassion towards all living beings. Hatred leads to destruction.", source: "Mahavira", icon: <Leaf className="w-6 h-6 text-indigo-600" /> },
  { religion: "Jainism", text: "A man is seated on top of a tree in the midst of a burning forest. He sees all living beings perish. But he doesn't realize that the same fate is soon to overtake him.", source: "Uttaradhyayana Sutra", icon: <Leaf className="w-6 h-6 text-indigo-600" /> }
];

export default function PeaceQuotesPage() {

  return (
    <div className="min-h-screen bg-stone-50 text-slate-900 pb-20 font-sans selection:bg-teal-100">
      <nav className="bg-white/80 backdrop-blur-md border-b border-slate-200/60 sticky top-0 z-50">
        <div className="max-w-[1400px] mx-auto px-6 h-16 flex items-center">
          <Link href="/dashboard" className="flex items-center gap-2 text-slate-500 hover:text-teal-700 font-medium transition-colors text-sm tracking-wide">
            <ArrowLeft className="w-4 h-4" /> BACK TO DASHBOARD
          </Link>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-6 pt-16">
        <div className="text-center max-w-3xl mx-auto mb-20">
          <span className="text-xs font-bold uppercase tracking-[0.2em] text-teal-700 block mb-4">Unity In Diversity</span>
          <h1 className="text-4xl md:text-5xl font-serif text-slate-900 mb-6 leading-tight">
            Universal Harmony
          </h1>
          <p className="text-lg text-slate-500 font-light leading-relaxed">
            Sukoon means peace. Across time and geography, every major philosophy and faith has anchored itself to a singular, profound truth: that we are deeply connected, and our highest purpose is to live in harmony.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {[...quotes].sort((a, b) => a.religion.localeCompare(b.religion)).map((quote, idx) => (
            <div 
              key={idx} 
              className="bg-white p-10 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100/50 hover:shadow-[0_8px_40px_rgb(0,0,0,0.08)] hover:-translate-y-1 transition-all duration-500 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center gap-4 mb-8">
                  <div className="p-3 bg-slate-50 rounded-2xl">
                    {quote.icon}
                  </div>
                  <span className="text-xs font-bold uppercase tracking-widest text-slate-400">
                    {quote.religion}
                  </span>
                </div>
                
                <p className="text-xl text-slate-700 font-serif leading-relaxed mb-8">
                  "{quote.text}"
                </p>
              </div>

              <div className="pt-6 border-t border-slate-100 flex items-center justify-between">
                <span className="text-sm font-medium text-teal-700">
                  {quote.source}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-20 text-center p-12 bg-teal-900 rounded-3xl text-stone-50 shadow-xl">
          <Feather className="w-10 h-10 mx-auto mb-6 text-teal-200 opacity-80" />
          <h2 className="text-2xl font-serif mb-3">Verify before you share.</h2>
          <p className="text-teal-200/80 font-light tracking-wide">Protecting our peace is a shared responsibility.</p>
        </div>
      </div>
    </div>
  );
}
