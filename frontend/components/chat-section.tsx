"use client";

import { useState, useRef, useEffect } from "react";
import { Send, User, Bot, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import Cookies from "js-cookie";
import axios from "axios";
interface ChatEntry {
  user_input: string;
  bot_response: string;
  emotion: string;
  timestamp: string;
}

export default function ChatSection({
  setTriggerCapture,
}: {
  setTriggerCapture: (value: boolean) => void;
}) {
  const [messages, setMessages] = useState<ChatEntry[]>([]);
  const [inputValue, setInputValue] = useState("");
  const lastMessageRef = useRef<HTMLDivElement>(null);
  const [typingAllowed, setTypingAllowed] = useState(false);
  const [capturing, setCapturing] = useState(false);

  useEffect(() => {
    const storedChat = Cookies.get("chat_history");
    if (storedChat) {
      setMessages(JSON.parse(storedChat));
    }
  }, []);

  useEffect(() => {
    lastMessageRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages]);

  const updateChatHistory = (newMessages: ChatEntry[]) => {
    setMessages(newMessages);
    Cookies.set("chat_history", JSON.stringify(newMessages), { expires: 7 });
  };

  // Fetch latest emotion from backend
  const getLatestEmotionFromBackend = async (): Promise<string> => {
    try {
      const response = await axios.get("http://localhost:8000/emotion/");
      console.log("Emotion from backend:", response.data.final_emotion);
      return response.data.final_emotion || "neutral"; // Default fallback
    } catch (error) {
      console.error("Error fetching emotion from backend:", error);
      return "neutral"; // Default to neutral if error occurs
    }
  };

  const handleTyping = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);

    if (!capturing) {
      setCapturing(true);
      setTriggerCapture(true); // Trigger frame capture

      setTimeout(() => {
        setCapturing(false);
      }, 2000);
    }

    if (typingAllowed) {
      setTypingAllowed(false);
    }
  };

  const captureFrameFromWebcam = async (): Promise<Blob> => {
    return new Promise((resolve, reject) => {
      const video = document.querySelector("video"); // Get the video element
  
      if (!video) {
        reject(new Error("Webcam not found"));
        return;
      }
  
      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
  
      if (!ctx) {
        reject(new Error("Canvas context not supported"));
        return;
      }
  
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  
      // Convert to Blob (JPEG format)
      canvas.toBlob((blob) => {
        if (blob) {
          resolve(blob);
        } else {
          reject(new Error("Failed to capture frame"));
        }
      }, "image/jpeg");
    });
  };
  
  const captureFrames = async (numFrames: number) => {
    const frames: Blob[] = [];
    for (let i = 0; i < numFrames; i++) {
      try {
        const frame = await captureFrameFromWebcam();
        frames.push(frame);
        await new Promise((resolve) => setTimeout(resolve, 100)); // Small delay to capture different frames
      } catch (error) {
        console.error("Error capturing frame:", error);
      }
    }
    return frames;
  };
  
  const sendFramesToBackend = async (frames: Blob[]): Promise<string> => {
    try {
      const formData = new FormData();
      frames.forEach((frame, index) => {
        formData.append("files", frame, `frame_${index}.jpg`);
      });
  
      const response = await axios.post("http://localhost:8000/emotion/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        withCredentials: true,
      });
  
      console.log("Backend Response:", response.data);
  
      return response.data.final_emotion || "neutral"; // Return detected emotion
    } catch (error) {
      console.error("Error sending frames:", error);
      return "neutral"; // Default to neutral if error occurs
    }
  };
  


  const handleSendMessage = async () => {
    if (inputValue.trim() === "") return;
  
    setTypingAllowed(false);
  
    // Trigger webcam frame capture for 10 frames
    setTriggerCapture(true);
    await new Promise((resolve) => setTimeout(resolve, 2000)); // Wait for frames to be captured
  
    try {
      const frames = await captureFrames(10); // Function to capture 10 frames
      if (frames.length === 0) throw new Error("No frames captured");
  
      // Send frames to the backend for emotion analysis
      const latestEmotion = await sendFramesToBackend(frames);
      console.log("Emotion from frames:", latestEmotion);
  
      const timestamp = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
  
      const userMessage: ChatEntry = {
        user_input: inputValue,
        bot_response: "",
        emotion: latestEmotion,
        timestamp,
      };
  
      const updatedMessages = [...messages, userMessage];
      updateChatHistory(updatedMessages);
      setInputValue("");
  
      const token = localStorage.getItem("jwt");
  
      // Send chat message along with detected emotion
      const response = await fetch("http://localhost:8000/chat/", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: inputValue,
          emotion: latestEmotion,
        }),
      });
  
      if (!response.ok) {
        throw new Error("Failed to send message");
      }
  
      const data = await response.json();
      console.log("Chatbot Response:", data);
  
      const botMessage: ChatEntry = {
        user_input: inputValue,
        bot_response: data.message,
        emotion: latestEmotion,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };
  
      updateChatHistory([...updatedMessages, botMessage]);
      setTypingAllowed(true);
    } catch (error) {
      console.error("Error sending message:", error);
      setTypingAllowed(true);
    }
  };
  


  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSendMessage();
  };

  const clearChatHistory = () => {
    setMessages([]);
    Cookies.remove("chat_history");

    document.cookie.split(";").forEach((c) => {
      document.cookie = c
        .replace(/^ +/, "")
        .replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
    });
  };

  return (
    <Card className="h-[calc(100vh-150px)] flex flex-col shadow-lg transition-all duration-300 hover:shadow-xl relative">
      <CardHeader className="bg-muted">
        <CardTitle>Chat Assistant</CardTitle>
      </CardHeader>
      <ScrollArea className="flex-grow p-4">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex items-start space-x-2 animate-slide-in ${
                message.bot_response === "" ? "flex-row-reverse space-x-reverse" : ""
              }`}
              ref={index === messages.length - 1 ? lastMessageRef : null}
            >
              <div
                className={`flex-shrink-0 rounded-full p-2 ${
                  message.bot_response === "" ? "bg-primary" : "bg-secondary"
                }`}
              >
                {message.bot_response === "" ? (
                  <User className="h-4 w-4 text-primary-foreground" />
                ) : (
                  <Bot className="h-4 w-4 text-secondary-foreground" />
                )}
              </div>
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.bot_response === "" ? "bg-primary text-primary-foreground" : "bg-secondary text-secondary-foreground"
                }`}
              >
                <p>{message.bot_response === "" ? message.user_input : message.bot_response}</p>
                <p className="text-xs opacity-70 mt-1">{message.timestamp}</p>
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>

      <CardFooter className="border-t p-4 flex justify-between">
        <form onSubmit={handleSubmit} className="w-full flex gap-2">
          <Input value={inputValue} onChange={handleTyping} placeholder="Type your message..." className="flex-grow" />
          <Button type="submit" size="icon" className="shrink-0">
            <Send className="h-4 w-4" />
          </Button>
        </form>

        <Button
          variant="destructive"
          size="sm"
          onClick={clearChatHistory}
          className="ml-4 px-3 py-1"
        >
          <Trash2 className="h-4 w-4 mr-1" /> Clear Chat
        </Button>
      </CardFooter>
    </Card>
  );
}
