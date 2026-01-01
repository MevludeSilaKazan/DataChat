from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Header, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import io
import pandas as pd

from app.services.db_service import DatabaseManager
from app.services.llm_service import SQLAgentService
from app.services.session_manager import session_store

app = FastAPI(title="DataChat API", version="1.2 - Enterprise")
# --- CORS AYARLARI (YENİ) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme aşamasında herkese izin veriyoruz
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, DELETE vb. hepsi serbest
    allow_headers=["*"],  # Tüm başlıklara (Header) izin ver
)
# --- Bağımlılıklar (Dependencies) ---

async def get_session_id(x_session_id: Optional[str] = Header(None)) -> str:
    """İstek başlığından Session ID'yi okur ve doğrular."""
    if not x_session_id:
        raise HTTPException(status_code=401, detail="X-Session-ID başlığı eksik. Önce /session/start yapın.")
    
    session = session_store.get_session(x_session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Geçersiz veya süresi dolmuş oturum.")
    return x_session_id

def get_db_manager(session_id: str = Depends(get_session_id)) -> DatabaseManager:
    """Geçerli oturumun veritabanı yöneticisini getirir."""
    session = session_store.get_session(session_id)
    if not session or not session.db_manager:
        raise HTTPException(status_code=400, detail="Bu oturum için henüz dosya yüklenmedi veya DB bağlanmadı.")
    return session.db_manager

# --- Modeller ---

class QueryRequest(BaseModel):
    question: str

class ExportRequest(BaseModel):
    sql: str
    format: str = "excel" # "excel" veya "csv"

# --- Endpointler ---

@app.post("/session/start")
async def start_session():
    """Yeni bir kullanıcı oturumu başlatır."""
    session_id = session_store.create_session()
    return {
        "status": "success", 
        "session_id": session_id, 
        "message": "Oturum başlatıldı. X-Session-ID başlığını sonraki isteklerde kullanın."
    }

@app.delete("/session/end")
async def end_session(session_id: str = Depends(get_session_id)):
    """Oturumu sonlandırır ve kaynakları (RAM/DB bağlantısı) temizler."""
    session_store.close_session(session_id)
    return {"status": "success", "message": "Oturum kapatıldı."}

@app.post("/upload/file")
async def upload_file(
    file: UploadFile = File(...), 
    session_id: str = Depends(get_session_id)
):
    """Oturuma özel Excel/CSV dosyası yükler."""
    content = await file.read()
    
    try:
        # 1. Dosyadan Geçici DB oluştur
        temp_manager, engine = DatabaseManager.from_file(content, file.filename)
        # Engine referansını sakla (Memory DB olduğu için garbage collector silmesin)
        temp_manager.engine = engine
        
        # 2. Bu manager'ı oturuma kaydet
        session_store.set_db_for_session(session_id, temp_manager)
        
        schema = temp_manager.get_schema_info()
        return {"status": "success", "message": "Dosya analiz edildi", "schema_preview": schema}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/connect/database")
async def connect_database(
    connection_url: str = Form(...),
    session_id: str = Depends(get_session_id)
):
    """Mevcut bir SQL veritabanına bağlanır."""
    try:
        new_manager = DatabaseManager(connection_string=connection_url)
        # Bağlantı testi için şemayı çek
        schema = new_manager.get_schema_info()
        
        # Oturuma kaydet
        session_store.set_db_for_session(session_id, new_manager)
        
        return {"status": "success", "message": "Veritabanı bağlandı", "schema_preview": schema}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bağlantı hatası: {str(e)}")

@app.post("/chat")
async def chat_with_data(
    request: QueryRequest,
    session_id: str = Depends(get_session_id)
):
    """Aktif oturumdaki veriyle sohbet eder (Hafızalı)."""
    
    # Session nesnesini al (History'e erişmek için)
    session = session_store.get_session(session_id)
    if not session or not session.db_manager:
        raise HTTPException(status_code=400, detail="Önce veri kaynağı bağlayın.")

    # Ajanı geçmiş konuşmalarla (history) birlikte başlat
    agent_service = SQLAgentService(session.db_manager, history=session.history)
    
    try:
        response = agent_service.process_request(request.question)
        
        # Eğer ajan history'yi güncellediyse, session'a kaydet
        if "history_update" in response:
            session.history = response["history_update"]
            # Frontend'e history objesini göndermeye gerek yok, temizle
            del response["history_update"]
            
        return response
    except Exception as e:
        return {"error": str(e)}

@app.post("/export/result")
async def export_query_result(
    request: ExportRequest,
    db_manager: DatabaseManager = Depends(get_db_manager)
):
    """Belirli bir SQL sonucunu Excel veya CSV dosyası olarak indirir."""
    
    try:
        # SQL'i tekrar çalıştır (Cache olmadığı için)
        result = db_manager.execute_safe_query(request.sql)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        data = result.get("data", [])
        if not data:
            raise HTTPException(status_code=404, detail="Sorgu boş sonuç döndürdü.")

        df = pd.DataFrame(data)
        stream = io.BytesIO()
        
        if request.format == "csv":
            df.to_csv(stream, index=False)
            media_type = "text/csv"
            filename = "sonuc.csv"
        else:
            # Excel export
            df.to_excel(stream, index=False, engine='openpyxl')
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            filename = "sonuc.xlsx"
            
        stream.seek(0)
        
        return StreamingResponse(
            stream, 
            media_type=media_type, 
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Geliştirme ortamı için reload açık
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)