import { useRef, useEffect, useState } from "react";
import { Play, Pause } from "lucide-react";

interface WordTimestamp {
    word: string;
    start: number;
    end: number;
}

interface SegmentWithWords {
    id: string;
    start: number;
    end: number;
    text: string;
    words?: WordTimestamp[];
}

interface KaraokePlayerProps {
    audioUrl: string;
    segments: SegmentWithWords[];
    currentTime: number;
    onTimeUpdate: (time: number) => void;
    onSeek: (time: number) => void;
}

export function KaraokePlayer({
    audioUrl,
    segments,
    currentTime,
    onTimeUpdate,
    onSeek,
}: KaraokePlayerProps) {
    const audioRef = useRef<HTMLAudioElement>(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);

    const [duration, setDuration] = useState(0);

    useEffect(() => {
        const audio = audioRef.current;
        if (!audio) return;

        const handleTimeUpdate = () => {
            onTimeUpdate(audio.currentTime);
        };

        const handleLoadedMetadata = () => {
            setDuration(audio.duration);
        };

        const handlePlay = () => setIsPlaying(true);
        const handlePause = () => setIsPlaying(false);

        audio.addEventListener("timeupdate", handleTimeUpdate);
        audio.addEventListener("loadedmetadata", handleLoadedMetadata);
        audio.addEventListener("play", handlePlay);
        audio.addEventListener("pause", handlePause);

        return () => {
            audio.removeEventListener("timeupdate", handleTimeUpdate);
            audio.removeEventListener("loadedmetadata", handleLoadedMetadata);
            audio.removeEventListener("play", handlePlay);
            audio.removeEventListener("pause", handlePause);
        };
    }, [onTimeUpdate]);

    const togglePlay = () => {
        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
        }
    };

    const handleWordClick = (time: number) => {
        onSeek(time);
        if (audioRef.current) {
            audioRef.current.currentTime = time;
            audioRef.current.play();
        }
    };

    // Auto-scroll to current word
    useEffect(() => {
        if (containerRef.current) {
            const activeWord = containerRef.current.querySelector("[data-active='true']");
            if (activeWord) {
                activeWord.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center",
                });
            }
        }
    }, [currentTime]);

    const isWordActive = (word: WordTimestamp) => {
        return currentTime >= word.start && currentTime <= word.end;
    };

    const isSegmentActive = (segment: SegmentWithWords) => {
        return currentTime >= segment.start && currentTime <= segment.end;
    };

    return (
        <div className="flex flex-col gap-4">
            {/* Audio Controls */}
            <div className="flex items-center gap-4 p-4 bg-slate-950 border border-slate-800 rounded-lg">
                <button
                    onClick={togglePlay}
                    className="p-3 rounded-full bg-indigo-500 hover:bg-indigo-600 text-white transition-colors"
                >
                    {isPlaying ? <Pause size={20} /> : <Play size={20} />}
                </button>
                <audio ref={audioRef} src={audioUrl} className="hidden" />
                <div className="flex-1">
                    <div className="text-sm text-slate-400 mb-1">
                        {formatTime(currentTime)} / {formatTime(duration)}
                    </div>
                    <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-indigo-500 transition-all duration-100"
                            style={{
                                width: `${((currentTime / (duration || 1)) * 100)}%`,
                            }}
                        />
                    </div>
                </div>
            </div>

            {/* Karaoke Display */}
            <div
                ref={containerRef}
                className="p-6 bg-slate-900 border border-slate-800 rounded-lg overflow-auto max-h-[400px]"
            >
                <div className="space-y-4">
                    {segments.map((segment) => (
                        <div
                            key={segment.id}
                            className={`transition-opacity duration-200 ${isSegmentActive(segment) ? "opacity-100" : "opacity-40"
                                }`}
                        >
                            {segment.words && segment.words.length > 0 ? (
                                <div className="flex flex-wrap gap-2 leading-relaxed text-lg">
                                    {segment.words.map((word, idx) => (
                                        <span
                                            key={`${segment.id}-${idx}`}
                                            data-active={isWordActive(word)}
                                            onClick={() => handleWordClick(word.start)}
                                            className={`cursor-pointer transition-all duration-150 ${isWordActive(word)
                                                ? "text-indigo-400 font-semibold scale-110 drop-shadow-[0_0_8px_rgba(129,140,248,0.5)]"
                                                : "text-slate-300 hover:text-slate-100"
                                                }`}
                                        >
                                            {word.word}
                                        </span>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-slate-300 text-lg">{segment.text}</p>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

function formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, "0")}`;
}
