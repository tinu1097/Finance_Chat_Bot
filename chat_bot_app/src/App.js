// import React, { useState, useEffect } from "react";
// import "./App.css";

// function App() {
//   const [messages, setMessages] = useState([]); // All messages
//   const [input, setInput] = useState("");
//   const [selectedModel, setSelectedModel] = useState(""); // Selected model
//   const [isModelDropdownOpen, setIsModelDropdownOpen] = useState(false);
//   const [chatSessions, setChatSessions] = useState([
//     { id: 1, name: "New Chat", history: [] },
//   ]);
//   const [selectedChat, setSelectedChat] = useState(1);
//   const [dualView, setDualView] = useState(false); // Dual view for both models
//   const [modelPreference, setModelPreference] = useState(""); // Store model preference

//   useEffect(() => {
//     // Initial greeting message
//     setMessages([{ sender: "Bot", text: "Hi, how can I help you?" }]);
//   }, []);

//   const handleSend = async () => {
//     if (!input.trim()) return;

//     // Save user message
//     const userMessage = { sender: "User", text: input };
//     setMessages((prev) => [...prev, userMessage]);
//     setInput("");

//     // Save message to current chat session
//     const updatedSessions = chatSessions.map((chat) =>
//       chat.id === selectedChat
//         ? { ...chat, history: [...chat.history, userMessage] }
//         : chat
//     );
//     setChatSessions(updatedSessions);

//     // Fetch responses from models
//     try {
//       let gptMessage = {};
//       let customMessage = {};

//       if (modelPreference === "GPT_Model" || modelPreference === "Both") {
//         try {
//           const gptResponse = await fetch(`http://127.0.0.1:5000/get_company_info`, {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ query: input }), // Corrected to match the Flask API's expected key
//           });
//           const gptData = await gptResponse.json();
//           console.log("Error",gptData)
//           gptMessage = {
//             sender: "GPT_Model",
//             text: gptData.answer || "No response",
//           };
//         } catch {
//           gptMessage = {
//             sender: "GPT_Model",
//             text: "Error from GPT_Model API",
//           };
//         }
//       }

//       try {
//         const customResponse = await fetch(
//           `http://127.0.0.1:5000/ask_questions`,
//           {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ question: input }), // input is the question
//           }
//         );
    
//         const customData = await customResponse.json();
    
//         // The correct key is "answer" based on your Flask API
//         const customMessage = {
//           sender: "Custom_Model",
//           text: customData.answer || "No response", // Access 'answer' here
//         };
//     } catch (error) {
//         const customMessage = {
//           sender: "Custom_Model",
//           text: "Error from Custom_Model API",
//         };
//         console.error(error); // Log the error for debugging
//     }
    

//       // Update messages based on selected model
//       const newMessages = [
//         ...(modelPreference === "Both" ? [gptMessage, customMessage] : []),
//         ...(modelPreference === "GPT_Model" ? [gptMessage] : []),
//         ...(modelPreference === "Custom_Model" ? [customMessage] : []),
//       ];

//       setMessages((prev) => [...prev, ...newMessages]);

//       // Save responses to chat history
//       const updatedSessionsWithResponses = chatSessions.map((chat) =>
//         chat.id === selectedChat
//           ? { ...chat, history: [...chat.history, ...newMessages] }
//           : chat
//       );
//       setChatSessions(updatedSessionsWithResponses);
//     } catch {
//       setMessages((prev) => [
//         ...prev,
//         { sender: "Bot", text: "An error occurred." },
//       ]);
//     }
//   };

//   const toggleModelDropdown = () => {
//     setIsModelDropdownOpen(!isModelDropdownOpen);
//   };

//   const selectModel = (model) => {
//     setSelectedModel(model);
//     setIsModelDropdownOpen(false);
//     setModelPreference(model);
//     setDualView(model === "Both");
//   };

//   const addNewChat = () => {
//     const newChatId = chatSessions.length + 1;
//     setChatSessions([
//       ...chatSessions,
//       { id: newChatId, name: `Chat ${newChatId}`, history: [] },
//     ]);
//     setSelectedChat(newChatId);
//     setMessages([]);
//   };

//   const switchChat = (chatId) => {
//     const selectedChatHistory =
//       chatSessions.find((chat) => chat.id === chatId)?.history || [];
//     setSelectedChat(chatId);
//     setMessages(selectedChatHistory);
//   };

