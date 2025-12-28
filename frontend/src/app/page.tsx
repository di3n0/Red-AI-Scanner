
'use client';
import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen w-full flex flex-col items-center justify-center p-8 relative overflow-hidden text-white">
      {/* Background Image */}
      <div
        className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat opacity-40"
        style={{ backgroundImage: "url('/bg.png')" }}
      ></div>

      {/* Dark Overlay for Readability */}
      <div className="absolute inset-0 z-0 bg-black/60"></div>

      <div className="z-10 w-full max-w-5xl text-center flex flex-col items-center">
        <h1 className="text-8xl font-black mb-6 tracking-tighter text-white drop-shadow-[0_0_15px_rgba(255,255,255,0.8)]">
          RED-AI-SCANNER
        </h1>
        <p className="text-2xl mb-20 text-gray-200 font-mono tracking-[0.5em] uppercase border-b border-gray-500 pb-4 inline-block">
          Autonomous Red Teaming Assistant
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 max-w-4xl mx-auto w-full">

          <Link href="/dashboard" className="group block h-full">
            <div className="glass-panel p-12 h-full flex flex-col items-center justify-center text-center border border-gray-800 hover:border-red-500 transition-all duration-300 hover:shadow-[0_0_50px_rgba(220,38,38,0.3)] bg-gradient-to-b from-gray-900/80 to-black hover:-translate-y-2">
              <div className="text-6xl mb-6 group-hover:scale-110 transition-transform duration-300 filter drop-shadow-[0_0_10px_rgba(255,0,0,0.5)]">🔍</div>
              <h2 className="text-3xl font-bold text-white mb-4 font-mono tracking-widest group-hover:text-red-400 transition-colors text-glow">SCANNER</h2>
              <p className="text-gray-400 text-sm font-mono leading-relaxed">Target Analysis, Vulnerability Scanning, and Exploitation Dashboard.</p>
              <div className="mt-8 px-6 py-2 border border-red-900 rounded text-red-500 text-xs font-mono uppercase tracking-widest group-hover:bg-red-900/20 transition-colors">
                [ ENTER_MODULE ]
              </div>
            </div>
          </Link>

          <Link href="/generator" className="group block h-full">
            <div className="glass-panel p-12 h-full flex flex-col items-center justify-center text-center border border-gray-800 hover:border-purple-500 transition-all duration-300 hover:shadow-[0_0_50px_rgba(147,51,234,0.3)] bg-gradient-to-b from-gray-900/80 to-black hover:-translate-y-2">
              <div className="text-6xl mb-6 group-hover:scale-110 transition-transform duration-300 filter drop-shadow-[0_0_10px_rgba(168,85,247,0.5)]">⚡</div>
              <h2 className="text-3xl font-bold text-white mb-4 font-mono tracking-widest group-hover:text-purple-400 transition-colors text-glow">GENERATOR</h2>
              <p className="text-gray-400 text-sm font-mono leading-relaxed">Gemini-Powered Exploit Script Generation from External Sources.</p>
              <div className="mt-8 px-6 py-2 border border-purple-900 rounded text-purple-500 text-xs font-mono uppercase tracking-widest group-hover:bg-purple-900/20 transition-colors">
                [ ENTER_MODULE ]
              </div>
            </div>
          </Link>

        </div>

        <div className="mt-16 text-xs text-gray-600 font-mono">

        </div>
      </div>
    </main>
  );
}
