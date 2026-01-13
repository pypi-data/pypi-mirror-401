"use client";

import Navbar from "@/components/landing/Navbar";
import Hero from "@/components/landing/Hero";
import PainPoints from "@/components/landing/PainPoints";
import Demo from "@/components/landing/Demo";
import Principles from "@/components/landing/Principles";
import Quickstart from "@/components/landing/Quickstart";
import UseCases from "@/components/landing/UseCases";
import Pricing from "@/components/landing/Pricing";
import CTA from "@/components/landing/CTA";
import Footer from "@/components/landing/Footer";

export default function Home() {
  return (
    <div className="min-h-screen bg-background bg-grid relative overflow-x-hidden selection:bg-primary/30 selection:text-foreground">
      <Navbar />
      <Hero />
      <PainPoints />
      <div id="demo">
        <Demo />
      </div>
      <div id="principles">
        <Principles />
      </div>
      <div id="quickstart">
        <Quickstart />
      </div>
      <UseCases />
      <div id="pricing">
        <Pricing />
      </div>
      <CTA />
      <Footer />
    </div>
  );
}
