import React, { useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [chatResponse, setChatResponse] = useState("");

  const [imagePrompt, setImagePrompt] = useState("");
  const [image, setImage] = useState("");

  const [selectedFile, setSelectedFile] = useState(null);
  const [fileSummary, setFileSummary] = useState("");

  // ---------------- CHAT ----------------
  const handleChat = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/chat", {
        message,
      });
      console.log("Chat:", response.data);
      setChatResponse(response.data.reply);
    } catch (error) {
      console.error("Chat error:", error);
      setChatResponse("Error: Could not reach backend.");
    }
  };

  // ---------------- IMAGE ----------------
  const handleImageGenerate = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/image", {
        prompt: imagePrompt,
      });

      console.log("Image response:", response.data);

      if (response.data.base64) {
        setImage(response.data.base64);
      } else {
        alert("Image generation failed: " + response.data.error);
      }
    } catch (error) {
      console.error("Image error:", error);
      alert("Network error — check backend.");
    }
  };

  // ---------------- SUMMARY ----------------
  const handleFileUpload = async () => {
    if (!selectedFile) {
      alert("Upload a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/summarize",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      console.log("Summary:", response.data);
      setFileSummary(response.data.summary);
    } catch (error) {
      console.error("Summary error:", error);
      setFileSummary("Error summarizing file.");
    }
  };

  return (
    <div style={{ padding: 40, fontFamily: "Arial" }}>
      <h1>UniAI — your companion</h1>

      {/* ------------ CHAT ------------ */}
      <h2>Chat</h2>
      <textarea
        rows="4"
        style={{ width: "100%" }}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
      ></textarea>
      <button onClick={handleChat} style={{ marginTop: 10 }}>
        Send
      </button>

      {chatResponse && (
        <div
          style={{
            marginTop: 20,
            padding: 10,
            background: "#f7f7f7",
            borderRadius: 6,
            whiteSpace: "pre-wrap",
          }}
        >
          {chatResponse}
        </div>
      )}

      {/* ------------ IMAGE ------------ */}
      <h2 style={{ marginTop: 40 }}>Image</h2>
      <input
        type="text"
        value={imagePrompt}
        onChange={(e) => setImagePrompt(e.target.value)}
        placeholder="Enter an image prompt..."
        style={{ width: "100%", padding: 8 }}
      />
      <button onClick={handleImageGenerate} style={{ marginTop: 10 }}>
        Generate
      </button>

      {image && (
        <div style={{ marginTop: 20 }}>
          <img
            src={`data:image/jpeg;base64,${image}`}
            alt="Generated"
            style={{ width: 300, borderRadius: "8px" }}
          />
        </div>
      )}

      {/* ------------ SUMMARY ------------ */}
      <h2 style={{ marginTop: 40 }}>Document Summary</h2>
      <input type="file" onChange={(e) => setSelectedFile(e.target.files[0])} />

      <button onClick={handleFileUpload} style={{ marginLeft: 10 }}>
        Upload & Summarize
      </button>

      <div
        style={{
          marginTop: 20,
          background: "#f4f4f4",
          padding: 10,
          borderRadius: 6,
        }}
      >
        {fileSummary}
      </div>
    </div>
  );
}

export default App;