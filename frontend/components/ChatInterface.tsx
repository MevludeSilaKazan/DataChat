"use client";

import { useState, useEffect, useRef } from "react";
import { apiService, ChatResponse, VizSuggestion } from "@/services/api"; // veya "@/app/services/api"
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle, 
  DialogTrigger,
  DialogFooter
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Send, Paperclip, Database, FileSpreadsheet, Download, Loader2, Plug } from "lucide-react";

// Mesaj Tipi
interface Message {
  role: "user" | "assistant" | "system";
  content: string;
  sql?: string;
}

export default function ChatInterface() {
  const [sessionId, setSessionId] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  
  // Veri Sonuçları
  const [queryResult, setQueryResult] = useState<any[] | null>(null);
  const [lastSql, setLastSql] = useState<string>("");

  // DB Bağlantı Form State'leri
  const [isDbModalOpen, setIsDbModalOpen] = useState(false);
  const [dbConfig, setDbConfig] = useState({
    type: "postgresql", // Varsayılan
    host: "localhost",
    port: "5432",
    username: "",
    password: "",
    database: ""
  });

  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const initSession = async () => {
      try {
        const res = await apiService.startSession();
        setSessionId(res.session_id);
        setMessages([{ role: "system", content: "Hoşgeldin! Analiz için dosya yükle veya veritabanı bağla." }]);
      } catch (err) {
        console.error("Oturum hatası:", err);
      }
    };
    initSession();
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !sessionId) return;
    const userMsg = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setIsLoading(true);

    try {
      const response = await apiService.chat(userMsg, sessionId);
      if (response.error) {
        setMessages((prev) => [...prev, { role: "assistant", content: `Hata: ${response.error}` }]);
      } else {
        setMessages((prev) => [...prev, { role: "assistant", content: "Sonuçlar aşağıda:", sql: response.sql }]);
        if (response.result?.data) {
          setQueryResult(response.result.data);
          setLastSql(response.sql || "");
        }
      }
    } catch (error) {
      setMessages((prev) => [...prev, { role: "assistant", content: "Sunucu hatası." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0] || !sessionId) return;
    setIsUploading(true);
    const file = e.target.files[0];
    try {
      await apiService.uploadFile(file, sessionId);
      setMessages((prev) => [...prev, { role: "system", content: `Dosya yüklendi: ${file.name}.` }]);
    } catch (error) {
      setMessages((prev) => [...prev, { role: "system", content: "Yükleme başarısız." }]);
    } finally {
      setIsUploading(false);
    }
  };

  // Veritabanı Bağlantı Fonksiyonu
  const handleDbConnect = async () => {
    if (!sessionId) return;
    setIsUploading(true); // Yükleniyor animasyonu için kullanalım

    // 1. Connection String Oluşturma
    // Format: dialect+driver://username:password@host:port/database
    let connectionUrl = "";
    const { type, host, port, username, password, database } = dbConfig;

    if (type === "postgresql") {
  // Neon ve Bulut DB'ler için SSL modu zorunludur
  connectionUrl = `postgresql+psycopg2://${username}:${password}@${host}:${port}/${database}?sslmode=require`;
}else if (type === "mysql") {
      connectionUrl = `mysql+pymysql://${username}:${password}@${host}:${port}/${database}`;
    }

    try {
      await apiService.connectDatabase(connectionUrl, sessionId);
      setMessages((prev) => [...prev, { role: "system", content: `Veritabanına bağlanıldı: ${database} (${type})` }]);
      setIsDbModalOpen(false); // Modalı kapat
    } catch (error) {
      setMessages((prev) => [...prev, { role: "system", content: "Veritabanı bağlantısı başarısız. Bilgileri kontrol edin." }]);
    } finally {
      setIsUploading(false);
    }
  };

  const handleExport = async () => {
    if (!lastSql || !sessionId) return;
    try {
      await apiService.exportResult(lastSql, "excel", sessionId);
    } catch (error) {
      alert("İndirme hatası");
    }
  };

  return (
    <div className="flex h-[calc(100vh-100px)] w-full gap-4 p-4">
      {/* SOL PANEL */}
      <Card className="w-1/3 flex flex-col shadow-lg">
        <CardHeader className="bg-slate-50 border-b py-3">
          <CardTitle className="text-md font-medium flex items-center gap-2">
            <Database className="w-4 h-4 text-blue-600" /> Sohbet Asistanı
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 flex flex-col p-0 overflow-hidden">
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-4">
              {messages.map((msg, i) => (
                <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div className={`max-w-[90%] rounded-lg px-3 py-2 text-sm ${
                    msg.role === "user" ? "bg-blue-600 text-white" : 
                    msg.role === "system" ? "bg-yellow-50 text-yellow-800 border border-yellow-200" : 
                    "bg-slate-100 text-slate-800"
                  }`}>
                    {msg.content}
                    {msg.sql && <div className="mt-2 p-2 bg-slate-800 text-green-400 font-mono text-xs rounded">{msg.sql}</div>}
                  </div>
                </div>
              ))}
              <div ref={scrollRef} />
              {isLoading && <div className="text-xs text-slate-400 flex items-center gap-1"><Loader2 className="w-3 h-3 animate-spin"/> Yanıt bekleniyor...</div>}
            </div>
          </ScrollArea>

          {/* Input Alanı */}
          <div className="p-4 bg-white border-t space-y-3">
            <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex gap-2">
              <Input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Veriyle ilgili soru sor..." disabled={isLoading} />
              <Button type="submit" disabled={isLoading} size="icon"><Send className="w-4 h-4" /></Button>
            </form>
            
            <div className="flex items-center justify-between text-xs text-slate-500">
               {/* Dosya Yükleme */}
               <div className="flex gap-4">
                 <div className="flex items-center gap-2">
                   <input type="file" id="file-upload" className="hidden" accept=".csv, .xlsx" onChange={handleFileUpload} />
                   <label htmlFor="file-upload" className="flex items-center gap-1 cursor-pointer hover:text-blue-600">
                     <Paperclip className="w-3 h-3" /> Dosya
                   </label>
                 </div>

                 {/* Veritabanı Bağlama Butonu (Dialog Trigger) */}
                 <Dialog open={isDbModalOpen} onOpenChange={setIsDbModalOpen}>
                   <DialogTrigger asChild>
                     <button className="flex items-center gap-1 cursor-pointer hover:text-blue-600">
                       <Plug className="w-3 h-3" /> Veritabanı
                     </button>
                   </DialogTrigger>
                   <DialogContent>
                     <DialogHeader>
                       <DialogTitle>Veritabanı Bağlantısı</DialogTitle>
                     </DialogHeader>
                     
                     <div className="grid gap-4 py-4">
                       <div className="grid grid-cols-4 items-center gap-4">
                         <Label className="text-right">Tip</Label>
                         <Select 
                            value={dbConfig.type} 
                            onValueChange={(val) => setDbConfig({...dbConfig, type: val})}
                         >
                           <SelectTrigger className="col-span-3">
                             <SelectValue placeholder="Seçiniz" />
                           </SelectTrigger>
                           <SelectContent>
                             <SelectItem value="postgresql">PostgreSQL</SelectItem>
                             <SelectItem value="mysql">MySQL</SelectItem>
                           </SelectContent>
                         </Select>
                       </div>
                       <div className="grid grid-cols-4 items-center gap-4">
                         <Label className="text-right">Host</Label>
                         <Input value={dbConfig.host} onChange={(e) => setDbConfig({...dbConfig, host: e.target.value})} className="col-span-3" placeholder="localhost" />
                       </div>
                       <div className="grid grid-cols-4 items-center gap-4">
                         <Label className="text-right">Port</Label>
                         <Input value={dbConfig.port} onChange={(e) => setDbConfig({...dbConfig, port: e.target.value})} className="col-span-3" placeholder="5432" />
                       </div>
                       <div className="grid grid-cols-4 items-center gap-4">
                         <Label className="text-right">Kullanıcı</Label>
                         <Input value={dbConfig.username} onChange={(e) => setDbConfig({...dbConfig, username: e.target.value})} className="col-span-3" />
                       </div>
                       <div className="grid grid-cols-4 items-center gap-4">
                         <Label className="text-right">Şifre</Label>
                         <Input type="password" value={dbConfig.password} onChange={(e) => setDbConfig({...dbConfig, password: e.target.value})} className="col-span-3" />
                       </div>
                       <div className="grid grid-cols-4 items-center gap-4">
                         <Label className="text-right">DB Adı</Label>
                         <Input value={dbConfig.database} onChange={(e) => setDbConfig({...dbConfig, database: e.target.value})} className="col-span-3" />
                       </div>
                     </div>

                     <DialogFooter>
                       <Button onClick={handleDbConnect} disabled={isUploading}>
                         {isUploading ? "Bağlanıyor..." : "Bağlantıyı Kur"}
                       </Button>
                     </DialogFooter>
                   </DialogContent>
                 </Dialog>
               </div>

               <div>Session: {sessionId ? "Aktif" : "..."}</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* SAĞ PANEL */}
      <Card className="w-2/3 flex flex-col shadow-lg">
         <CardHeader className="bg-slate-50 border-b py-3 flex flex-row items-center justify-between">
            <CardTitle className="text-md font-medium flex items-center gap-2"><FileSpreadsheet className="w-4 h-4 text-green-600" /> Sonuç Tablosu</CardTitle>
            {queryResult && <Button variant="outline" size="sm" onClick={handleExport} className="h-8 gap-2"><Download className="w-3 h-3" /> Excel</Button>}
         </CardHeader>
         <CardContent className="flex-1 p-0 overflow-auto bg-white">
            {queryResult ? (
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-slate-500 uppercase bg-slate-50 sticky top-0">
                  <tr>{Object.keys(queryResult[0] || {}).map((key) => <th key={key} className="px-6 py-3 border-b">{key}</th>)}</tr>
                </thead>
                <tbody>
                  {queryResult.map((row, idx) => (
                    <tr key={idx} className="border-b hover:bg-slate-50">
                       {Object.values(row).map((val: any, i) => <td key={i} className="px-6 py-4 truncate max-w-[200px]">{val}</td>)}
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="flex flex-col items-center justify-center h-full text-slate-400 gap-4">
                <FileSpreadsheet className="w-16 h-16 opacity-20" /> <p>Veri bekleniyor...</p>
              </div>
            )}
         </CardContent>
      </Card>
    </div>
  );
}