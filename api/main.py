"""
Crypto Compatibility FastAPI Main App
Farcaster Mini App için ana uygulama
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from .personality import PersonalityAnalyzer
from .comedy_generator import ComedyGenerator
from .matching import MatchmakerAI
from .frame_builder import FrameBuilder

# Ortam değişkenlerini yükle
load_dotenv()

# FastAPI uygulaması
app = FastAPI(
    title="Crypto Compatibility",
    description="AI-Powered Crypto Dating for Farcaster",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Componentleri initialize et
personality_analyzer = PersonalityAnalyzer()
comedy_generator = ComedyGenerator()
matchmaker = MatchmakerAI()
frame_builder = FrameBuilder()


# ============== ANA ENDPOINTS ==============

@app.get("/", response_class=HTMLResponse)
async def root():
    """Ana sayfa / İlk frame"""
    return frame_builder.build_initial_frame()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}


@app.post("/api/frame/analyze")
async def analyze_personality(request: Request):
    """
    Kullanıcının crypto kişiliğini analiz eder
    Farcaster'dan gelen frame tıklamasını işler
    """
    try:
        # Farcaster frame verisini al
        data = await request.json()
        fid = data.get("untrustedData", {}).get("fid", 12345)  # Demo FID
        
        # Kişilik analizi yap
        personality_data = personality_analyzer.analyze_from_fid(fid)
        
        # Komedi üret
        commentary = comedy_generator.generate_personality_reveal(personality_data)
        
        # Sonuç frame'i oluştur
        result_frame = frame_builder.build_personality_result_frame(personality_data)
        
        return HTMLResponse(content=result_frame)
    
    except Exception as e:
        print(f"Error in analyze: {e}")
        return HTMLResponse(content=frame_builder.build_initial_frame())


@app.post("/api/frame/matches")
async def find_matches(request: Request):
    """
    Kullanıcı için en uyumlu kişileri bulur
    """
    try:
        data = await request.json()
        fid = data.get("untrustedData", {}).get("fid", 12345)
        
        # Kullanıcı verisini al
        user_data = personality_analyzer.analyze_from_fid(fid)
        
        # Eşleşmeleri bul
        matches = matchmaker.find_matches(fid, num_matches=3)
        
        # Her eşleşme için komedi üret
        for match in matches:
            match['comedy'] = comedy_generator.generate_match_commentary(
                user_data,
                match,
                match['compatibility']
            )
        
        # Eşleşme frame'i oluştur
        matches_frame = frame_builder.build_matches_frame(matches, user_data)
        
        return HTMLResponse(content=matches_frame)
    
    except Exception as e:
        print(f"Error in matches: {e}")
        return HTMLResponse(content=frame_builder._build_no_matches_frame())


@app.post("/api/frame/match-detail")
async def match_detail(request: Request):
    """Detaylı eşleşme raporu"""
    try:
        data = await request.json()
        user_fid = data.get("untrustedData", {}).get("fid", 12345)
        match_fid = data.get("match_fid", 67890)
        
        # Detaylı rapor al
        report = matchmaker.get_detailed_match_report(user_fid, match_fid)
        
        # Komedi ekle
        report['comedy'] = comedy_generator.generate_match_commentary(
            report['user1'],
            report['user2'],
            report['compatibility']
        )
        
        return JSONResponse(content=report)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/personality/{fid}")
async def get_personality(fid: int):
    """Kullanıcı kişiliğini al (API endpoint)"""
    try:
        personality = personality_analyzer.analyze_from_fid(fid)
        return JSONResponse(content=personality)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/compatibility/{fid1}/{fid2}")
async def calculate_compatibility(fid1: int, fid2: int):
    """İki kullanıcı arasında uyumluluk hesapla"""
    try:
        report = matchmaker.get_detailed_match_report(fid1, fid2)
        
        # Komedi ekle
        report['comedy'] = comedy_generator.generate_match_commentary(
            report['user1'],
            report['user2'],
            report['compatibility']
        )
        
        return JSONResponse(content=report)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/generate-image/personality/{personality_type}")
async def generate_personality_image(personality_type: str):
    """
    Kişilik için görsel üret
    Production'da: Gerçek görsel üretimi veya cache'lenmiş görseller
    """
    # TODO: Gerçek görsel üretimi (PIL, Pillow, veya harici API)
    return {"message": "Image generation endpoint", "type": personality_type}


@app.get("/api/generate-image/match/{fid1}/{fid2}")
async def generate_match_image(fid1: int, fid2: int):
    """Eşleşme için görsel üret"""
    # TODO: Gerçek görsel üretimi
    return {"message": "Match image generation", "fids": [fid1, fid2]}


@app.get("/api/leaderboard")
async def get_leaderboard():
    """En yüksek uyumluluklar leaderboard'u"""
    # TODO: Database'den gerçek leaderboard
    return {
        "top_matches": [
            {"user1": "@alice", "user2": "@bob", "score": 96.5},
            {"user1": "@charlie", "user2": "@diana", "score": 94.2},
            {"user1": "@eve", "user2": "@frank", "score": 92.8}
        ]
    }


# ============== DEPLOYMENT HANDLER (Vercel için) ==============

# Vercel serverless fonksiyon handler'ı
handler = app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )