"use client"

import { useState, useEffect } from "react"
import ThemeToggle from "@/components/theme-toggle"
import WebcamSection from "@/components/webcam-section"
import ChatSection from "@/components/chat-section"


export default function Home() {
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [triggerCapture, setTriggerCapture] = useState(false)

  useEffect(() => {
    const savedTheme = localStorage.getItem("theme")
    if (savedTheme === "dark") {
      setIsDarkMode(true)
      document.documentElement.classList.add("dark")
    }
  }, [])

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode)
    if (!isDarkMode) {
      document.documentElement.classList.add("dark")
      localStorage.setItem("theme", "dark")
    } else {
      document.documentElement.classList.remove("dark")
      localStorage.setItem("theme", "light")
    }
  }

  return (
    <div className={`min-h-screen transition-colors duration-300 ${isDarkMode ? "dark" : ""}`}>
      <div className="container mx-auto p-4 md:p-6 lg:p-8">
        <header className="flex justify-between items-center mb-8">
          <ThemeToggle isDarkMode={isDarkMode} toggleTheme={toggleTheme} />
        </header>

        <main className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          <div className="lg:col-span-2 space-y-8">
            <WebcamSection triggerCapture={triggerCapture} />
          </div>
          <div className="lg:col-span-3">
            <ChatSection setTriggerCapture={setTriggerCapture} />
          </div>
        </main>
      </div>
    </div>
  )
}