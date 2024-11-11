import { useState } from "react"

type Message = {
  author: 'user' | 'system',
  text: string
}

function App () {
  const [chatMessages, setChatMessages] = useState<Message[]>([])
  const [inputText, setInputText] = useState<string>("")

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(e.target.value)
  }

  const handleSend = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (inputText.trim()) {
      const newMessage: Message = {
        author: 'user',
        text: inputText
      }
      setChatMessages(prevMessages => [...prevMessages, newMessage])

      try {
        const response = await getResponse(newMessage.text)
        setChatMessages(prevMessages => [...prevMessages, { author: 'system', text: response }])
        setInputText("")
      }
      catch {
        console.log('Erro ao gerar resposta')
      }
    }
  }

  async function getResponse (input: string): Promise<string> {
    const response = await fetch('http://localhost:8000/predict', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        'text': input
      })
    })

    await new Promise(resolve => setTimeout(resolve, 3000)) // add 3 seconds delay

    const data = await response.json()
    return data.prediction
  }

  return (
    <div className="flex justify-center items-center h-screen w-full">
      <div className="container my-12 w-1/2 h-5/6 bg-white shadow-lg border border-gray-300 rounded-lg flex flex-col">
        <div className="navbar bg-neutral text-neutral-content rounded-t-lg p-4">
          <span className="text-xl font-bold">MoshiMoshi Bot</span>
        </div>
        <div className="flex flex-grow overflow-auto p-4 flex-col">
          {chatMessages.map((message: Message, index: number) => (
            <div key={index} className={`chat ${message.author === 'user' ? 'chat-end' : 'chat-start'} p-2`}>
              <div className={`chat-bubble ${message.author === 'user' ? 'bg-neutral' : 'bg-neutral'} rounded p-2 text-white`}>
                {message.text}
              </div>
            </div>
          ))}
        </div>
        <form className="p-2 relative" onSubmit={handleSend}>
          <input
            type="text"
            placeholder="Type here"
            className="input input-bordered w-full rounded-b-lg text-white"
            value={inputText}
            onChange={handleInputChange}
          />
          <button type="submit" className="flex items-center justify-center absolute right-4 bottom-4 w-8 h-8 rounded-lg bg-white hover:bg-slate-400">
            <img src="/arrow-up.svg" alt="Send" className="w-6 h-6" />
          </button>
        </form>
      </div>
    </div>
  )
}

export default App
