
'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navigation() {
    const pathname = usePathname();

    return (
        <nav className="fixed top-0 left-0 right-0 h-16 bg-black/50 backdrop-blur-md border-b border-gray-800 z-50 flex items-center justify-between px-8">
            <Link href="/" className="font-bold text-xl tracking-tighter">
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-red-600 via-rose-500 to-purple-600">
                    Red-AI-Scanner
                </span>
            </Link>

            <div className="flex gap-1">
                <Link href="/dashboard" className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${pathname === '/dashboard' ? 'bg-white/10 text-white' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}>
                    Scanner
                </Link>
                <Link href="/generator" className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${pathname === '/generator' ? 'bg-white/10 text-white' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}>
                    Exploit Generator
                </Link>
            </div>
        </nav>
    );
}
