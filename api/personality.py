"""
Crypto Personality Analyzer
Kullanıcının crypto kişiliğini analiz eder
"""

from typing import Dict, List, Optional
from enum import Enum
import random

class CryptoPersonality(str, Enum):
    BITCOIN_MAXI = "bitcoin_maxi"
    DEFI_DEGEN = "defi_degen"
    NFT_CONNOISSEUR = "nft_connoisseur"
    SHITCOIN_SURFER = "shitcoin_surfer"
    CRYPTO_BOOMER = "crypto_boomer"
    ETH_ENTHUSIAST = "eth_enthusiast"
    MEME_LORD = "meme_lord"
    DAO_ARCHITECT = "dao_architect"
    WHALE_WATCHER = "whale_watcher"
    PRIVACY_MAXIMALIST = "privacy_maximalist"


PERSONALITY_PROFILES = {
    "bitcoin_maxi": {
        "name": "Bitcoin Purist 🟠",
        "description": "Sadece BTC, diğerleri shitcoin! Güven sorunları var ama en sağlam ilişkileri kurar.",
        "traits": ["loyal", "conservative", "skeptical", "long_term"],
        "token_preference": ["BTC"],
        "risk_tolerance": 30,
        "fun_fact": "İlk date'te Lightning Network anlatır",
        "dating_style": "Yavaş ama garantili - 'Not your keys, not your heart' mantığı",
        "ideal_match": ["eth_enthusiast", "crypto_boomer"],
        "avoid": ["shitcoin_surfer", "defi_degen"]
    },
    "defi_degen": {
        "name": "DeFi Degenerate 🦄",
        "description": "Yield farming bağımlısı! APY %10,000 gördüğünde kalp atışları hızlanır.",
        "traits": ["risky", "adventurous", "FOMO", "24_7_trader"],
        "token_preference": ["UNI", "AAVE", "CRV", "random_tokens"],
        "risk_tolerance": 95,
        "fun_fact": "Gas fee'yi date bütçesinden yüksek tutar",
        "dating_style": "Hızlı ve riskli - 'Farm and dump' stratejisi",
        "ideal_match": ["shitcoin_surfer", "meme_lord"],
        "avoid": ["bitcoin_maxi", "crypto_boomer"]
    },
    "nft_connoisseur": {
        "name": "NFT Sanat Sevdalısı 🎨",
        "description": "Her NFT bir hikaye anlatır. Floor price'a bakmaz, vibes'a bakar.",
        "traits": ["artistic", "cultured", "trend_setter", "community_focused"],
        "token_preference": ["ETH", "APE", "LOOKS"],
        "risk_tolerance": 60,
        "fun_fact": "Profile pic'i gerçek fotoğrafından değerli",
        "dating_style": "Estetik ve anlamlı - 'Mint your love' felsefesi",
        "ideal_match": ["eth_enthusiast", "dao_architect"],
        "avoid": ["bitcoin_maxi", "shitcoin_surfer"]
    },
    "shitcoin_surfer": {
        "name": "Shitcoin Avcısı 🏄",
        "description": "Her yeni token potansiyel 100x! Portföyü bir roulette masası.",
        "traits": ["gambler", "optimistic", "impulsive", "moonboy"],
        "token_preference": ["yeni_tokenlar", "meme_coins", "random_gems"],
        "risk_tolerance": 99,
        "fun_fact": "Telegram gruplarında 'wen moon' sorar",
        "dating_style": "Hızlı giriş-çıkış - 'Pump and dump love'",
        "ideal_match": ["defi_degen", "meme_lord"],
        "avoid": ["crypto_boomer", "bitcoin_maxi"]
    },
    "crypto_boomer": {
        "name": "Crypto Boomer 👔",
        "description": "Sadece top 10 coin! Risk sevmez, diversification ister.",
        "traits": ["conservative", "careful", "rational", "long_term"],
        "token_preference": ["BTC", "ETH", "top_10_only"],
        "risk_tolerance": 20,
        "fun_fact": "Coinbase'den başka exchange kullanmaz",
        "dating_style": "Geleneksel ve güvenli - 'HODL my heart'",
        "ideal_match": ["bitcoin_maxi", "eth_enthusiast"],
        "avoid": ["defi_degen", "shitcoin_surfer"]
    },
    "eth_enthusiast": {
        "name": "Ethereum Hayranı ⟠",
        "description": "Smart contract aşkı! Her şey Ethereum'da çözülür.",
        "traits": ["tech_savvy", "innovative", "ecosystem_believer", "builder"],
        "token_preference": ["ETH", "layer2s", "ETH_ecosystem"],
        "risk_tolerance": 50,
        "fun_fact": "Gas fee'ler için ayrı bütçe tutar",
        "dating_style": "Akıllı ve sürdürülebilir - 'Merge our hearts'",
        "ideal_match": ["nft_connoisseur", "dao_architect"],
        "avoid": ["bitcoin_maxi"]
    },
    "meme_lord": {
        "name": "Meme Coin Kralı 🐕",
        "description": "Dogecoin millionaire olacaktı ama tam zamanında satmadı. Her şey meme!",
        "traits": ["funny", "community_driven", "viral_hunter", "ironic"],
        "token_preference": ["DOGE", "SHIB", "PEPE", "latest_meme"],
        "risk_tolerance": 85,
        "fun_fact": "Elon'un tweetlerini bildirimle takip eder",
        "dating_style": "Eğlenceli ve viral - 'To the moon together'",
        "ideal_match": ["shitcoin_surfer", "defi_degen"],
        "avoid": ["crypto_boomer", "privacy_maximalist"]
    },
    "dao_architect": {
        "name": "DAO Mimarı 🏛️",
        "description": "Decentralization her şeydir! Relationship'i de DAO olarak yönetir.",
        "traits": ["democratic", "organized", "visionary", "community_first"],
        "token_preference": ["governance_tokens", "UNI", "COMP"],
        "risk_tolerance": 55,
        "fun_fact": "İlk date önerisini governance proposal olarak sunar",
        "dating_style": "Demokratik ve şeffaf - 'Vote for love'",
        "ideal_match": ["eth_enthusiast", "nft_connoisseur"],
        "avoid": ["bitcoin_maxi", "meme_lord"]
    },
    "whale_watcher": {
        "name": "Balina Gözlemcisi 🐋",
        "description": "Whale hareketlerini takip eder, büyük oyunculara göre pozisyon alır.",
        "traits": ["analytical", "strategic", "patient", "data_driven"],
        "token_preference": ["top_caps", "whale_holdings"],
        "risk_tolerance": 40,
        "fun_fact": "Etherscan'i Instagram'dan çok açar",
        "dating_style": "Stratejik ve hesaplı - 'Follow the big money'",
        "ideal_match": ["crypto_boomer", "eth_enthusiast"],
        "avoid": ["shitcoin_surfer", "meme_lord"]
    },
    "privacy_maximalist": {
        "name": "Privacy Maksimalist 🥷",
        "description": "Anonim kal, güvenli ol! Monero her şeyin çözümü.",
        "traits": ["private", "paranoid", "security_focused", "anonymous"],
        "token_preference": ["XMR", "ZEC", "privacy_coins"],
        "risk_tolerance": 35,
        "fun_fact": "İlk buluşmaya VPN ile gelir",
        "dating_style": "Gizli ve güvenli - 'Anonymous love'",
        "ideal_match": ["bitcoin_maxi", "crypto_boomer"],
        "avoid": ["meme_lord", "nft_connoisseur"]
    }
}


