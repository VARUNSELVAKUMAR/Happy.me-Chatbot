"use client";

import { useState, useRef, useEffect } from "react";
import { X, Camera } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import axios from "axios";
import Webcam from "react-webcam";

export default function WebcamSection({ triggerCapture }: { triggerCapture: boolean }) {
  const webcamRef = useRef<Webcam>(null);
  const [isWebcamActive, setIsWebcamActive] = useState(true);
  const [capturing, setCapturing] = useState(false);

  useEffect(() => {
    if (triggerCapture && !capturing) {
      captureFrames();
    }
  }, [triggerCapture]);

  const captureFrames = async () => {
    if (!webcamRef.current) return;

    setCapturing(true);
    const frames: Blob[] = [];

    for (let i = 0; i < 10; i++) {
      await new Promise((resolve) => setTimeout(resolve, 100)); // Capture every 250ms
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        const blob = await fetch(imageSrc).then((res) => res.blob());
        frames.push(blob);
      }
    }

    sendFramesToBackend(frames);
    setCapturing(false);
  };

  const sendFramesToBackend = async (frames: Blob[]) => {
    try {
      const formData = new FormData();
      frames.forEach((frame, index) => {
        formData.append("files", frame, `frame_${index}.jpg`);
      });
  
      const response = await axios.post("http://localhost:8000/emotion/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        withCredentials: true, // Allows cookies/session
      });
  
      console.log("Backend Response 123:", response.data);
  
      if (response.data.detected_emotions) {
        console.log("Detected Emotions Per Frame:", response.data.detected_emotions);
      }
  
      localStorage.setItem("emotion", response.data.final_emotion); // Store the final averaged emotion
    } catch (error) {
      console.error("Error sending frames:", error);
    }
  };
  
  const stopWebcam = () => {
    setIsWebcamActive(false);
  };

  const startWebcam = () => {
    setIsWebcamActive(true);
  };

  return (
    <Card className="overflow-hidden shadow-lg transition-all duration-300 hover:shadow-xl">
      <CardHeader className="bg-muted">
        <CardTitle className="flex justify-between items-center">
          <span>Webcam Feed</span>
          {isWebcamActive ? (
            <Button variant="destructive" size="sm" onClick={stopWebcam} aria-label="Stop webcam">
              <X className="h-4 w-4 mr-2" />
              Stop Webcam
            </Button>
          ) : (
            <Button variant="default" size="sm" onClick={startWebcam} aria-label="Start webcam">
              <Camera className="h-4 w-4 mr-2" />
              Start Webcam
            </Button>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        {/* Live Webcam Feed */}
        {isWebcamActive && (
          <div className="relative animate-fade-in">
            <Webcam
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              className="w-full h-[300px] object-cover bg-black rounded-lg"
              mirrored={true}
              videoConstraints={{ facingMode: "user" }}
            />
          </div>
        )}
      </CardContent>
    </Card>
  );
}