//   return (
//     <div className="App">
//       {/* Sidebar */}
//       <div className="sidebar">
//         <div className="header">
//           <button className="add-chat-btn" onClick={addNewChat}>
//             Add New Chat
//           </button>
//         </div>
//         <h3>Chat History</h3>
//         <div className="chat-list">
//           {chatSessions.map((chat) => (
//             <div
//               key={chat.id}
//               className={`chat-item ${chat.id === selectedChat ? "active" : ""}`}
//               onClick={() => switchChat(chat.id)}
//             >
//               {chat.name}
//             </div>
//           ))}
//         </div>
//       </div>

//       {/* Main Chat Section */}
//       <div className={`main ${dualView ? "dual-view" : ""}`}>
//         {/* Chat Window */}
//         <div className="chat-window">
//           {messages.map((message, index) => (
//             <div key={index} className={`message ${message.sender}`}>
//               <strong>{message.sender}: </strong>
//               {message.text}
//             </div>
//           ))}
//         </div>

//         {/* Dual Model Views */}
//         {dualView && (
//           <div className="dual-view-container">
//             <div className="dual-view-column">
//               <h3>Response from Custom_Model</h3>
//               {messages
//                 .filter((msg) => msg.sender === "Custom_Model")
//                 .map((msg, index) => (
//                   <div key={index} className="message Custom_Model">
//                     <strong>{msg.sender}: </strong>
//                     {msg.text}
//                   </div>
//                 ))}
//             </div>

//             <div className="dual-view-column">
//               <h3>Response from GPT_Model</h3>
//               {messages
//                 .filter((msg) => msg.sender === "GPT_Model")
//                 .map((msg, index) => (
//                   <div key={index} className="message GPT_Model">
//                     <strong>{msg.sender}: </strong>
//                     {msg.text}
//                   </div>
//                 ))}
//             </div>
//           </div>
//         )}

//         {/* Chat Input Section */}
//         <div className="chat-input">
//           <div className="model-dropdown">
//             <button className="model-dropdown-btn" onClick={toggleModelDropdown}>
//               {selectedModel || "Select Model"}
//             </button>
//             {isModelDropdownOpen && (
//               <div className="model-dropdown-menu">
//                 <div
//                   className="dropdown-item"
//                   onClick={() => selectModel("GPT_Model")}
//                 >
//                   GPT_Model
//                 </div>
//                 <div
//                   className="dropdown-item"
//                   onClick={() => selectModel("Custom_Model")}
//                 >
//                   Custom_Model
//                 </div>
//                 <div
//                   className="dropdown-item"
//                   onClick={() => selectModel("Both")}
//                 >
//                   Use Dual Model
//                 </div>
//               </div>
//             )}
//           </div>

//           <input
//             type="text"
//             className="input-box"
//             placeholder="Type a question..."
//             value={input}
//             onChange={(e) => setInput(e.target.value)}
//             onKeyDown={(e) => e.key === "Enter" && handleSend()}
//           />
//           <button className="send-btn" onClick={handleSend}>
//             Send
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;



