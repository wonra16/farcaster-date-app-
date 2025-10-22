"""
AI Comedy Generator
OpenAI GPT-4 kullanarak komik yorumlar üretir
"""

import os
from openai import OpenAI
from typing import Dict, List
import random

class ComedyGenerator:
    """AI destekli komedi üretim motoru"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.comedy_templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Hazır komedi şablonları"""
        return {
            "high_compatibility": [
                "İkiniz de {trait} - birlikte {activity}! 💕",
                "{user1} ve {user2}: Crypto'nun Romeo ve Juliet'i! 🎭",
                "Bu uyum {comparison} gibi mükemmel! ✨"
            ],
            "low_compatibility": [
                "İkiniz {difference} - ama opposites attract! 🤷",
                "{user1} {type1}, {user2} {type2} - ilginç kombinasyon! 😅",
                "Bu ilişki {risk_description} - riskli ama heyecanlı! 🎢"
            ],
            "token_jokes": [
                "İkiniz de {token} tutuyorsunuz - evlilik teklifi token transfer'le mi olacak? 💍",
                "{token1} vs {token2} - klasik aşk üçgeni! 💔",
                "Gas fee'niz uyumlu - birlikte mint yapmaya hazırsınız! ⛽"
            ],
            "risk_jokes": [
                "Risk toleransı: {score}% - ikiniz de anadan doğma degen! 🎰",
                "{user1} diamond hands, {user2} paper hands - dengeli portföy! 📊",
                "İkiniz de {risk_level} - rekt olmak için hazır mısınız? 🔥"
            ],
            "date_ideas": [
                "İlk date önerim: {activity} 🎉",
                "Birlikte: {shared_activity} yapın! 💫",
                "İdeal buluşma: {location} 📍"
            ]
        }
    
    def generate_match_commentary(self, user1_data: Dict, user2_data: Dict, 
                                  compatibility: Dict) -> Dict:
        """
        İki kullanıcı için komik eşleşme yorumu üretir
        """
        score = compatibility["total_score"]
        
        # AI ile üretilen custom yorum
        ai_commentary = self._generate_ai_commentary(user1_data, user2_data, compatibility)
        
        # Template-based yorumlar
        template_jokes = self._generate_template_jokes(user1_data, user2_data, score)
        
        # Date fikirleri
        date_ideas = self._generate_date_ideas(user1_data, user2_data)
        
        return {
            "headline": self._generate_headline(score),
            "main_commentary": ai_commentary,
            "bullet_jokes": template_jokes,
            "date_ideas": date_ideas,
            "viral_snippet": self._generate_viral_snippet(user1_data, user2_data, score)
        }
    
    def _generate_ai_commentary(self, user1: Dict, user2: Dict, compat: Dict) -> str:
        """OpenAI GPT-4 ile custom komedi üretir"""
        
        try:
            prompt = f"""Sen bir crypto dating komedyenisin. İki Farcaster kullanıcısı için komik bir eşleşme yorumu yaz.

Kullanıcı 1: {user1['profile']['name']} - {user1['profile']['description']}
Kullanıcı 2: {user2['profile']['name']} - {user2['profile']['description']}

Uyumluluk Skoru: {compat['total_score']}%

Kurallar:
- Crypto insider şakaları kullan
- 2-3 cümle maksimum
- Emoji ekle
- Eğlenceli ve paylaşılabilir ol
- Türkçe yaz
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sen eğlenceli bir crypto dating komedyenisin."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.9
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            # Fallback: template kullan
            return self._fallback_commentary(user1, user2, compat['total_score'])
    
    def _fallback_commentary(self, user1: Dict, user2: Dict, score: float) -> str:
        """AI çalışmazsa template yorum"""
        templates = [
            f"{user1['profile']['name']} ve {user2['profile']['name']} - %{score} uyum! Crypto'nun en wholesome çifti olabilirsiniz! 💕",
            f"İkiniz de crypto'ya aşıksınız, birbirinize de %{score} aşıksınız! WAGMI together! 🚀",
            f"%{score} uyum... Bu rakamlar yalan söylemez! İkiniz için bullish'im! 📈"
        ]
        return random.choice(templates)
    
    def _generate_template_jokes(self, user1: Dict, user2: Dict, score: float) -> List[str]:
        """Template bazlı şakalar"""
        jokes = []
        
        # Token joke
        tokens1 = user1['profile']['token_preference'][:2]
        tokens2 = user2['profile']['token_preference'][:2]
        
        if set(tokens1) & set(tokens2):
            common = list(set(tokens1) & set(tokens2))[0]
            jokes.append(f"İkiniz de {common} tutuyorsunuz - wedding ring olarak NFT basın! 💍")
        else:
            jokes.append(f"{tokens1[0]} vs {tokens2[0]} - portföy diversification! 📊")
        
        # Risk joke
        risk1 = user1['profile']['risk_tolerance']
        risk2 = user2['profile']['risk_tolerance']
        avg_risk = (risk1 + risk2) / 2
        
        if avg_risk > 80:
            jokes.append(f"Risk toleransı: %{int(avg_risk)} - ikiniz de tam degen! Birlikte rekt olun! 🎰")
        elif avg_risk < 40:
            jokes.append(f"Risk toleransı: %{int(avg_risk)} - güvenli liman! HODL love! 🏦")
        else:
            jokes.append(f"Risk toleransı: %{int(avg_risk)} - balanced portfolio gibi ilişki! ⚖️")
        
        # Trait joke
        traits1 = set(user1['profile']['traits'])
        traits2 = set(user2['profile']['traits'])
        common_traits = traits1 & traits2
        
        if common_traits:
            trait = list(common_traits)[0].replace("_", " ")
            jokes.append(f"İkiniz de {trait} - bu uyum on-chain! ⛓️")
        
        return jokes
    
    def _generate_date_ideas(self, user1: Dict, user2: Dict) -> List[str]:
        """İdeal date fikirleri"""
        ideas = []
        
        # Kişiliklere göre custom fikirler
        personalities = [user1['personality_type'], user2['personality_type']]
        
        if 'defi_degen' in personalities:
            ideas.append("İlk date: Birlikte yield farming! APY avcılığı romantiktir! 🌾")
        
        if 'nft_connoisseur' in personalities:
            ideas.append("NFT gallery walk - Art Basel kadar fancy! 🎨")
        
        if 'bitcoin_maxi' in personalities:
            ideas.append("Romantik bir Bitcoin whitepaper okuma gecesi! 📄")
        
        if 'meme_lord' in personalities:
            ideas.append("Dogecoin meetup'ta buluşun - Elon gönderi atar belki! 🐕")
        
        # Genel fikirler
        general_ideas = [
            "ETH gas fee düşükken Uniswap'te token swap - en romantik date! ⛽",
            "DAO toplantısında tanışın - governance proposal: 'Date me' 🗳️",
            "Crypto conference'ta panel sonrası coffee - networking ama romantik! ☕",
            "Birlikte bir NFT mint edin - shared custody relationship! 🖼️"
        ]
        
        ideas.extend(random.sample(general_ideas, 2))
        
        return ideas[:3]
    
    def _generate_headline(self, score: float) -> str:
        """Ana başlık"""
        if score >= 90:
            return "🔥 ATEŞ UYUM! Crypto Soulmates!"
        elif score >= 80:
            return "💕 Harika Eşleşme! Bull Market Love!"
        elif score >= 70:
            return "✨ İyi Potansiyel! DYOR ama promising!"
        elif score >= 60:
            return "🤝 Orta Düzey! Paper hands değil, hold edin!"
        else:
            return "🤷 Farklı Vibe'lar! Ama diversification önemli!"
    
    def _generate_viral_snippet(self, user1: Dict, user2: Dict, score: float) -> str:
        """Paylaşım için viral snippet"""
        return f"""
🚀 CRYPTO COMPATIBILITY SONUÇLARI! 🚀

{user1['profile']['name']} 💫 {user2['profile']['name']}

Uyumluluk: %{score}

{self._fallback_commentary(user1, user2, score)}

Sen de dene! 👇
        """.strip()
    
    def generate_personality_reveal(self, user_data: Dict) -> str:
        """Kişilik açıklama metni"""
        profile = user_data['profile']
        
        try:
            prompt = f"""Sen bir crypto kişilik analisti ve komedyensin. Bu kişilik için eğlenceli bir açıklama yaz:

Kişilik: {profile['name']}
Açıklama: {profile['description']}
Özellikler: {', '.join(profile['traits'])}

Kurallar:
- 3-4 cümle
- Komik ve özgün
- Crypto insider şakalar
- Emoji kullan
- Türkçe yaz
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sen crypto komedyenisin."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.9
            )
            
            return response.choices[0].message.content.strip()
        
        except:
            return f"""
{profile['name']}

{profile['description']}

{profile['fun_fact']} 😄

{profile['dating_style']}
            """.strip()