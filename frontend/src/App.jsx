// App.jsx

import React, { useEffect, useState } from "react";
import axios from "axios";

export default function App() {
	const [physicianId, setPhysicianId] = useState("");
	const [messages, setMessages] = useState([]);
	const [loading, setLoading] = useState(false);

	const fetchMessages = async () => {
		if (!physicianId) return;
		setLoading(true);
		try {
			const res = await axios.get(`http://localhost:8000/messages?physician_id=${physicianId}`);
			setMessages(res.data);
		} catch (err) {
			console.error("Error fetching messages", err);
		} finally {
			setLoading(false);
		}
	};

	const classifyMessage = async (messageId) => {
		try {
			const res = await axios.post(`http://localhost:8000/classify/${messageId}`);
			const triggered = res.data.triggered_rules;
			alert( triggered.length > 0 
				? `Triggered rules:\n${triggered.map((r) => r.name).join("\n")}`
				: "No rules triggered."
			);
		} catch (err) {
			console.error("Error classifying message", err);
		}
	};

	return (
		<div style={{ fontFamily: "sans-serif", padding: 20 }}> 
			<h1>Healthcare Engagement Dashboard</h1>
			  <div style={{ marginBottom: 20 }}>
			    <label>
					Physician ID:&nbsp;
				      <input
				        value={physicianId}
				        onChange={(e) => setPhysicianId(e.target.value)}
				        placeholder="Enter Physician ID"
				      />
			    </label>
			    <button onClick={fetchMessages} disabled={!physicianId || loading}>
			      {loading ? "Loading..." : "Search"}
			    </button>
			  </div>

  {messages.length > 0 && (
    <table border="1" cellPadding="6" style={{ borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>Topic</th>
          <th>Sentiment</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {messages.map((m) => (
          <tr key={m.message_id}>
            <td>{new Date(m.timestamp).toLocaleString()}</td>
            <td>{m.topic}</td>
            <td>{m.sentiment}</td>
            <td>
              <button onClick={() => classifyMessage(m.message_id)}>Classify</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )}

  {messages.length === 0 && !loading && (
    <p style={{ color: "gray" }}>No messages found. Try searching by physician ID.</p>
  )}
</div>

	); //close return
} //close function
