import axios from 'axios';

// 1. Çevresel değişkeni al
let apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// 2. Render bazen sadece "datachat.onrender.com" verir.
// Eğer başında "http" yoksa ve localhost değilse, biz ekleyelim.
if (!apiBaseUrl.startsWith('http') && !apiBaseUrl.startsWith('//')) {
  apiBaseUrl = `https://${apiBaseUrl}`;
}

// 3. Sonunda "/" varsa onu da temizleyelim (Garanti olsun)
if (apiBaseUrl.endsWith('/')) {
  apiBaseUrl = apiBaseUrl.slice(0, -1);
}

console.log("🔗 Bağlanılan Backend Adresi:", apiBaseUrl); // Konsolda görebilmek için

const API_BASE_URL = apiBaseUrl;

// Axios örneği oluşturuyoruz
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- TİP TANIMLAMALARI (Types) ---
// Backend'den gelecek verilerin şablonu

export interface SessionResponse {
  status: string;
  session_id: string;
  message: string;
}

export interface SchemaResponse {
  status: string;
  message: string;
  schema_preview: string;
}

export interface VizSuggestion {
  type: 'bar' | 'line' | 'pie' | 'table';
  x_key?: string;
  y_key?: string;
  label_key?: string;
  value_key?: string;
  title?: string;
  explanation?: string;
}

export interface ChatResponse {
  sql?: string;
  result?: {
    data: any[];
    count: number;
  };
  visualization?: VizSuggestion;
  error?: string;
}

// --- API FONKSİYONLARI ---

export const apiService = {
  
  // 1. Yeni Oturum Başlat
  startSession: async (): Promise<SessionResponse> => {
    const response = await apiClient.post<SessionResponse>('/session/start');
    return response.data;
  },

  // 2. Dosya Yükle (Excel/CSV)
  uploadFile: async (file: File, sessionId: string): Promise<SchemaResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post<SchemaResponse>('/upload/file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'X-Session-ID': sessionId, // Backend'in istediği Header
      },
    });
    return response.data;
  },

  // 3. Veritabanı Bağla
  connectDatabase: async (connectionString: string, sessionId: string): Promise<SchemaResponse> => {
    const formData = new FormData();
    formData.append('connection_url', connectionString);

    const response = await apiClient.post<SchemaResponse>('/connect/database', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded', // Form verisi
        'X-Session-ID': sessionId,
      },
    });
    return response.data;
  },

  // 4. Sohbet Et
  chat: async (question: string, sessionId: string): Promise<ChatResponse> => {
    const response = await apiClient.post<ChatResponse>('/chat', 
      { question }, 
      {
        headers: { 'X-Session-ID': sessionId },
      }
    );
    return response.data;
  },

  // 5. Excel/CSV İndir
  exportResult: async (sql: string, format: 'excel' | 'csv', sessionId: string) => {
    const response = await apiClient.post('/export/result', 
      { sql, format },
      {
        headers: { 'X-Session-ID': sessionId },
        responseType: 'blob', // Dosya indireceğimiz için blob formatı şart
      }
    );

    // Tarayıcıda indirme işlemini tetikleyen yardımcı kod
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    // Dosya adını belirle
    link.setAttribute('download', `sonuc.${format === 'excel' ? 'xlsx' : 'csv'}`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },
  
  // 6. Oturumu Kapat
  endSession: async (sessionId: string) => {
    await apiClient.delete('/session/end', {
      headers: { 'X-Session-ID': sessionId },
    });
  }
};
