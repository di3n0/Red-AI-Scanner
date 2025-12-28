'use client';

import { useSearchParams } from 'next/navigation';
import { useEffect, useState, Suspense } from 'react';

// Types
interface ScanResult {
    status: string;
    findings?: any[];
    file?: string;
    output?: string; // Nmap output
    error?: string;
    command?: string;
}

interface AnalysisResult {
    severity: string;
    description: string;
    patch_advice: string;
    impact?: string;
}

interface AttackScript {
    id: string;
    name: string;
    category: string;
    description: string;
}

function DashboardContent() {
    const searchParams = useSearchParams();
    const targetType = searchParams.get('type') || 'custom';
    // Initialize state with URL param or empty
    const [localTargetUrl, setLocalTargetUrl] = useState(searchParams.get('url') || '');

    interface LogEntry {
        timestamp: string;
        message: string;
    }

    const [logs, setLogs] = useState<LogEntry[]>([
        { timestamp: "SYSTEM", message: "System Initialized." },
        { timestamp: "SYSTEM", message: "----------------------------------------" },
        { timestamp: "SYSTEM", message: "🎯 K8s Goat Targets Reference:" },
        { timestamp: "SYSTEM", message: "http://127.0.0.1:1230 : Sensitive Keys" },
        { timestamp: "SYSTEM", message: "http://127.0.0.1:1231 : DIND Exploit" },
        { timestamp: "SYSTEM", message: "http://127.0.0.1:1232 : SSRF" },
        { timestamp: "SYSTEM", message: "http://127.0.0.1:1233 : Container Escape" },
        { timestamp: "SYSTEM", message: "http://127.0.0.1:1234 : Goat Home (Manual)" },
        { timestamp: "SYSTEM", message: "http://127.0.0.1:1235 : Private Registry" },
        { timestamp: "SYSTEM", message: "http://127.0.0.1:1236 : DoS Resources" },
        { timestamp: "SYSTEM", message: "----------------------------------------" },
        { timestamp: "SYSTEM", message: "Ready for scanning..." }
    ]);
    const [nmapResult, setNmapResult] = useState<ScanResult | null>(null);
    const [nucleiResult, setNucleiResult] = useState<ScanResult | null>(null);
    const [loading, setLoading] = useState(false);

    // Progress Logic
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        let interval: NodeJS.Timeout;
        if (loading) {
            setProgress(5);
            interval = setInterval(() => {
                setProgress(prev => {
                    // Slow down significantly as we get closer to 90% to assume a 15-30s scan
                    if (prev >= 90) return prev;
                    // Lower increment to 1-2%
                    return prev + (Math.random() > 0.5 ? 1 : 0);
                });
            }, 500); // 500ms update rate = slower fill
        } else {
            setProgress(100);
        }
        return () => clearInterval(interval);
    }, [loading]);

    // Attack Script State
    const [attacks, setAttacks] = useState<{ [key: string]: AttackScript[] }>({});
    const [selectedAttacks, setSelectedAttacks] = useState<Set<string>>(new Set());
    const [attackResults, setAttackResults] = useState<{ [key: string]: { status: 'success' | 'failed' | 'running' | null, output?: string, analysis?: AnalysisResult } }>({});
    const [showPatchReport, setShowPatchReport] = useState(false);

    // Workflow State
    const [activeStep, setActiveStep] = useState<'scan' | 'exploit'>('scan');

    const addLog = (msg: string) => setLogs(prev => [...prev, { timestamp: new Date().toLocaleTimeString('en-US', { hour12: false }), message: msg }]);

    // Update local state if URL param changes (optional but good practice)
    useEffect(() => {
        const urlParam = searchParams.get('url');
        if (urlParam) setLocalTargetUrl(urlParam);
    }, [searchParams]);

    // Load attacks on mount
    useEffect(() => {
        fetch('http://localhost:8000/attacks').then(r => r.json()).then(data => {
            setAttacks(data);
        }).catch(console.error);
    }, []);

    const startScan = async () => {
        if (!localTargetUrl) {
            addLog("Error: Please enter a target URL.");
            return;
        }
        setLoading(true);
        addLog(`Starting comprehensive scan on ${localTargetUrl}...`);

        try {
            // 1. Nmap
            addLog("Running Nmap scan...");
            const nmapRes = await fetch('http://localhost:8000/scan/nmap', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target_url: localTargetUrl, scan_type: targetType })
            }).then(r => r.json());
            setNmapResult(nmapRes);
            if (nmapRes.output) {
                addLog(`\n--- [Nmap Scan Result] ---\n${nmapRes.output}\n--------------------------`);
            } else if (nmapRes.error) {
                addLog(`[Nmap Error] ${nmapRes.error}`);
            }

            // 2. Nuclei
            addLog("Running Nuclei scan...");
            const nucleiRes = await fetch('http://localhost:8000/scan/nuclei', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target_url: localTargetUrl, scan_type: targetType })
            }).then(r => r.json());
            setNucleiResult(nucleiRes);
            if (nucleiRes.findings && nucleiRes.findings.length > 0) {
                const findingLog = nucleiRes.findings.map((f: any) => `[${f.info?.severity?.toUpperCase()}] ${f.info?.name} (${f.matcher_name})`).join('\n');
                addLog(`\n--- [Nuclei Findings] ---\n${findingLog}\n-------------------------`);
            } else {
                addLog("[Nuclei] No high-risk vulnerabilities detected.");
            }

            // 3. ZAP Scan Removed
            addLog("All Scans Complete. Check console for details.");

        } catch (e) {
            addLog(`Error during scan: ${e}`);
        } finally {
            setLoading(false);
        }
    };

    const toggleAttack = (id: string) => {
        const next = new Set(selectedAttacks);
        if (next.has(id)) next.delete(id);
        else next.add(id);
        setSelectedAttacks(next);
    };

    const selectAll = () => {
        const all = new Set<string>();
        Object.values(attacks).forEach(list => list.forEach(a => all.add(a.id)));
        setSelectedAttacks(all);
    };

    const clearAll = () => {
        setSelectedAttacks(new Set());
    };

    const runSelectedAttacks = async () => {
        if (selectedAttacks.size === 0) return;
        addLog(`Starting ${selectedAttacks.size} attack verification scripts...`);
        setShowPatchReport(false);

        for (const id of Array.from(selectedAttacks)) {
            setAttackResults(prev => ({ ...prev, [id]: { status: 'running' } }));
            addLog(`Running Attack: ${id}...`);
            try {
                // 1. Run Attack
                const res = await fetch('http://localhost:8000/attack/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ attack_id: id, target_url: localTargetUrl })
                }).then(r => r.json());

                const status = (res.success || (res.output && res.output.includes("SUCCESS")) || (res.output && res.output.includes("CONFIRMED"))) ? 'success' : 'failed';

                let analysis: AnalysisResult | undefined;
                // 2. Analyze Result (if success) to get structured Remediation
                if (status === 'success') {
                    try {
                        analysis = await fetch('http://localhost:8000/analyze', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ vulnerability_data: { output: res.output, name: id } })
                        }).then(r => r.json());

                        if (analysis) {
                            const logMsg = `
----------------------------------------
🛡️ Remediation & Patch Advice
----------------------------------------
Fix for: ${id}

${analysis.patch_advice ? `Patch Advice:\n${analysis.patch_advice}` : ''}
${analysis.impact ? `\nExploitation Steps & Impact:\n${analysis.impact}` : ''}
----------------------------------------`;
                            addLog(logMsg);
                        }

                    } catch (err) {
                        console.error("Analysis failed", err);
                    }
                }

                setAttackResults(prev => ({ ...prev, [id]: { status, output: res.output, analysis } }));
                addLog(`Attack ${id}: ${status.toUpperCase()}`);
            } catch (e) {
                setAttackResults(prev => ({ ...prev, [id]: { status: 'failed' } }));
                addLog(`Attack ${id} Error: ${e}`);
            }
        }
        addLog("Batch Attack Execution Finished.");
        setShowPatchReport(true);
    };

    // Script Import State
    const [scriptUrl, setScriptUrl] = useState('');
    const [importStatus, setImportStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
    const [importMsg, setImportMsg] = useState('');

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
                addLog(`[GEMINI] Successfully generated exploit: ${res.entry?.name}`);
                // Refresh attacks
                fetch('http://localhost:8000/attacks').then(r => r.json()).then(setAttacks);
            } else {
                setImportStatus('error');
                setImportMsg(res.detail || "Unknown error");
                addLog(`[GEMINI] Failed to generate exploit: ${res.detail}`);
            }
        } catch (e) {
            setImportStatus('error');
            setImportMsg(String(e));
            addLog(`Error importing script: ${e}`);
        }
    };

    // Code View State - REMOVED

    const handleStopScan = async () => {
        try {
            await fetch('http://localhost:8000/scan/stop', { method: 'POST' });
            addLog("Scan stopped by user.");
            // Trigger UI to show Next button by setting a result state
            setNmapResult({ output: "Scan stopped manually", file: "stopped", status: "stopped" });
            setLoading(false);
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="min-h-screen p-8 relative z-10 selection:bg-red-900 selection:text-white">
            <header className="mb-8 border-b border-gray-800 pb-8">
                <div className="flex justify-between items-center mb-6">
                    <div>
                        <h1 className="text-5xl font-mono tracking-tighter mb-2 text-glow uppercase text-transparent bg-clip-text bg-gradient-to-r from-red-600 to-red-400"
                            style={{ textShadow: '0 0 20px rgba(255, 0, 0, 0.5)' }}>
                            Red-AI-Scanner
                        </h1>
                        <div className="flex items-center gap-2 text-cyan-400 text-xs font-mono">
                            <span className="inline-block w-2 h-2 bg-green-500 rounded-full animate-blink"></span>
                            SYSTEM_ONLINE :: V.1.0.33
                        </div>
                    </div>
                </div>

                <div className="glass-panel p-3 flex gap-4 items-center">
                    <div className="flex-1">
                        <label className="text-xs text-cyan-400 font-mono font-bold uppercase ml-1 block mb-1 tracking-widest">Target Acquisition</label>
                        <div className="flex gap-4">
                            <input
                                type="text"
                                placeholder="ENTER TARGET URL..."
                                className="bg-black/80 border border-gray-700 hover:border-red-500 focus:border-red-500 rounded-sm px-4 py-2 w-full text-white outline-none transition-all font-mono tracking-wider shadow-inner"
                                value={localTargetUrl}
                                onChange={(e) => setLocalTargetUrl(e.target.value)}
                                disabled={loading}
                            />
                            {loading ? (
                                <button onClick={handleStopScan} className="btn-primary" style={{ background: '#330000', borderColor: '#ff0000' }}>
                                    🛑 ABORT OPERATION
                                </button>
                            ) : (
                                <button onClick={startScan} disabled={loading} className="btn-primary hover:bg-red-700">
                                    INITIALIZE SCAN
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">

                {/* Left: Logs (Persistent) */}
                <div className="space-y-6 lg:col-span-1">
                    <div className="glass-panel p-3 h-[400px] flex flex-col border-secondary">
                        <h3 className="text-xs mb-3 text-cyan-400 font-mono font-bold flex items-center gap-2 border-b border-gray-800 pb-2">
                             // LIVE_CONSOLE_OUTPUT
                        </h3>
                        <div className="scan-terminal flex-1 custom-scrollbar">
                            {logs.map((l, i) => (
                                <div key={i} className="scan-line font-mono text-xs whitespace-pre-wrap mb-1 border-b border-transparent hover:border-gray-800 hover:bg-gray-900/50 transition-colors">
                                    <span className="text-gray-600 mr-2">[{l.timestamp}]</span>
                                    {l.message}
                                </div>
                            ))}
                            <span className="inline-block w-2.5 h-4 bg-green-500 animate-blink align-middle ml-1"></span>
                        </div>
                    </div>
                </div>

                {/* Right: Detailed Scan & Attacks */}
                <div className="lg:col-span-4 space-y-6">

                    {/* VIEW 1: SCAN RESULTS STATUS */}
                    {activeStep === 'scan' && (
                        <div className="glass-panel p-0 overflow-hidden flex flex-col animate-fade-in h-full min-h-[350px]">
                            <div className="p-6 flex flex-col items-center justify-center space-y-4 text-center flex-1">
                                {loading ? (
                                    <div className="space-y-4 w-full max-w-lg mx-auto relative flex flex-col justify-center h-full">
                                        {/* Massive Percentage Display */}
                                        <div className="relative flex justify-center items-center py-4">
                                            <span className="text-9xl scale-150 font-black text-red-600 drop-shadow-[0_0_30px_rgba(220,38,38,0.8)] font-mono tracking-tighter animate-pulse">
                                                {progress}%
                                            </span>
                                            {/* Decorative Elements */}
                                            <div className="absolute -inset-4 border border-red-900/30 rounded-full animate-spin-slow opacity-50"></div>
                                            <div className="absolute -inset-8 border border-dashed border-red-900/20 rounded-full animate-reverse-spin opacity-30"></div>
                                        </div>

                                        {/* Progress Bar */}
                                        <div className="space-y-2">
                                            <div className="flex justify-between text-sm text-red-400 font-mono tracking-widest uppercase">
                                                <span className="animate-blink">Scanner Activity</span>
                                                <span>{progress >= 90 ? "FINALIZING" : "IN PROGRESS"}</span>
                                            </div>
                                            <div className="w-full bg-black/50 rounded-full h-2 overflow-hidden border border-gray-800">
                                                <div
                                                    className="bg-red-600 h-full shadow-[0_0_15px_rgba(220,38,38,0.8)]"
                                                    style={{ width: `${progress}%`, transition: 'width 0.2s linear' }}
                                                ></div>
                                            </div>
                                        </div>

                                        <p className="text-xs text-gray-500 font-mono text-center">
                                            TARGET: {localTargetUrl || 'UNKNOWN'} | MODE: FAST_SCAN | THREADS: T5
                                        </p>
                                    </div>
                                ) : nmapResult ? (
                                    <div className="space-y-4 animate-fade-in-up">
                                        <div className="text-5xl">{nmapResult.file === 'stopped' ? '🛑' : '✅'}</div>
                                        <h3 className="text-xl font-bold text-white">
                                            {nmapResult.file === 'stopped' ? 'Scan Stopped' : 'Scan Completed'}
                                        </h3>
                                        <p className="text-gray-400 max-w-md">
                                            {nmapResult.file === 'stopped'
                                                ? "You halted the scan manually. You can still proceed to run exploits."
                                                : "Detailed Nmap and Nuclei results have been output to the Live Console on the left."
                                            }
                                        </p>
                                        <div className="pt-4">
                                            <button
                                                onClick={() => setActiveStep('exploit')}
                                                className="btn-primary bg-red-600 hover:bg-red-500 text-base py-3 px-8 flex items-center gap-2 mx-auto"
                                            >
                                                {nmapResult.file === 'stopped' ? 'Skip to Exploits ➔' : 'Next: Select Exploits ➔'}
                                            </button>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="text-gray-500 italic">
                                        Enter a target URL above and click "Start Full Scan" to begin.
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* VIEW 2: VERIFICATION & EXPLOIT */}
                    {activeStep === 'exploit' && (
                        <div className="space-y-6 animate-fade-in-up">
                            <div className="glass-panel p-6">
                                <div className="flex justify-between items-center mb-6 border-b border-gray-800 pb-4">
                                    <div>
                                        <div className="flex items-center gap-2">
                                            <button onClick={() => setActiveStep('scan')} className="text-gray-500 hover:text-white transition-colors font-mono text-xs tracking-widest">
                                                [ &lt;&lt; RETURN ]
                                            </button>
                                            <h2 className="text-2xl font-mono text-white text-glow tracking-tighter">ATTACK_REGISTRY</h2>
                                        </div>
                                        <p className="text-xs text-cyan-500 mt-1 font-mono tracking-widest pl-4 border-l-2 border-cyan-500 ml-1">SELECT VECTORS FOR DEPLOYMENT</p>
                                    </div>
                                    <div className="flex gap-2">
                                        <button onClick={selectAll} className="btn-secondary text-xs py-2 px-3 border-secondary text-cyan-400 hover:bg-cyan-900/20 font-mono tracking-wider">ALL</button>
                                        <button onClick={clearAll} className="btn-secondary text-xs py-2 px-3 border-gray-600 text-gray-400 hover:bg-gray-800 font-mono tracking-wider">NONE</button>
                                        <button onClick={runSelectedAttacks} className="btn-primary text-sm py-2 px-6 font-bold tracking-widest border border-red-500 shadow-lg shadow-red-900/50">
                                            EXECUTE ({selectedAttacks.size})
                                        </button>
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 h-[300px] overflow-y-auto pr-2 custom-scrollbar">
                                    {Object.keys(attacks).length > 0 ? Object.keys(attacks).map(category => (
                                        <div key={category} className="mb-4">
                                            <h3 className="text-lg font-bold capitalize text-gray-300 mb-2 border-b border-gray-700 pb-1 sticky top-0 bg-black/90 z-10">{category.replace('_', ' ')}</h3>
                                            <div className="space-y-2">
                                                {attacks[category].map(attack => (
                                                    <div key={attack.id} className={`p-3 rounded border transition-all duration-200 ${selectedAttacks.has(attack.id) ? 'border-cyan-500 bg-cyan-900/20' : 'border-gray-800 bg-black/40 hover:border-gray-600'} flex justify-between items-center cursor-pointer group`}
                                                        onClick={() => toggleAttack(attack.id)}>

                                                        {/* Left: Checkbox + Name */}
                                                        <div className="flex items-center gap-3 overflow-hidden flex-1">
                                                            <input
                                                                type="checkbox"
                                                                checked={selectedAttacks.has(attack.id)}
                                                                readOnly
                                                                className="w-5 h-5 accent-cyan-500 cursor-pointer shrink-0"
                                                            />
                                                            <span className="font-bold text-sm text-white truncate">{attack.name}</span>
                                                        </div>

                                                        {/* Right: Status + Code Button */}
                                                        <div className="flex items-center gap-3 shrink-0 ml-2">
                                                            {attackResults[attack.id]?.status === 'running' && <span className="text-yellow-400 animate-pulse text-xs">Running...</span>}
                                                            {attackResults[attack.id]?.status === 'success' && <span className="text-green-500 font-bold text-sm">✓ PASS</span>}
                                                            {attackResults[attack.id]?.status === 'failed' && <span className="text-red-500 font-bold text-sm">✗ FAIL</span>}

                                                            <button
                                                                onClick={(e) => {
                                                                    e.stopPropagation();
                                                                    window.open(`/dashboard/code-viewer?id=${attack.id}`, '_blank');
                                                                }}
                                                                className="text-[10px] uppercase bg-gray-800 text-gray-400 px-3 py-1 rounded border border-gray-700 hover:bg-gray-700 hover:text-white transition-colors"
                                                            >
                                                                Code
                                                            </button>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )) : <div className="p-4 text-gray-500">Loading attack registry...</div>}
                                </div>
                            </div>
                        </div>
                    )}
                    <span className="inline-block w-2.5 h-4 bg-green-500 animate-blink align-middle ml-1"></span>
                </div>
            </div>
        </div>


    );
}

export default function Dashboard() {
    return (
        <Suspense fallback={<div className="text-center p-20">Loading Dashboard...</div>}>
            <DashboardContent />
        </Suspense>
    )
}
