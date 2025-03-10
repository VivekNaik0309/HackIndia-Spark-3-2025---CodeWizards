import React, { useState } from "react";
import axios from "axios";

const Summarize = () => {
  const [docId, setDocId] = useState("");
  const [summary, setSummary] = useState("");

  const handleSummarize = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/summarize/?doc_id=${docId}`);
      setSummary(response.data.summary);
    } catch (error) {
      console.error("Error fetching summary:", error);
    }
  };

  return (
    <div>
      <h2>Summarize Document</h2>
      <input 
        type="text" 
        placeholder="Enter document ID..." 
        value={docId} 
        onChange={(e) => setDocId(e.target.value)}
      />
      <button onClick={handleSummarize}>Summarize</button>
      <p>{summary}</p>
    </div>
  );
};

export default Summarize;
