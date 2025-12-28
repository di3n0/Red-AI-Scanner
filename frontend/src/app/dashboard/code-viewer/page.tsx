'use client';

import { useSearchParams } from 'next/navigation';
import { useEffect, useState, Suspense } from 'react';

function CodeViewerContent() {
    const searchParams = useSearchParams();
    const id = searchParams.get('id');
    const [code, setCode] = useState<string>('Loading...');
    const [error, setError] = useState<string>('');

    useEffect(() => {
        if (!id) {
            setError('No attack ID provided');
            return;
        }

        fetch(`http://localhost:8000/attack/${id}`)
            .then(res => {
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                return res.json();
            })
            .then(data => {
                if (data.code) {
                    setCode(data.code);
                } else {
                    setError('No code found for this attack ID');
                }
            })
            .catch(err => {
                console.error(err);
                setError(err.message);
            });
    }, [id]);

    return (
        <div className="min-h-screen bg-[#1e1e1e] text-gray-300 p-0 flex flex-col font-mono text-sm">
            <div className="bg-[#252526] p-4 border-b border-black flex justify-between items-center sticky top-0 z-10">
                <h1 className="font-bold text-white tracking-wider flex items-center gap-2">
                    <span className="text-cyan-500">⚡</span>
                    {id || 'Unknown Script'}
                </h1>
                <div className="text-xs text-gray-500">Read-Only Mode</div>
            </div>

            <div className="flex-1 overflow-auto p-6">
                {error ? (
                    <div className="text-red-500 border border-red-900 bg-red-900/20 p-4 rounded">
                        Error: {error}
                    </div>
                ) : (
                    <pre className="whitespace-pre-wrap leading-relaxed selection:bg-cyan-900 selection:text-white">
                        {code}
                    </pre>
                )}
            </div>
        </div>
    );
}

export default function CodeViewerPage() {
    return (
        <Suspense fallback={<div className="min-h-screen bg-[#1e1e1e] text-gray-300 p-8">Loading viewer...</div>}>
            <CodeViewerContent />
        </Suspense>
    );
}
