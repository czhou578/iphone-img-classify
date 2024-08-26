'use client'

import { useState } from "react";
import nlp from 'compromise'

export default function Home() {

  const [parameter, setParameter] = useState("")
  const [data, setData] = useState([])

  const getPythonRoute = "http://192.168.81.153:8080/get-images?"

  const extractKeywords = () => {
    const doc = nlp(parameter);
    
    // Use compromise to find the most relevant noun
    let keyword = '';

    // Match and extract noun or noun phrases
    const nouns = doc.nouns().out('array');

    if (nouns.length > 0) {
      // For simplicity, let's just take the first noun as the keyword
      keyword = nouns[nouns.length - 1];
    }

    return keyword
  }

  const handleSubmit = () => {
    let keyword = extractKeywords()
    fetch(getPythonRoute + new URLSearchParams({
      keyword: keyword.toString()
    }),
    {
      method: 'GET'
    }
  )
  .then((response: any) => {
    if (response.ok) return response.json();
  }).then((data) => {
    console.log(data);
    setData(data)
  })
  }

  return (
    <div>
      <div className="flex items-center justify-center">
        <div className="mt-20">
          <h1 className="mb-5">Enter A Prompt To Find Images</h1>
          <div>
            <input type="text" className="mb-5 text-black pl-1.5 mr-5" onChange={(e) => setParameter(e.target.value)}/>
            <button onClick={handleSubmit} className="bg-white text-black rounded-lg pl-5 pr-5 ">Enter</button>
          </div>
        </div>
      </div>
      <div style={{display: 'flex'}}>
        {data ? data.map((element: any, idx) => (
            <img
              key={idx}
              src={`data:image/png;base64,${element.path}`}
              width={500}
              height={500}
              alt="result image"
              style={{ width: "500px", height: "500px", objectFit: "cover" }} 
              />
        )): null}
      </div>
    </div>
  );
}
