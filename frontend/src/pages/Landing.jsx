import { useNavigate } from 'react-router-dom';
import { motion } from 'motion/react';
import { useRef, useEffect } from 'react';
import { Shield, RefreshCw, Link2 } from 'lucide-react';

function Landing() {
  const navigate = useNavigate();
  const videoRef = useRef(null);

  // Force video to play when component mounts
  useEffect(() => {
    const video = videoRef.current;
    if (video) {
      video.play().catch(error => {
        console.error('Video autoplay failed:', error);
      });
    }
  }, []);

  return (
    <div className="relative bg-black min-h-screen">
      {/* Fixed Header */}
      <header className="fixed top-0 left-0 right-0 z-[100] pt-6 px-6 md:px-12">
        <div className="flex items-center justify-between backdrop-blur-md bg-black/30 rounded-full px-6 py-3 border border-white/10">
          {/* Logo with gradient V icon */}
          <div className="flex items-center gap-2">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 28L4 4H12L16 12L20 4H28L16 28Z" fill="url(#gradient)" />
              <defs>
                <linearGradient id="gradient" x1="4" y1="4" x2="28" y2="28" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#9c27b0" />
                  <stop offset="0.5" stopColor="#ff4081" />
                  <stop offset="1" stopColor="#ff6b35" />
                </linearGradient>
              </defs>
            </svg>
            <span className="text-2xl font-bold text-white tracking-tight">VYBE</span>
            <span className="text-yellow-300 text-xs ml-0.5 -mt-2">✦</span>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            <button
              onClick={() => navigate('/events')}
              className="text-white/80 hover:text-white transition-colors"
            >
              Events
            </button>
            <button
              onClick={() => navigate('/how-it-works')}
              className="text-white/80 hover:text-white transition-colors"
            >
              How it Works
            </button>
            <button
              onClick={() => navigate('/signin')}
              className="text-white/80 hover:text-white transition-colors"
            >
              Sign In
            </button>
            <button
              onClick={() => navigate('/signup')}
              className="bg-white text-black px-6 py-2 rounded-full font-medium hover:bg-gray-100 transition-colors"
            >
              Get Started
            </button>
          </nav>
        </div>
      </header>

      {/* Fixed full-screen video background - loops independently of scroll */}
      <div className="fixed inset-0 w-full h-full overflow-hidden z-0 bg-gray-900">
        <video
          ref={videoRef}
          className="absolute inset-0 w-full h-full object-cover"
          autoPlay
          loop
          muted
          playsInline
          preload="auto"
          onError={(e) => {
            console.error('Video failed to load:', e);
            console.error('Video source:', e.target.src);
            console.error('Video error code:', e.target.error?.code);
            console.error('Video error message:', e.target.error?.message);
          }}
          onLoadedData={(e) => {
            console.log('Video loaded successfully');
            console.log('Video duration:', e.target.duration);
            console.log('Video dimensions:', e.target.videoWidth, 'x', e.target.videoHeight);
            e.target.play().catch(err => console.error('Play failed:', err));
          }}
          onCanPlay={() => console.log('Video can play')}
          onLoadStart={() => console.log('Video load started')}
        >
          <source src="/videos/vybe_animated.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        
        {/* Dark gradient overlay for text legibility */}
        <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/40 to-black/70" />
      </div>

      {/* Hero Section - overlaps the video at the top */}
      <section className="relative z-[5] min-h-screen flex items-center justify-center px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl text-center relative"
        >
          {/* Sparkle accent - top left */}
          <span className="absolute -left-8 top-0 text-white/40 text-2xl" style={{ transform: 'rotate(-15deg)' }}>✦</span>
          
          {/* Main heading with gradient text */}
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            Find your next<br />
            <span className="gradient-text">experien</span>
            <span className="text-white">ce.</span>
          </h1>
          
          {/* Sparkle accent - right side */}
          <span className="absolute -right-8 top-20 text-white/40 text-xl" style={{ transform: 'rotate(15deg)' }}>✦</span>
          
          <p className="text-lg md:text-xl text-white/80 mb-8 max-w-2xl mx-auto">
            Concerts, sports, festivals, and more — all in one place.
          </p>
          <button
            onClick={() => navigate('/events')}
            className="bg-white text-black px-8 py-4 rounded-full font-semibold text-lg hover:bg-gray-100 transition-all hover:scale-105 inline-flex items-center gap-2"
          >
            Browse Events
            <span>→</span>
          </button>
        </motion.div>
      </section>

      {/* Why Vybe - Features Section */}
      <section className="relative z-[5] bg-[#FFF8F0] py-24 px-6">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8 }}
          className="max-w-6xl mx-auto"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-[#3B2A24] mb-16 text-center">
            Why Vybe
          </h2>
          
          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12">
            {/* Feature 1 - Verified Sellers */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="flex flex-col items-center text-center bg-white rounded-3xl p-8 shadow-lg hover:scale-105 transition-transform duration-300"
            >
              <div className="w-16 h-16 rounded-full bg-[#F5B942]/30 flex items-center justify-center mb-6">
                <Shield className="w-8 h-8 text-[#F5B942]" />
              </div>
              <h3 className="text-xl font-bold text-[#3B2A24] mb-3">
                Verified Sellers Only
              </h3>
              <p className="text-[#3B2A24]/70 leading-relaxed">
                Every seller is AI-verified before listing. No fake tickets, ever.
              </p>
            </motion.div>

            {/* Feature 2 - AI-Investigated Transfers */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex flex-col items-center text-center bg-white rounded-3xl p-8 shadow-lg hover:scale-105 transition-transform duration-300"
            >
              <div className="w-16 h-16 rounded-full bg-[#FF6F91]/30 flex items-center justify-center mb-6">
                <RefreshCw className="w-8 h-8 text-[#FF6F91]" />
              </div>
              <h3 className="text-xl font-bold text-[#3B2A24] mb-3">
                AI-Investigated Transfers
              </h3>
              <p className="text-[#3B2A24]/70 leading-relaxed">
                Every resale is checked by our fraud-detection agents before it's approved.
              </p>
            </motion.div>

            {/* Feature 3 - Blockchain Guaranteed */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="flex flex-col items-center text-center bg-white rounded-3xl p-8 shadow-lg hover:scale-105 transition-transform duration-300"
            >
              <div className="w-16 h-16 rounded-full bg-[#FF8C42]/30 flex items-center justify-center mb-6">
                <Link2 className="w-8 h-8 text-[#FF8C42]" />
              </div>
              <h3 className="text-xl font-bold text-[#3B2A24] mb-3">
                Blockchain Guaranteed
              </h3>
              <p className="text-[#3B2A24]/70 leading-relaxed">
                Every ticket's ownership is recorded on-chain — impossible to duplicate or fake.
              </p>
            </motion.div>
          </div>
        </motion.div>
      </section>

      {/* Section 3 - The Guarantee */}
      <section className="relative z-[5] bg-gradient-to-br from-[#FFF8F0] via-[#FFE8E0] to-[#FFE0E8] py-24 px-6">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto text-center"
        >
          <p className="text-sm md:text-base text-[#FF8C42] font-medium tracking-wider uppercase mb-4">
            The Guarantee
          </p>
          <h2 className="text-5xl md:text-7xl font-bold text-[#3B2A24] mb-6 leading-tight">
            Every ticket, verified on-chain
          </h2>
          <p className="text-lg md:text-xl text-[#3B2A24]/80 mb-8 max-w-2xl mx-auto">
            Blockchain-recorded ownership means your ticket can never be secretly resold twice.
          </p>
          <button
            onClick={() => navigate('/signup')}
            className="bg-gradient-to-r from-[#FF8C42] to-[#FF6F91] text-white px-8 py-4 rounded-full font-semibold text-lg hover:opacity-90 transition-all hover:scale-105"
          >
            Get Started
          </button>
        </motion.div>
      </section>

      {/* CTA Banner Section */}
      <section className="relative z-[5] bg-[#FDF6EC] py-16 px-6">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8 }}
          className="max-w-6xl mx-auto"
        >
          <div className="flex flex-col md:flex-row items-center justify-between gap-8 bg-gradient-to-r from-[#FF8C42] to-[#FF6F91] rounded-3xl p-8 md:p-12 shadow-xl">
            <div className="flex-1 text-center md:text-left">
              <h3 className="text-3xl md:text-4xl font-bold text-white mb-4">
                Have tickets to sell?
              </h3>
              <p className="text-white/90 text-lg">
                List them in minutes. Our AI verifies and lists your ticket instantly for thousands of buyers to see.
              </p>
            </div>
            <button
              onClick={() => navigate('/sell')}
              className="bg-white text-[#FF6F91] px-8 py-4 rounded-full font-semibold text-lg hover:bg-[#FFF8F0] transition-all hover:scale-105 whitespace-nowrap"
            >
              List a Ticket
            </button>
          </div>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="relative z-[5] bg-[#3B1A2B] border-t border-white/10">
        {/* Main Footer Content */}
        <div className="max-w-7xl mx-auto px-6 py-16">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-12">
            {/* Column 1 - Brand */}
            <div className="md:col-span-1">
              <div className="flex items-center gap-2 mb-4">
                <svg width="28" height="28" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M16 28L4 4H12L16 12L20 4H28L16 28Z" fill="url(#footerGradient)" />
                  <defs>
                    <linearGradient id="footerGradient" x1="4" y1="4" x2="28" y2="28" gradientUnits="userSpaceOnUse">
                      <stop stopColor="#9c27b0" />
                      <stop offset="0.5" stopColor="#ff4081" />
                      <stop offset="1" stopColor="#ff6b35" />
                    </linearGradient>
                  </defs>
                </svg>
                <span className="text-xl font-bold text-[#FFF8F0]">VYBE</span>
                <span className="text-[#F5B942] text-xs ml-0.5">✦</span>
              </div>
              <p className="text-[#FFF8F0]/70 text-sm leading-relaxed">
                AI-powered, fraud-protected ticketing for concerts, sports, and festivals.
              </p>
            </div>

            {/* Column 2 - About */}
            <div>
              <h4 className="text-[#F5B942] font-semibold mb-4 uppercase text-sm tracking-wider">
                About
              </h4>
              <ul className="space-y-3">
                <li>
                  <button onClick={() => navigate('/about')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    Who We Are
                  </button>
                </li>
                <li>
                  <button onClick={() => navigate('/how-it-works')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    How It Works
                  </button>
                </li>
                <li>
                  <button onClick={() => navigate('/careers')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    Careers
                  </button>
                </li>
              </ul>
            </div>

            {/* Column 3 - Help */}
            <div>
              <h4 className="text-[#FF6F91] font-semibold mb-4 uppercase text-sm tracking-wider">
                Help
              </h4>
              <ul className="space-y-3">
                <li>
                  <button onClick={() => navigate('/support')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    Support Center
                  </button>
                </li>
                <li>
                  <button onClick={() => navigate('/buying-guide')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    Buying Guide
                  </button>
                </li>
                <li>
                  <button onClick={() => navigate('/selling-guide')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    Selling Guide
                  </button>
                </li>
                <li>
                  <button onClick={() => navigate('/verify')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    Verify a Ticket
                  </button>
                </li>
              </ul>
            </div>

            {/* Column 4 - Legal */}
            <div>
              <h4 className="text-[#FF8C42] font-semibold mb-4 uppercase text-sm tracking-wider">
                Legal
              </h4>
              <ul className="space-y-3">
                <li>
                  <button onClick={() => navigate('/terms')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    Terms of Service
                  </button>
                </li>
                <li>
                  <button onClick={() => navigate('/privacy')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    Privacy Policy
                  </button>
                </li>
                <li>
                  <button onClick={() => navigate('/disputes')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    Dispute Resolution
                  </button>
                </li>
              </ul>
            </div>

            {/* Column 5 - Contact */}
            <div>
              <h4 className="text-[#F5B942] font-semibold mb-4 uppercase text-sm tracking-wider">
                Contact
              </h4>
              <ul className="space-y-3">
                <li>
                  <button onClick={() => navigate('/customer-service')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    Customer Service
                  </button>
                </li>
                <li>
                  <button onClick={() => navigate('/press')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    Press
                  </button>
                </li>
                <li>
                  <button onClick={() => navigate('/partnerships')} className="text-[#FFF8F0]/80 hover:text-[#F5B942] transition-colors text-sm">
                    Partnerships
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-white/10">
          <div className="max-w-7xl mx-auto px-6 py-6 flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-[#FFF8F0]/60 text-sm">
              © 2026 Vybe. All rights reserved.
            </p>
            <div className="flex items-center gap-6">
              {/* Instagram */}
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="text-[#FF8C42] hover:text-[#F5B942] hover:drop-shadow-[0_0_8px_rgba(245,185,66,0.6)] transition-all">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
              </a>
              
              {/* Twitter/X */}
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="text-[#FF8C42] hover:text-[#F5B942] hover:drop-shadow-[0_0_8px_rgba(245,185,66,0.6)] transition-all">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
              </a>
              
              {/* Facebook */}
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="text-[#FF8C42] hover:text-[#F5B942] hover:drop-shadow-[0_0_8px_rgba(245,185,66,0.6)] transition-all">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Landing;