class PersonalityAnalyzer:
    """Kullanıcının crypto kişiliğini analiz eder"""
    
    def __init__(self):
        self.profiles = PERSONALITY_PROFILES
    
    def analyze_from_fid(self, fid: int, user_data: Optional[Dict] = None) -> Dict:
        """
        Farcaster ID'den kişilik analizi yapar
        Gerçek uygulamada: user'ın cast history, follows, reactions analiz edilir
        """
        # Demo için: Random kişilik atama (gerçekte AI analiz yapılır)
        personality_type = random.choice(list(CryptoPersonality))
        profile = self.profiles[personality_type.value]
        
        return {
            "fid": fid,
            "personality_type": personality_type.value,
            "profile": profile,
            "analysis": self._generate_detailed_analysis(profile)
        }
    
    def _generate_detailed_analysis(self, profile: Dict) -> Dict:
        """Detaylı kişilik analizi üretir"""
        return {
            "strengths": self._get_strengths(profile),
            "weaknesses": self._get_weaknesses(profile),
            "dating_tips": self._get_dating_tips(profile),
            "compatibility_factors": {
                "token_preferences": profile["token_preference"],
                "risk_tolerance": profile["risk_tolerance"],
                "traits": profile["traits"]
            }
        }
    
    def _get_strengths(self, profile: Dict) -> List[str]:
        """Kişiliğin güçlü yönleri"""
        strength_map = {
            "loyal": "Sadık ve güvenilir",
            "adventurous": "Cesur ve risk almaktan korkmaz",
            "artistic": "Yaratıcı ve estetik anlayışı yüksek",
            "funny": "Espritüel ve eğlenceli",
            "democratic": "Adil ve şeffaf",
            "analytical": "Stratejik düşünür",
            "private": "Güvenliğe önem verir"
        }
        return [strength_map.get(trait, trait.replace("_", " ").title()) 
                for trait in profile["traits"][:3]]
    
    def _get_weaknesses(self, profile: Dict) -> List[str]:
        """Kişiliğin zayıf yönleri"""
        weakness_map = {
            "skeptical": "Çok şüpheci olabilir",
            "FOMO": "FOMO nedeniyle aceleci kararlar alır",
            "impulsive": "Düşünmeden hareket eder",
            "conservative": "Yeniliklere kapalı",
            "paranoid": "Aşırı tedbirli ve güvensiz"
        }
        return [weakness_map.get(trait, f"Bazen {trait.replace('_', ' ')}")
                for trait in profile["traits"][-2:]]
    
    def _get_dating_tips(self, profile: Dict) -> List[str]:
        """Kişiliğe özel dating tavsiyeleri"""
        return [
            f"{profile['name']} için ideal ilk buluşma: {profile['fun_fact']}",
            f"Dating style: {profile['dating_style']}",
            f"En uyumlu tipler: {', '.join(profile['ideal_match'])}"
        ]
    
    def calculate_compatibility(self, user1_profile: Dict, user2_profile: Dict) -> Dict:
        """İki kullanıcı arasında uyumluluk hesaplar"""
        
        # Token preference compatibility (30%)
        token_score = self._calculate_token_compatibility(
            user1_profile["token_preference"],
            user2_profile["token_preference"]
        ) * 0.30
        
        # Risk tolerance compatibility (25%)
        risk_score = self._calculate_risk_compatibility(
            user1_profile["risk_tolerance"],
            user2_profile["risk_tolerance"]
        ) * 0.25
        
        # Trait compatibility (20%)
        trait_score = self._calculate_trait_compatibility(
            user1_profile["traits"],
            user2_profile["traits"]
        ) * 0.20
        
        # Ideal match bonus (15%)
        match_bonus = self._calculate_ideal_match_bonus(
            user1_profile.get("ideal_match", []),
            user2_profile.get("ideal_match", []),
            user1_profile.get("avoid", []),
            user2_profile.get("avoid", [])
        ) * 0.15
        
        # Community engagement (10%)
        community_score = random.uniform(0.7, 1.0) * 0.10
        
        total_score = (token_score + risk_score + trait_score + 
                      match_bonus + community_score) * 100
        
        return {
            "total_score": round(total_score, 1),
            "breakdown": {
                "token_preferences": round(token_score * 100 / 0.30, 1),
                "risk_tolerance": round(risk_score * 100 / 0.25, 1),
                "personality_traits": round(trait_score * 100 / 0.20, 1),
                "ideal_match_factor": round(match_bonus * 100 / 0.15, 1),
                "community_vibe": round(community_score * 100 / 0.10, 1)
            },
            "interpretation": self._interpret_score(total_score)
        }
    
    def _calculate_token_compatibility(self, tokens1: List, tokens2: List) -> float:
        """Token tercih uyumluluğu"""
        # Aynı tokenlar varsa yüksek skor
        common = set(tokens1) & set(tokens2)
        if common:
            return 0.9
        # Alakalı ekosistemler
        if any(t in ["BTC"] for t in tokens1) and any(t in ["BTC"] for t in tokens2):
            return 0.8
        return 0.5
    
    def _calculate_risk_compatibility(self, risk1: int, risk2: int) -> float:
        """Risk toleransı uyumluluğu"""
        diff = abs(risk1 - risk2)
        if diff < 10:
            return 1.0
        elif diff < 30:
            return 0.7
        else:
            return 0.4
    
    def _calculate_trait_compatibility(self, traits1: List, traits2: List) -> float:
        """Karakter özelliği uyumluluğu"""
        common = set(traits1) & set(traits2)
        return len(common) / max(len(traits1), len(traits2))
    
    def _calculate_ideal_match_bonus(self, ideal1: List, ideal2: List, 
                                     avoid1: List, avoid2: List) -> float:
        """İdeal eşleşme bonus puanı"""
        # Birbirinin ideal listesinde mi?
        if any(x in ideal1 for x in ideal2) or any(x in ideal2 for x in ideal1):
            return 1.0
        # Birbirinin avoid listesinde mi?
        if any(x in avoid1 for x in avoid2) or any(x in avoid2 for x in avoid1):
            return 0.3
        return 0.6
    
    def _interpret_score(self, score: float) -> str:
        """Skor yorumlama"""
        if score >= 90:
            return "🔥 MÜKEMMEL EŞLEŞME - Siz ikisi için yazılmışsınız!"
        elif score >= 80:
            return "💕 ÇOK UYUMLU - Harika bir çift olabilirsiniz!"
        elif score >= 70:
            return "✨ İYİ POTANSİYEL - Birbirinizi tanımaya değer!"
        elif score >= 60:
            return "🤝 ORTA DÜZEY - Arkadaş olarak başlayın belki?"
        else:
            return "🤷 FARKLI DÜNYALAR - Ama opposites attract derler!"