import ChatInterface from "@/components/ChatInterface";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b px-6 py-3 flex items-center gap-3 sticky top-0 z-10">
        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">
          D
        </div>
        <h1 className="text-xl font-bold text-slate-800 tracking-tight">DataChat <span className="text-xs font-normal text-slate-400 bg-slate-100 px-2 py-0.5 rounded-full">Enterprise</span></h1>
      </header>

      {/* Main Content */}
      <div className="flex-1 container mx-auto max-w-7xl">
        <ChatInterface />
      </div>
    </main>
  );
}