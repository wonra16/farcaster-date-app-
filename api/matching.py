"""
Matching Algorithm
Kullanıcıları eşleştiren ana algoritma
"""

from typing import Dict, List, Optional
import random
from .personality import PersonalityAnalyzer, PERSONALITY_PROFILES

class MatchmakerAI:
    """Akıllı eşleştirme motoru"""
    
    def __init__(self):
        self.analyzer = PersonalityAnalyzer()
        self.cache = {}  # Basit cache (production'da Redis kullan)
    
    def find_matches(self, user_fid: int, num_matches: int = 3) -> List[Dict]:
        """
        Kullanıcı için en uyumlu kişileri bulur
        Gerçek uygulamada: Farcaster social graph kullanılır
        """
        
        # Kullanıcının kişiliğini analiz et
        user_analysis = self.analyzer.analyze_from_fid(user_fid)
        
        # Potansiyel eşleşmeleri bul (Demo: random FIDs)
        potential_matches = self._get_potential_matches(user_fid)
        
        # Her potansiyel eşleşme için uyumluluk hesapla
        scored_matches = []
        for match_fid in potential_matches[:10]:  # İlk 10'u değerlendir
            match_analysis = self.analyzer.analyze_from_fid(match_fid)
            
            compatibility = self.analyzer.calculate_compatibility(
                user_analysis['profile'],
                match_analysis['profile']
            )
            
            scored_matches.append({
                "fid": match_fid,
                "username": f"@user{match_fid}",  # Gerçekte Farcaster API'den
                "profile": match_analysis['profile'],
                "compatibility": compatibility
            })
        
        # Skora göre sırala ve top N'i al
        scored_matches.sort(key=lambda x: x['compatibility']['total_score'], reverse=True)
        
        return scored_matches[:num_matches]
    
    def _get_potential_matches(self, user_fid: int) -> List[int]:
        """
        Potansiyel eşleşmeleri getirir
        Gerçek uygulamada: Farcaster social graph, followers, following
        """
        # Demo için random FIDs
        return [random.randint(1000, 9999) for _ in range(20)]
    
    def get_detailed_match_report(self, user1_fid: int, user2_fid: int) -> Dict:
        """İki kullanıcı için detaylı eşleşme raporu"""
        
        user1 = self.analyzer.analyze_from_fid(user1_fid)
        user2 = self.analyzer.analyze_from_fid(user2_fid)
        
        compatibility = self.analyzer.calculate_compatibility(
            user1['profile'],
            user2['profile']
        )
        
        return {
            "user1": {
                "fid": user1_fid,
                "personality": user1['profile']['name'],
                "description": user1['profile']['description']
            },
            "user2": {
                "fid": user2_fid,
                "personality": user2['profile']['name'],
                "description": user2['profile']['description']
            },
            "compatibility": compatibility,
            "strengths": self._identify_relationship_strengths(user1, user2),
            "challenges": self._identify_relationship_challenges(user1, user2),
            "advice": self._generate_relationship_advice(user1, user2, compatibility)
        }
    
    def _identify_relationship_strengths(self, user1: Dict, user2: Dict) -> List[str]:
        """İlişkinin güçlü yönleri"""
        strengths = []
        
        # Ortak tokenlar
        common_tokens = set(user1['profile']['token_preference']) & set(user2['profile']['token_preference'])
        if common_tokens:
            strengths.append(f"Ortak token sevgisi: {', '.join(common_tokens)}")
        
        # Benzer risk seviyesi
        risk_diff = abs(user1['profile']['risk_tolerance'] - user2['profile']['risk_tolerance'])
        if risk_diff < 20:
            strengths.append("Uyumlu risk toleransı - mali kararlar kolay!")
        
        # Ortak özellikler
        common_traits = set(user1['profile']['traits']) & set(user2['profile']['traits'])
        if common_traits:
            strengths.append(f"Ortak özellikler: {len(common_traits)} adet!")
        
        return strengths
    
    def _identify_relationship_challenges(self, user1: Dict, user2: Dict) -> List[str]:
        """İlişkinin zorlukları"""
        challenges = []
        
        # Farklı risk seviyeleri
        risk_diff = abs(user1['profile']['risk_tolerance'] - user2['profile']['risk_tolerance'])
        if risk_diff > 50:
            challenges.append("Çok farklı risk seviyeleri - ape vs hodl tartışmaları olabilir!")
        
        # Avoid listesinde mi?
        if user2['personality_type'] in user1['profile'].get('avoid', []):
            challenges.append("Farklı crypto felsefeleriniz var - ama tam da bu sizi ilginç kılıyor!")
        
        # Farklı tokenlar
        tokens1 = set(user1['profile']['token_preference'])
        tokens2 = set(user2['profile']['token_preference'])
        if not (tokens1 & tokens2):
            challenges.append("Hiç ortak tokenınız yok - diversification çok iyi olur!")
        
        return challenges
    
    def _generate_relationship_advice(self, user1: Dict, user2: Dict, compat: Dict) -> List[str]:
        """İlişki tavsiyeleri"""
        score = compat['total_score']
        advice = []
        
        if score >= 80:
            advice.append("Harika uyum! Birlikte bir crypto projesi başlatın! 🚀")
            advice.append("İkiniz için custom ENS domain alın: couple.eth 💕")
        elif score >= 60:
            advice.append("İyi potansiyel! Birlikte portfolio review yapın 📊")
            advice.append("Farklılıklarınız sizi tamamlıyor - birbirinden öğrenin! 📚")
        else:
            advice.append("Arkadaş olarak başlayın, DeFi'yi birlikte öğrenin! 🤝")
            advice.append("Opposites attract - belki tam da ihtiyacınız olan bu! 💫")
        
        return advice