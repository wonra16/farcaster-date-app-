"""
Farcaster Frame Builder
Dynamic frame HTML üretir
"""

from typing import Dict, Optional
import os

class FrameBuilder:
    """Farcaster Frame oluşturucu"""
    
    def __init__(self):
        self.app_url = os.getenv("APP_URL", "https://your-app.vercel.app")
    
    def build_initial_frame(self) -> str:
        """İlk frame: Başlangıç ekranı"""
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Compatibility</title>
    
    <!-- Farcaster Frame Meta Tags -->
    <meta property="fc:frame" content="vNext" />
    <meta property="fc:frame:image" content="{self.app_url}/static/images/start.png" />
    <meta property="fc:frame:button:1" content="🔍 Kişiliğimi Keşfet!" />
    <meta property="fc:frame:button:2" content="💕 Kiminle Uyumluyum?" />
    <meta property="fc:frame:post_url" content="{self.app_url}/api/frame/analyze" />
    
    <!-- Open Graph -->
    <meta property="og:title" content="Crypto Compatibility" />
    <meta property="og:description" content="Crypto kişiliğini keşfet, soulmate'ini bul!" />
    <meta property="og:image" content="{self.app_url}/static/images/start.png" />
    
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            color: white;
        }}
        .container {{
            text-align: center;
            padding: 2rem;
        }}
        h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
        }}
        p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Crypto Compatibility</h1>
        <p>Crypto kişiliğini keşfet, soulmate'ini bul!</p>
    </div>
</body>
</html>"""
    
    def build_personality_result_frame(self, personality_data: Dict) -> str:
        """Kişilik sonuç frame'i"""
        profile = personality_data['profile']
        
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kişiliğin: {profile['name']}</title>
    
    <!-- Farcaster Frame Meta Tags -->
    <meta property="fc:frame" content="vNext" />
    <meta property="fc:frame:image" content="{self.app_url}/api/generate-image/personality/{personality_data['personality_type']}" />
    <meta property="fc:frame:button:1" content="💕 Eşleşmeleri Gör" />
    <meta property="fc:frame:button:2" content="🔄 Tekrar Dene" />
    <meta property="fc:frame:button:3" content="📤 Paylaş" />
    <meta property="fc:frame:post_url" content="{self.app_url}/api/frame/matches" />
    
    <!-- Open Graph -->
    <meta property="og:title" content="Ben bir {profile['name']}!" />
    <meta property="og:description" content="{profile['description']}" />
    <meta property="og:image" content="{self.app_url}/api/generate-image/personality/{personality_data['personality_type']}" />
    
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 2rem;
            color: white;
        }}
        .result {{
            max-width: 600px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 20px;
        }}
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        .description {{
            font-size: 1.1rem;
            line-height: 1.6;
            margin: 1rem 0;
        }}
        .fun-fact {{
            background: rgba(255,255,255,0.2);
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1rem;
        }}
    </style>
</head>
<body>
    <div class="result">
        <h1>{profile['name']}</h1>
        <p class="description">{profile['description']}</p>
        <div class="fun-fact">
            <strong>Fun Fact:</strong> {profile['fun_fact']}
        </div>
        <div class="fun-fact">
            <strong>Dating Style:</strong> {profile['dating_style']}
        </div>
    </div>
</body>
</html>"""
    
    def build_matches_frame(self, matches: list, user_data: Dict) -> str:
        """Eşleşme sonuçları frame'i"""
        
        if not matches:
            return self._build_no_matches_frame()
        
        top_match = matches[0]
        score = top_match['compatibility']['total_score']
        
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>En İyi Eşleşmen!</title>
    
    <!-- Farcaster Frame Meta Tags -->
    <meta property="fc:frame" content="vNext" />
    <meta property="fc:frame:image" content="{self.app_url}/api/generate-image/match/{user_data['fid']}/{top_match['fid']}" />
    <meta property="fc:frame:button:1" content="📊 Detaylı Analiz" />
    <meta property="fc:frame:button:2" content="➡️ Sonraki Eşleşme" />
    <meta property="fc:frame:button:3" content="📤 Paylaş" />
    <meta property="fc:frame:post_url" content="{self.app_url}/api/frame/match-detail" />
    
    <!-- Open Graph -->
    <meta property="og:title" content="{top_match['username']} ile %{score} uyumluyum!" />
    <meta property="og:description" content="Crypto soulmate'imi buldum! 🚀" />
    <meta property="og:image" content="{self.app_url}/api/generate-image/match/{user_data['fid']}/{top_match['fid']}" />
    
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            padding: 2rem;
            color: #333;
        }}
        .match-card {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .score {{
            font-size: 4rem;
            font-weight: bold;
            color: #fa709a;
            text-align: center;
        }}
        .match-name {{
            font-size: 2rem;
            text-align: center;
            margin: 1rem 0;
        }}
        .compatibility-breakdown {{
            margin: 1.5rem 0;
        }}
        .compat-item {{
            display: flex;
            justify-content: space-between;
            margin: 0.5rem 0;
            padding: 0.5rem;
            background: #f8f9fa;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="match-card">
        <div class="score">{score}%</div>
        <div class="match-name">{top_match['username']}</div>
        <p style="text-align: center; font-size: 1.2rem;">
            {top_match['profile']['name']}
        </p>
        <div class="compatibility-breakdown">
            <h3>Uyumluluk Detayları:</h3>
            {"".join([f'<div class="compat-item"><span>{k}</span><span>{v}%</span></div>' 
                     for k, v in top_match['compatibility']['breakdown'].items()])}
        </div>
    </div>
</body>
</html>"""
    
    def _build_no_matches_frame(self) -> str:
        """Eşleşme bulunamadı frame'i"""
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Henüz Eşleşme Yok</title>
    <meta property="fc:frame" content="vNext" />
    <meta property="fc:frame:image" content="{self.app_url}/static/images/no-matches.png" />
    <meta property="fc:frame:button:1" content="🔄 Tekrar Dene" />
    <meta property="fc:frame:post_url" content="{self.app_url}/api/frame/analyze" />
</head>
<body>
    <div style="text-align: center; padding: 3rem;">
        <h1>😅 Henüz Eşleşme Bulamadık</h1>
        <p>Ama üzülme! Daha fazla kullanıcı katıldıkça eşleşmeler artacak! 🚀</p>
    </div>
</body>
</html>"""
    
    def build_share_frame(self, share_data: Dict) -> str:
        """Paylaşım frame'i"""
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Sonuçlarımı Paylaşıyorum!</title>
    
    <meta property="fc:frame" content="vNext" />
    <meta property="fc:frame:image" content="{self.app_url}/api/generate-image/share/{share_data['fid']}" />
    <meta property="fc:frame:button:1" content="🔍 Ben de Dene" />
    <meta property="fc:frame:post_url" content="{self.app_url}/api/frame/start" />
    
    <meta property="og:title" content="{share_data['text']}" />
    <meta property="og:image" content="{self.app_url}/api/generate-image/share/{share_data['fid']}" />
</head>
<body>
    <div style="text-align: center; padding: 2rem;">
        <h1>🎉 Paylaşıldı!</h1>
        <p>Arkadaşların da deneyebilir!</p>
    </div>
</body>
</html>"""