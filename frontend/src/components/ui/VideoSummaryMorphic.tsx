'use client'

import { useState } from 'react'
import { Search, Send, Youtube, RefreshCw } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"

export default function VideoSummaryMorphic() {
  const [lang, setLang] = useState('')
  const [videoUrl, setVideoUrl] = useState('')
  const [summary, setSummary] = useState('')
  const [transcript, setTranscript] = useState('')
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<Array<{type: 'qa'| 'answer'|'qst', content: string}>>([])
  const [loading, setLoading] = useState(false)

  // Función para extraer el ID del video de la URL si es necesario
  const getYouTubeID = (input: string) => {
    // Verifica si ya es un ID válido (11 caracteres, comúnmente usados por YouTube)
    if (/^[a-zA-Z0-9_-]{11}$/.test(input)) {
      return input
    }
    
    // Si no es un ID, intenta extraer el ID de la URL
    const match = input.match(/(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/)
    return match ? match[1] : null
  }
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const videoID = getYouTubeID(videoUrl)
    
    if (!videoID) {
      alert('Invalid YouTube ID or URL. Please enter a valid ID or URL.')
      return
    }
    setLoading(true)
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/video-summary/?name=${encodeURIComponent(videoID)}&lang=${encodeURIComponent(lang)}`, {
        method: 'POST',
      })
      
      const data = await response.json()
      if (response.ok) {
        setSummary(data.summary)
        setTranscript(data.transcript)
        setMessages(prev => [...prev, { type: 'answer', content: data.summary }])
      } else {
        alert(`Error: ${data.error || 'Unknown error occurred'}`)
      }
    } catch (error) {
      alert('Failed to fetch summary. Please try again.')
    }
    setLoading(false)
  }

  const handleQuestionSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!transcript) {
      alert('Please get a video summary first to ask questions about it.')
      return
    }
    setLoading(true)
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/ask-question/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question, transcript }),
      })
      const data = await response.json()
      if (response.ok) {
        setMessages(prev => [...prev, 
          { type: 'qst', content: `Q: ${question}` },
          { type: 'answer', content: `A: ${data.answer}` }
        ])
        setQuestion('')
      } else {
        alert(`Error: ${data.error || 'Unknown error occurred'}`)
      }
    } catch (error) {
      alert('Failed to get answer. Please try again.')
    }
    setLoading(false)
  }

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div className="w-[300px] border-r bg-muted/40 p-4 space-y-4">
        <div className="font-semibold text-lg flex items-center gap-2">
          <Youtube className="h-5 w-5" />
          Video Summary AI
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              value={videoUrl}
              onChange={(e) => setVideoUrl(e.target.value)}
              placeholder="Enter YouTube URL or ID"
              className="pl-8 my-2"
              required
            />
            <a className='text-gray-500 text-left text-sm'>Enter Video Language <br></br>(Ex: en for English): </a>
            <Input
              type="text"
              maxLength={2}
              value={lang}
              onChange={(e) => setLang(e.target.value)}
              placeholder="en"
              className="w-10 border p-2 rounded-md lowercase"
              required
            />
          </div>
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? <RefreshCw className="h-4 w-4 animate-spin" /> : 'Get Summary'}
          </Button>
        </form>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Messages Area */}
        <ScrollArea className="flex-1 p-4">
          <div className="space-y-4 max-w-3xl mx-auto">
            {messages.map((message, index) => (
              <Card key={index} className={cn(
                "p-4",
                message.type === 'answer' ? "bg-primary/5" : "bg-secondary/5"
              )}>
                <p className="whitespace-pre-wrap">{message.content}</p>
              </Card>
            ))}
          </div>
        </ScrollArea>

        {/* Question Input */}
        <div className="border-t p-4">
          <form onSubmit={handleQuestionSubmit} className="max-w-3xl mx-auto flex gap-2">
            <Input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder={transcript ? "Ask a question about the video..." : "Get a video summary first to ask questions"}
              disabled={!transcript || loading}
              className="flex-1"
            />
            <Button type="submit" disabled={!transcript || loading}>
              {loading ? (
                <RefreshCw className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </form>
        </div>
      </div>
    </div>
  ) 
}
