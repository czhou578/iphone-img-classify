'use client'

import { useState } from "react";

export default function Home() {

  const [parameter, setParameter] = useState("")
  const [data, setData] = useState([])

  const getPythonRoute = "http://192.168.81.153:8080/get-images?"

  const handleSubmit = () => {
    fetch(getPythonRoute + new URLSearchParams({
      keyword: parameter.toString()
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
      <div className="flex items-center justify-center min-h-screen">
        <div>
          <h1 className="mb-5">Enter Parameters</h1>
          <div>
            <input type="text" className="mb-5 text-black pl-1.5" onChange={(e) => setParameter(e.target.value)}/>
            <button onClick={handleSubmit}>Enter</button>
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
