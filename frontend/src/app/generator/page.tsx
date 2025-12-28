
'use client';

import { useState, useEffect } from 'react';

export default function GeneratorPage() {
    const [scriptUrl, setScriptUrl] = useState('');
    const [importStatus, setImportStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
    const [importMsg, setImportMsg] = useState('');
    const [logs, setLogs] = useState<string[]>([]);

    const addLog = (msg: string) => setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);

    const handleImportScript = async () => {
        if (!scriptUrl) return;
        setImportStatus('loading');
        addLog(`Analyzing and importing script from ${scriptUrl}...`);

        try {
            const res = await fetch('http://localhost:8000/script/import', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ script_url: scriptUrl })
            }).then(r => r.json());

            if (res.status === 'success') {
                setImportStatus('success');
                setImportMsg(`Generated and imported: ${res.entry?.name}`);
                addLog(`[AI] Successfully generated exploit: ${res.entry?.name}`);
            } else {
                setImportStatus('error');
                setImportMsg(res.detail || "Unknown error");
                addLog(`[AI] Failed to generate exploit: ${res.detail}`);
            }
        } catch (e) {
            setImportStatus('error');
            setImportMsg(String(e));
            addLog(`Error importing script: ${e}`);
        }
    };

    // API Key State
    const [apiKey, setApiKey] = useState('');
    const [currentKey, setCurrentKey] = useState('Loading...');
    const [showSettings, setShowSettings] = useState(false);

    // Fetch current key on mount
    // Fetch current key on mount
    useEffect(() => {
        fetch('http://localhost:8000/config/ai')
            .then(r => r.json())
            .then(data => setCurrentKey(data.key))
            .catch(() => setCurrentKey('Error fetching key'));
    }, []);

    const updateApiKey = async () => {
        if (!apiKey) return;
        try {
            const res = await fetch('http://localhost:8000/config/ai', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key: apiKey })
            }).then(r => r.json());

            if (res.status === 'success') {
                setCurrentKey(`${apiKey.substring(0, 4)}...${apiKey.substring(apiKey.length - 4)}`);
                setApiKey('');
                addLog('Groq API Key updated successfully.');
                alert('API Key Updated!');
            }
        } catch (e) {
            console.error(e);
            addLog('Failed to update API Key.');
        }
    };

    return (
        <div className="min-h-screen p-8 bg-black flex justify-center items-center">
            <div className="w-full max-w-2xl space-y-8">
                <div className="text-center">
                    <h1 className="text-4xl font-extrabold tracking-tighter mb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
                        Groq Exploit Generator
                    </h1>
                    <p className="text-gray-400">Powered by Groq (Llama-3). Paste a URL to generate a weaponized Python exploit.</p>
                </div>

                <div className="glass-panel p-8 border-t-2 border-purple-500">
                    <div className="space-y-6">

                        {/* API Key Config */}
                        <div className="bg-purple-900/10 p-4 rounded border border-purple-500/30">
                            <div className="flex justify-between items-center mb-4">
                                <h3 className="text-sm text-purple-300 font-bold uppercase tracking-widest">Groq API Key</h3>
                                <span className="text-xs text-gray-500 font-mono">Current: <span className="text-purple-400">{currentKey}</span></span>
                            </div>
                            <div className="flex gap-2">
                                <input
                                    type="password"
                                    value={apiKey}
                                    onChange={(e) => setApiKey(e.target.value)}
                                    placeholder="gsk_xxxxxxxxxxxxxxxx..."
                                    className="flex-1 bg-black/50 border border-purple-900/50 rounded px-3 py-2 text-sm text-white focus:border-purple-500 outline-none transition-colors"
                                />
                                <button
                                    onClick={updateApiKey}
                                    className="bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded text-xs font-bold uppercase transition-colors"
                                >
                                    Set Key
                                </button>
                            </div>
                        </div>

                        <div>
                            <label className="text-xs text-purple-400 font-bold uppercase ml-1 block mb-2">Source URL</label>
                            <input
                                type="text"
                                value={scriptUrl}
                                onChange={(e) => setScriptUrl(e.target.value)}
                                placeholder="https://github.com/exp/poc.py"
                                className="w-full bg-black/50 border border-purple-900/50 rounded px-4 py-3 text-white focus:border-purple-500 outline-none transition-colors"
                            />
                        </div>

                        <button
                            onClick={handleImportScript}
                            disabled={importStatus === 'loading'}
                            className={`w-full btn-primary bg-purple-600 hover:bg-purple-500 py-3 ${importStatus === 'loading' ? 'opacity-50' : ''}`}
                        >
                            {importStatus === 'loading' ? 'Generating with Gemini...' : 'Generate Exploit'}
                        </button>

                        {importStatus === 'success' && (
                            <div className="text-green-400 p-4 rounded bg-green-900/10 border border-green-900/20 text-center animate-pulse">
                                ✓ {importMsg}
                            </div>
                        )}
                        {importStatus === 'error' && (
                            <div className="text-red-400 p-4 rounded bg-red-900/10 border border-red-900/20 text-center">
                                ✗ {importMsg}
                            </div>
                        )}
                    </div>
                </div>

                {logs.length > 0 && (
                    <div className="glass-panel p-4 h-48 overflow-y-auto custom-scrollbar border-gray-800">
                        <div className="scan-terminal bg-transparent border-none p-0 h-auto">
                            {logs.map((l, i) => <div key={i} className="scan-line text-xs font-mono">{l}</div>)}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
