"use client";

import React, { useEffect, useRef } from 'react';

interface WaveformBackgroundProps {
    intensity?: number;
}

export const WaveformBackground: React.FC<WaveformBackgroundProps> = ({ intensity = 1 }) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationFrameId: number;
        let lines: {
            x: number;
            y: number;
            amplitude: number;
            frequency: number;
            phase: number;
            speed: number;
        }[] = [];

        const gap = 20;
        const speed = 0.002;

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            initLines();
        };

        const initLines = () => {
            lines = [];
            const count = Math.ceil(canvas.width / gap);
            for (let i = 0; i < count; i++) {
                lines.push({
                    x: i * gap,
                    y: canvas.height / 2,
                    amplitude: (Math.random() * 100 + 50) * intensity,
                    frequency: Math.random() * 0.02 + 0.01,
                    phase: Math.random() * Math.PI * 2,
                    speed: Math.random() * 0.02 + 0.01
                });
            }
        };

        const draw = (time: number) => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.lineWidth = 2;

            lines.forEach((line) => {
                const yOffset = Math.sin(time * speed + line.x * 0.005 + line.phase) * (Math.sin(time * 0.001) * line.amplitude);
                const alpha = Math.max(0.1, Math.min(0.5 * intensity, Math.abs(yOffset) / 100));

                const gradient = ctx.createLinearGradient(line.x, 0, line.x, canvas.height);
                gradient.addColorStop(0, `rgba(99, 102, 241, 0)`);
                gradient.addColorStop(0.5, `rgba(99, 102, 241, ${alpha})`);
                gradient.addColorStop(1, `rgba(99, 102, 241, 0)`);

                ctx.strokeStyle = gradient;
                ctx.beginPath();
                ctx.moveTo(line.x, canvas.height / 2 - yOffset);
                ctx.lineTo(line.x, canvas.height / 2 + yOffset);
                ctx.stroke();
            });

            animationFrameId = window.requestAnimationFrame(draw);
        };

        window.addEventListener('resize', resize);
        resize();
        draw(0);

        return () => {
            window.removeEventListener('resize', resize);
            window.cancelAnimationFrame(animationFrameId);
        };
    }, [intensity]);

    return <canvas ref={canvasRef} className="absolute inset-0 w-full h-full pointer-events-none" />;
};