import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]); // All messages
  const [input, setInput] = useState("");
  const [selectedModel, setSelectedModel] = useState(""); // Selected model
  const [isModelDropdownOpen, setIsModelDropdownOpen] = useState(false);
  const [chatSessions, setChatSessions] = useState([
    { id: 1, name: "New Chat", history: [] },
  ]);
  const [selectedChat, setSelectedChat] = useState(1);
  const [dualView, setDualView] = useState(false); // Dual view for both models
  const [modelPreference, setModelPreference] = useState(""); // Store model preference

  useEffect(() => {
    // Initial greeting message
    setMessages([{ sender: "Bot", text: "Hi, how can I help you?" }]);
  }, []);

  const handleSend = async () => {
    if (!input.trim()) return;

    // Save user message
    const userMessage = { sender: "User", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    // Save message to current chat session
    const updatedSessions = chatSessions.map((chat) =>
      chat.id === selectedChat
        ? { ...chat, history: [...chat.history, userMessage] }
        : chat
    );
    setChatSessions(updatedSessions);

    // Fetch responses from models
    try {
      let gptMessage = null;
      let customMessage = null;

      // Fetch response from GPT_Model if selected
      if (modelPreference === "GPT_Model" || modelPreference === "Both") {
        try {
          const gptResponse = await fetch("http://192.168.1.22:5000/get_company_info", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: input }),
          });
          const gptData = await gptResponse.json();
          gptMessage = {
            sender: "GPT_Model",
            text: gptData.answer || "No response from GPT_Model",
          };
        } catch (error) {
          console.error("Error from GPT_Model API:", error);
          gptMessage = {
            sender: "GPT_Model",
            text: "Error from GPT_Model API",
          };
        }
      }

      // Fetch response from Custom_Model if selected
      if (modelPreference === "Custom_Model" || modelPreference === "Both") {
        try {
          const customResponse = await fetch("http://127.0.0.1:5000/ask_questions", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: input }),
          });
          const customData = await customResponse.json();
          customMessage = {
            sender: "Custom_Model",
            text: customData.answer || "No response from Custom_Model",
          };
        } catch (error) {
          console.error("Error from Custom_Model API:", error);
          customMessage = {
            sender: "Custom_Model",
            text: "Error from Custom_Model API",
          };
        }
      }

      // Prepare new messages based on model preferences
      const newMessages = [
        ...(gptMessage ? [gptMessage] : []),
        ...(customMessage ? [customMessage] : []),
      ];

      setMessages((prev) => [...prev, ...newMessages]);

      // Update chat history with responses
      const updatedSessionsWithResponses = chatSessions.map((chat) =>
        chat.id === selectedChat
          ? { ...chat, history: [...chat.history, ...newMessages] }
          : chat
      );
      setChatSessions(updatedSessionsWithResponses);
    } catch (error) {
      console.error("An unexpected error occurred:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "Bot", text: "An error occurred while processing your request." },
      ]);
    }
  };

  const toggleModelDropdown = () => {
    setIsModelDropdownOpen(!isModelDropdownOpen);
  };

  const selectModel = (model) => {
    setSelectedModel(model);
    setIsModelDropdownOpen(false);
    setModelPreference(model);
    setDualView(model === "Both");
  };

  const addNewChat = () => {
    const newChatId = chatSessions.length + 1;
    setChatSessions([
      ...chatSessions,
      { id: newChatId, name: `Chat ${newChatId}`, history: [] },
    ]);
    setSelectedChat(newChatId);
    setMessages([]);
  };

  const switchChat = (chatId) => {
    const selectedChatHistory =
      chatSessions.find((chat) => chat.id === chatId)?.history || [];
    setSelectedChat(chatId);
    setMessages(selectedChatHistory);
  };

  return (
    <div className="App">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="header">
          <button className="add-chat-btn" onClick={addNewChat}>
            Add New Chat
          </button>
        </div>
        <h3>Chat History</h3>
        <div className="chat-list">
          {chatSessions.map((chat) => (
            <div
              key={chat.id}
              className={`chat-item ${chat.id === selectedChat ? "active" : ""}`}
              onClick={() => switchChat(chat.id)}
            >
              {chat.name}
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Section */}
      <div className={`main ${dualView ? "dual-view" : ""}`}>
        {/* Chat Window */}
        <div className="chat-window">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <strong>{message.sender}: </strong>
              {message.text}
            </div>
          ))}
        </div>

        {/* Dual Model Views */}
        {dualView && (
          <div className="dual-view-container">
            <div className="dual-view-column">
              <h3>Response from Custom_Model</h3>
              {messages
                .filter((msg) => msg.sender === "Custom_Model")
                .map((msg, index) => (
                  <div key={index} className="message Custom_Model">
                    <strong>{msg.sender}: </strong>
                    {msg.text}
                  </div>
                ))}
            </div>

            <div className="dual-view-column">
              <h3>Response from GPT_Model</h3>
              {messages
                .filter((msg) => msg.sender === "GPT_Model")
                .map((msg, index) => (
                  <div key={index} className="message GPT_Model">
                    <strong>{msg.sender}: </strong>
                    {msg.text}
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* Chat Input Section */}
        <div className="chat-input">
          <div className="model-dropdown">
            <button className="model-dropdown-btn" onClick={toggleModelDropdown}>
              {selectedModel || "Select Model"}
            </button>
            {isModelDropdownOpen && (
              <div className="model-dropdown-menu">
                <div
                  className="dropdown-item"
                  onClick={() => selectModel("GPT_Model")}
                >
                  GPT_Model
                </div>
                <div
                  className="dropdown-item"
                  onClick={() => selectModel("Custom_Model")}
                >
                  Custom_Model
                </div>
                <div
                  className="dropdown-item"
                  onClick={() => selectModel("Both")}
                >
                  Use Dual Model
                </div>
              </div>
            )}
          </div>

          <input
            type="text"
            className="input-box"
            placeholder="Type a question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button className="send-btn" onClick={handleSend}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
