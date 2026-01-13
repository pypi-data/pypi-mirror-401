"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X } from "lucide-react";
import Link from "next/link";

const navLinks = [
  { href: "#demo", label: "Demo" },
  { href: "#principles", label: "Principles" },
  { href: "#quickstart", label: "SDK" },
  { href: "#pricing", label: "Pricing" },
  { href: "/blog", label: "Blog", isRoute: true },
];

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Close mobile menu on resize
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setMobileMenuOpen(false);
      }
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  // Prevent scroll when mobile menu is open
  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [mobileMenuOpen]);

  return (
    <>
      <motion.nav
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
        className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrolled
          ? "py-3 bg-background/90 backdrop-blur-xl border-b border-border shadow-subtle"
          : "py-5"
          }`}
      >
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-12">
            <Link
              href="/"
              className="text-lg font-bold tracking-tighter flex items-center gap-2.5 text-foreground group"
            >
              <div className="w-6 h-6 bg-primary rounded-md flex items-center justify-center text-[11px] text-primary-foreground font-mono font-bold transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3">
                E
              </div>
              <span className="transition-colors duration-200 group-hover:text-indigo-400">
                Epist.ai
              </span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-1">
              {navLinks.map((link) =>
                link.isRoute ? (
                  <Link
                    key={link.href}
                    href={link.href}
                    className="relative px-4 py-2 text-[13px] font-medium text-muted-foreground transition-colors duration-200 hover:text-foreground rounded-lg hover:bg-secondary/50"
                  >
                    {link.label}
                  </Link>
                ) : (
                  <a
                    key={link.href}
                    href={link.href}
                    className="relative px-4 py-2 text-[13px] font-medium text-muted-foreground transition-colors duration-200 hover:text-foreground rounded-lg hover:bg-secondary/50"
                  >
                    {link.label}
                  </a>
                )
              )}
            </div>
          </div>

          {/* Desktop CTA */}
          <div className="hidden md:flex items-center gap-3">
            <Link href="/login">
              <button className="btn-ghost">Sign in</button>
            </Link>
            <Link href="/dashboard">
              <button className="btn-primary">
                Get API Keys
              </button>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 -mr-2 text-muted-foreground hover:text-foreground transition-colors"
            aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
            aria-expanded={mobileMenuOpen}
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </motion.nav>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="fixed inset-0 bg-background/80 backdrop-blur-sm z-40 md:hidden"
              onClick={() => setMobileMenuOpen(false)}
            />

            {/* Menu Panel */}
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
              className="fixed top-[60px] left-4 right-4 bg-card border border-border rounded-2xl p-6 z-50 md:hidden shadow-elevated"
            >
              <nav className="flex flex-col gap-2">
                {navLinks.map((link, index) =>
                  link.isRoute ? (
                    <motion.div
                      key={link.href}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.05 }}
                    >
                      <Link
                        href={link.href}
                        onClick={() => setMobileMenuOpen(false)}
                        className="block px-4 py-3 text-[15px] font-medium text-muted-foreground hover:text-foreground hover:bg-secondary/50 rounded-lg transition-colors"
                      >
                        {link.label}
                      </Link>
                    </motion.div>
                  ) : (
                    <motion.a
                      key={link.href}
                      href={link.href}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.05 }}
                      onClick={() => setMobileMenuOpen(false)}
                      className="px-4 py-3 text-[15px] font-medium text-muted-foreground hover:text-foreground hover:bg-secondary/50 rounded-lg transition-colors"
                    >
                      {link.label}
                    </motion.a>
                  )
                )}
              </nav>

              <div className="mt-6 pt-6 border-t border-border flex flex-col gap-3">
                <Link href="/login" className="w-full">
                  <button className="w-full py-3 text-center text-[14px] font-medium text-muted-foreground hover:text-foreground transition-colors">
                    Sign in
                  </button>
                </Link>
                <Link href="/dashboard" className="w-full">
                  <button className="w-full btn-primary justify-center">
                    Get API Keys
                  </button>
                </Link>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
};

export default Navbar;
