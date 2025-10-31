const { useState } = React;

const GOLD = "#FFC72C";
const NAVY = "#142857";
const SLATE = "#1C2540";
const CLOUD = "#F5F7FB";
const BORDER = "rgba(20, 40, 87, 0.12)";

const navLinks = ["Seminars", "Appointments", "Facebook", "Instagram", "Website Leads"];

const heroConversation = [
  {
    role: "agent",
    sender: "AI Agent",
    text: "Welcome to ProVision Brokerage! How can I help you today? I can assist with lead qualification, booking appointments, answering FAQs, and more."
  },
  {
    role: "user",
    sender: "You",
    text: "I'd like to learn about your seminars."
  },
  {
    role: "agent",
    sender: "AI Agent",
    text: 'Of course! We have an upcoming webinar on "Retirement Planning Strategies" this Friday. Would you like to register?'
  }
];

function Header({ activePage, onNavigate }) {

  return (
    <header
      style={{
        background: "#ffffff",
        borderBottom: `1px solid ${BORDER}`
      }}
    >
      <div
        style={{
          maxWidth: 1280,
          margin: "0 auto",
          padding: "18px 40px 10px",
          width: "100%"
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            width: "100%"
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 14
            }}
            onClick={() => onNavigate("home")}
            role="button"
            tabIndex={0}
            onKeyDown={(event) => {
              if (event.key === "Enter" || event.key === " ") {
                onNavigate("home");
              }
            }}
          >
            <span
              style={{
                display: "inline-flex",
                width: 34,
                height: 34,
                borderRadius: "50%",
                background: GOLD,
                alignItems: "center",
                justifyContent: "center",
                color: NAVY,
                fontWeight: 800,
                fontSize: "0.9em",
                boxShadow: "0 10px 24px rgba(255, 199, 44, 0.35)"
              }}
            >
              PB
            </span>
            <span
              style={{
                fontWeight: 800,
                fontSize: "1.18em",
                color: NAVY,
                letterSpacing: "-0.01em",
                cursor: "pointer"
              }}
            >
              ProVision Brokerage
            </span>
          </div>
          <nav
            style={{
              display: "flex",
              gap: 26,
              marginLeft: 36,
              fontWeight: 600,
              fontSize: "1.02em",
              color: NAVY
            }}
          >
            {navLinks.map((item) => {
              const isActive = activePage === item;
              return (
                <a
                  key={item}
                  href="#"
                  onClick={(event) => {
                    event.preventDefault();
                    onNavigate(item);
                  }}
            style={{
              textDecoration: "none",
              color: isActive ? "#ffffff" : "inherit",
              background: isActive ? "#000000" : "transparent",
              padding: "6px 14px",
              borderRadius: 6,
              letterSpacing: "0.08em",
              fontSize: "0.82em",
              textTransform: "uppercase",
              fontWeight: 700,
              transition: "background 0.2s ease, color 0.2s ease"
            }}
                >
                  {item}
                </a>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
}

function ChatMessage({ role, sender, text }) {
  const isUser = role === "user";
  return (
    <div
      style={{
        display: "flex",
        alignItems: "flex-end",
        justifyContent: isUser ? "flex-end" : "flex-start",
        gap: 12,
        marginBottom: isUser ? 20 : 14
      }}
    >
      {!isUser && (
        <div
          style={{
            width: 36,
            height: 36,
            borderRadius: "50%",
            backgroundImage: "url('https://i.pravatar.cc/72?img=47')",
            backgroundSize: "cover",
            backgroundPosition: "center",
            boxShadow: "0 6px 12px rgba(20, 40, 87, 0.18)",
            flexShrink: 0
          }}
        />
      )}
      <div
        style={{
          background: isUser ? GOLD : CLOUD,
          color: isUser ? NAVY : SLATE,
          padding: "14px 16px",
          borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
          maxWidth: 240,
          fontSize: "0.96em",
          lineHeight: 1.5,
          fontWeight: 500,
          boxShadow: isUser
            ? "0 12px 24px rgba(255, 199, 44, 0.32)"
            : "0 10px 20px rgba(20, 40, 87, 0.12)"
        }}
      >
        {!isUser && (
          <div
            style={{
              fontSize: "0.76em",
              fontWeight: 600,
              color: "#717C99",
              marginBottom: 6,
              textTransform: "uppercase",
              letterSpacing: "0.08em"
            }}
          >
            {sender}
          </div>
        )}
        {text}
      </div>
      {isUser && (
        <div
          style={{
            width: 30,
            height: 30,
            borderRadius: "50%",
            background: `linear-gradient(135deg, ${GOLD}, #FF9F1C)`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#fff",
            fontWeight: 700,
            fontSize: "0.72em",
            boxShadow: "0 10px 20px rgba(255, 159, 28, 0.35)",
            flexShrink: 0
          }}
        >
          You
        </div>
      )}
    </div>
  );
}

function DeviceMock({ pageContext = "home", initialMessage = "Hi. I'm Sarah from ProVision Brokerage, how can I help you?", showChannelToggle = false, channelMode: initialChannelMode = null }) {
  const [messages, setMessages] = useState([
    {
      role: "agent",
      sender: "AI Agent",
      text: initialMessage
    }
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [channelMode, setChannelMode] = useState(initialChannelMode || (showChannelToggle ? "sms" : "web")); // Use provided mode, or default based on toggle
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(`widget_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      role: "user",
      sender: "You",
      text: inputMessage
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage("");
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          session_id: sessionId,
          channel: channelMode || "web",
          context: {
            page: pageContext || "home"
          }
        })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      const agentMessage = {
        role: "agent",
        sender: "AI Agent",
        text: data.message
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: "agent",
        sender: "AI Agent",
        text: "I apologize, but I'm experiencing technical difficulties. Please try again or contact our support team."
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Channel-specific styles
  const getChannelStyles = () => {
    if (channelMode === "neuralapps") {
      return {
        container: {
          background: "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
          borderRadius: 20,
          padding: "20px",
          position: "relative",
          overflow: "hidden"
        },
        header: {
          textTransform: "uppercase",
          fontSize: "0.7em",
          letterSpacing: "0.15em",
          color: "#94a3b8",
          fontWeight: 600,
          marginBottom: 18,
          display: "flex",
          alignItems: "center",
          gap: 8
        },
        headerText: "NEURALAPPS.AI POWERED",
        userBubble: {
          background: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
          color: "#fff",
          padding: "10px 16px",
          borderRadius: "16px 16px 4px 16px",
          fontSize: "0.9em",
          maxWidth: "80%",
          alignSelf: "flex-end",
          boxShadow: "0 4px 12px rgba(99, 102, 241, 0.3)"
        },
        agentBubble: {
          background: "rgba(148, 163, 184, 0.1)",
          color: "#e2e8f0",
          padding: "10px 16px",
          borderRadius: "16px 16px 16px 4px",
          fontSize: "0.9em",
          maxWidth: "80%",
          alignSelf: "flex-start",
          border: "1px solid rgba(148, 163, 184, 0.2)"
        },
        inputStyle: {
          flex: 1,
          padding: "8px 12px",
          border: "1px solid rgba(148, 163, 184, 0.3)",
          borderRadius: 20,
          fontSize: "0.85em",
          outline: "none",
          background: "rgba(15, 23, 42, 0.5)",
          color: "#e2e8f0"
        }
      };
    } else if (channelMode === "instagram") {
      return {
        container: {
          background: "#ffffff",
          borderRadius: 20,
          padding: "0"
        },
        header: {
          display: "flex",
          alignItems: "center",
          gap: 12,
          marginBottom: 0,
          padding: "16px",
          background: "#fff",
          borderBottom: "1px solid #dbdbdb",
          borderRadius: "20px 20px 0 0"
        },
        headerText: {
          fontSize: "0.95em",
          color: "#262626",
          fontWeight: 600
        },
        userBubble: {
          background: "#3797f0",
          color: "#fff",
          padding: "10px 16px",
          borderRadius: "20px",
          maxWidth: "75%",
          alignSelf: "flex-end",
          fontSize: "0.95em"
        },
        agentBubble: {
          background: "#efefef",
          color: "#000",
          padding: "10px 16px",
          borderRadius: "20px",
          maxWidth: "75%",
          alignSelf: "flex-start",
          fontSize: "0.95em",
          border: "1px solid #dbdbdb"
        },
        inputStyle: {
          background: "#fff",
          border: "1px solid #dbdbdb",
          borderRadius: 22,
          padding: "10px 16px",
          fontSize: "0.9em"
        }
      };
    } else if (channelMode === "facebook") {
      return {
        container: {
          background: "#ffffff",
          borderRadius: 20,
          padding: "0"
        },
        header: {
          display: "flex",
          alignItems: "center",
          gap: 12,
          marginBottom: 0,
          padding: "16px",
          background: "linear-gradient(90deg, #0084ff 0%, #0066cc 100%)",
          borderRadius: "20px 20px 0 0"
        },
        headerText: {
          fontSize: "0.95em",
          color: "#fff",
          fontWeight: 600
        },
        userBubble: {
          background: "#0084ff",
          color: "#fff",
          padding: "10px 16px",
          borderRadius: "18px",
          maxWidth: "75%",
          alignSelf: "flex-end",
          fontSize: "0.95em"
        },
        agentBubble: {
          background: "#F0F0F0",
          color: "#000",
          padding: "10px 16px",
          borderRadius: "18px",
          maxWidth: "75%",
          alignSelf: "flex-start",
          fontSize: "0.95em"
        },
        inputStyle: {
          background: "#f4f4f4",
          border: "none",
          borderRadius: 20,
          padding: "10px 16px",
          fontSize: "0.9em"
        }
      };
    } else if (channelMode === "sms") {
      return {
        container: {
          background: pageContext === "seminars" 
            ? "#e8f4ff" 
            : "#f0f0f0",
          backgroundImage: pageContext === "seminars"
            ? "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"200\" height=\"200\"><defs><pattern id=\"seminar-pattern\" width=\"40\" height=\"40\" patternUnits=\"userSpaceOnUse\"><text x=\"10\" y=\"25\" font-size=\"20\" fill=\"%23007AFF\" opacity=\"0.08\"></text></pattern></defs><rect width=\"200\" height=\"200\" fill=\"url(%23seminar-pattern)\"/></svg>')"
            : "none",
          borderRadius: 20,
          padding: "20px 16px"
        },
        header: {
          display: "flex",
          alignItems: "center",
          gap: 8,
          marginBottom: 16,
          paddingBottom: 12,
          borderBottom: pageContext === "seminars" ? "1px solid #007AFF" : "1px solid #ddd"
        },
        headerText: {
          fontSize: "0.9em",
          color: pageContext === "seminars" ? "#007AFF" : "#333",
          fontWeight: 600
        },
        userBubble: {
          background: "#007AFF",
          color: "#fff",
          padding: "10px 14px",
          borderRadius: "18px 18px 4px 18px",
          maxWidth: "75%",
          alignSelf: "flex-end"
        },
        agentBubble: {
          background: pageContext === "seminars" ? "#ffffff" : "#E5E5EA",
          color: "#000",
          padding: "10px 14px",
          borderRadius: "18px 18px 18px 4px",
          maxWidth: "75%",
          alignSelf: "flex-start",
          boxShadow: pageContext === "seminars" ? "0 2px 8px rgba(0, 122, 255, 0.1)" : "none"
        },
        inputStyle: {
          background: "#fff",
          border: pageContext === "seminars" ? "1px solid #007AFF" : "1px solid #ccc",
          borderRadius: 20,
          padding: "10px 16px",
          fontSize: "0.9em"
        }
      };
    } else if (channelMode === "whatsapp") {
      return {
        container: {
          background: "#ECE5DD",
          backgroundImage: "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"300\" height=\"300\"><defs><pattern id=\"p\" width=\"40\" height=\"40\" patternUnits=\"userSpaceOnUse\"><circle cx=\"20\" cy=\"20\" r=\"2\" fill=\"%23D9D9D9\" opacity=\"0.3\"/></pattern></defs><rect width=\"300\" height=\"300\" fill=\"url(%23p)\"/></svg>')",
          borderRadius: 20,
          padding: "20px 16px"
        },
        header: {
          display: "flex",
          alignItems: "center",
          gap: 12,
          marginBottom: 16,
          paddingBottom: 12,
          background: "#075E54",
          margin: "-20px -16px 16px -16px",
          padding: "16px 16px",
          borderRadius: "20px 20px 0 0"
        },
        headerText: {
          fontSize: "0.95em",
          color: "#fff",
          fontWeight: 600
        },
        userBubble: {
          background: "#DCF8C6",
          color: "#000",
          padding: "8px 12px",
          borderRadius: "8px 8px 0 8px",
          maxWidth: "75%",
          alignSelf: "flex-end",
          boxShadow: "0 1px 2px rgba(0,0,0,0.1)"
        },
        agentBubble: {
          background: "#FFFFFF",
          color: "#000",
          padding: "8px 12px",
          borderRadius: "8px 8px 8px 0",
          maxWidth: "75%",
          alignSelf: "flex-start",
          boxShadow: "0 1px 2px rgba(0,0,0,0.1)"
        },
        inputStyle: {
          background: "#fff",
          border: "none",
          borderRadius: 20,
          padding: "10px 16px",
          fontSize: "0.9em"
        }
      };
    } else {
      // Web chat (default)
      return {
        container: {
          background: "linear-gradient(135deg, #ffffff 0%, #F5F7FB 50%, #E8ECF7 100%)",
          borderRadius: 30,
          padding: "35px 28px",
          position: "relative",
          overflow: "hidden"
        },
        header: {
          textTransform: "uppercase",
          fontSize: "0.72em",
          letterSpacing: "0.14em",
          color: "#8D97AF",
          fontWeight: 600,
          marginBottom: 18
        },
        headerText: "AI Agent",
        userBubble: {
          background: GOLD,
          color: NAVY,
          padding: "14px 20px",
          borderRadius: "18px 18px 4px 18px",
          fontSize: "0.96em"
        },
        agentBubble: {
          background: CLOUD,
          color: SLATE,
          padding: "14px 16px",
          borderRadius: "18px 18px 18px 4px",
          fontSize: "0.96em"
        },
        inputStyle: {
          flex: 1,
          padding: "8px 12px",
          border: "1px solid #ddd",
          borderRadius: 20,
          fontSize: "0.9em",
          outline: "none"
        }
      };
    }
  };

  const styles = getChannelStyles();

  return (
    <>
        <div
          style={{
            position: "relative",
            width: 420,
            maxWidth: "100%"
          }}
        >
      <div
        style={{
          position: "absolute",
          inset: "-18% -12% -18% -12%",
          background:
            "radial-gradient(70% 60% at 50% 35%, rgba(255, 170, 0, 0.65) 0%, rgba(255, 125, 0, 0.12) 58%, rgba(255, 125, 0, 0))",
          filter: "blur(18px)",
          opacity: 0.9,
          zIndex: 0
        }}
      />
      <div
        style={{
          position: "relative",
          background: channelMode === "neuralapps" ? "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)" : (channelMode === "instagram" ? "linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)" : (channelMode === "facebook" ? "#0084ff" : (channelMode === "whatsapp" ? "#075E54" : NAVY))),
          borderRadius: 42,
          padding: "28px 24px",
          boxShadow: "0 30px 60px rgba(20, 40, 87, 0.28)",
          zIndex: 1
        }}
      >
        <div
          style={{
            ...styles.container,
            minHeight: 580,
            boxShadow: "0 18px 28px rgba(20, 40, 87, 0.12)"
          }}
        >
          {/* Web Chat Watermark (only for web mode) */}
          {channelMode === "web" && (
            <>
              <div
                style={{
                  position: "absolute",
                  top: "50%",
                  left: "50%",
                  transform: "translate(-50%, -50%)",
                  fontSize: "120px",
                  fontWeight: 900,
                  color: "rgba(255, 199, 44, 0.03)",
                  letterSpacing: "-0.02em",
                  pointerEvents: "none",
                  userSelect: "none",
                  zIndex: 0
                }}
              >
                PB
              </div>
              <div
                style={{
                  position: "absolute",
                  bottom: "-20px",
                  right: "-20px",
                  width: "150px",
                  height: "150px",
                  borderRadius: "50%",
                  background: "radial-gradient(circle, rgba(255, 199, 44, 0.08) 0%, transparent 70%)",
                  pointerEvents: "none",
                  zIndex: 0
                }}
              />
              <div
                style={{
                  position: "absolute",
                  top: "-30px",
                  left: "-30px",
                  width: "120px",
                  height: "120px",
                  borderRadius: "50%",
                  background: "radial-gradient(circle, rgba(20, 40, 87, 0.04) 0%, transparent 70%)",
                  pointerEvents: "none",
                  zIndex: 0
                }}
              />
            </>
          )}
          
          {/* NeuralApps Watermark (only for neuralapps mode) */}
          {channelMode === "neuralapps" && (
            <>
              <div
                style={{
                  position: "absolute",
                  top: "50%",
                  left: "50%",
                  transform: "translate(-50%, -50%)",
                  fontSize: "80px",
                  fontWeight: 900,
                  color: "rgba(99, 102, 241, 0.08)",
                  letterSpacing: "0.05em",
                  pointerEvents: "none",
                  userSelect: "none",
                  zIndex: 0,
                  textAlign: "center",
                  lineHeight: 1
                }}
              >
                NEURAL<br/>APPS
              </div>
              <div
                style={{
                  position: "absolute",
                  bottom: "20px",
                  right: "20px",
                  fontSize: "0.7em",
                  color: "rgba(148, 163, 184, 0.5)",
                  fontWeight: 600,
                  letterSpacing: "0.1em",
                  pointerEvents: "none",
                  userSelect: "none",
                  zIndex: 0
                }}
              >
                POWERED BY NEURALAPPS.AI
              </div>
            </>
          )}
          
          {/* Header */}
          <div style={styles.header}>
            {channelMode === "neuralapps" && (
              <>
                <span style={{ fontSize: "1.2em" }}></span>
                <span>{styles.headerText}</span>
              </>
            )}
            {channelMode === "instagram" && (
              <>
                <div style={{ width: 40, height: 40, borderRadius: "50%", background: "linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "1.3em", color: "#fff" }}>
                  
                </div>
                <div style={{ flex: 1 }}>
                  <div style={styles.headerText}>provisionbrokerage</div>
                  <div style={{ fontSize: "0.75em", color: "#8e8e8e" }}>Active now</div>
                </div>
                <div style={{ fontSize: "1.3em", color: "#262626", cursor: "pointer" }}></div>
              </>
            )}
            {channelMode === "facebook" && (
              <>
                <div style={{ width: 40, height: 40, borderRadius: "50%", background: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "1.3em" }}>
                  
                </div>
                <div>
                  <div style={styles.headerText}>ProVision Brokerage</div>
                  <div style={{ fontSize: "0.75em", color: "rgba(255,255,255,0.9)" }}>Typically replies instantly</div>
                </div>
              </>
            )}
            {channelMode === "whatsapp" && (
              <>
                <div style={{ width: 40, height: 40, borderRadius: "50%", background: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "1.5em" }}>
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" fill="#25D366"/>
                  </svg>
                </div>
                <div>
                  <div style={styles.headerText}>Sarah - ProVision</div>
                  <div style={{ fontSize: "0.75em", color: "rgba(255,255,255,0.8)" }}>Online</div>
                </div>
              </>
            )}
            {channelMode === "sms" && (
              <>
                <div style={{ fontSize: "1.5em" }}></div>
                <div style={styles.headerText}>Sarah (ProVision)</div>
              </>
            )}
            {channelMode === "web" && styles.headerText}
          </div>
          
          {/* Messages */}
          <div
            style={{
              height: channelMode === "web" ? "480px" : (channelMode === "facebook" || channelMode === "instagram") ? "430px" : "450px",
              overflowY: "auto",
              marginBottom: "20px",
              padding: (channelMode === "facebook" || channelMode === "instagram") ? "16px" : "0",
              position: "relative",
              zIndex: 1,
              display: "flex",
              flexDirection: "column",
              gap: 8
            }}
          >
            {messages.map((message, index) => (
              <div
                key={index}
                style={message.role === "user" ? styles.userBubble : styles.agentBubble}
              >
                {channelMode === "web" && message.role !== "user" && (
                  <div
                    style={{
                      fontSize: "0.76em",
                      fontWeight: 600,
                      color: "#717C99",
                      marginBottom: 6,
                      textTransform: "uppercase",
                      letterSpacing: "0.08em"
                    }}
                  >
                    {message.sender}
                  </div>
                )}
                <div style={{ lineHeight: 1.5, fontSize: "0.95em" }}>{message.text}</div>
                {channelMode !== "web" && (
                  <div style={{ fontSize: "0.7em", color: "rgba(0,0,0,0.4)", marginTop: 4, textAlign: "right" }}>
                    {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div style={styles.agentBubble}>
                <div style={{ display: "flex", gap: 4 }}>
                  <div style={{ width: 8, height: 8, background: "#8D97AF", borderRadius: "50%", animation: "pulse 1.4s infinite" }}></div>
                  <div style={{ width: 8, height: 8, background: "#8D97AF", borderRadius: "50%", animation: "pulse 1.4s infinite 0.2s" }}></div>
                  <div style={{ width: 8, height: 8, background: "#8D97AF", borderRadius: "50%", animation: "pulse 1.4s infinite 0.4s" }}></div>
                </div>
              </div>
            )}
          </div>
          
          {/* Input */}
          <div
            style={{
              display: "flex",
              gap: 8,
              alignItems: "center",
              padding: (channelMode === "facebook" || channelMode === "instagram") ? "16px" : "0",
              background: (channelMode === "facebook" || channelMode === "instagram") ? "#fff" : "transparent",
              borderTop: (channelMode === "facebook" || channelMode === "instagram") ? "1px solid #dbdbdb" : "none",
              position: "relative",
              zIndex: 1
            }}
          >
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={channelMode === "instagram" ? "Message..." : (channelMode === "facebook" ? "Aa" : (channelMode === "sms" ? "Text message" : (channelMode === "whatsapp" ? "Type a message" : "Ask me anything...")))}
              style={styles.inputStyle}
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              style={{
                background: inputMessage.trim() && !isLoading ? (channelMode === "neuralapps" ? "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)" : (channelMode === "instagram" ? "#3797f0" : (channelMode === "facebook" ? "#0084ff" : (channelMode === "whatsapp" ? "#25D366" : (channelMode === "sms" ? "#007AFF" : GOLD))))) : "#e0e0e0",
                color: inputMessage.trim() && !isLoading ? "#fff" : "#999",
                border: "none",
                borderRadius: 20,
                padding: "8px 16px",
                fontSize: "0.9em",
                fontWeight: 600,
                cursor: inputMessage.trim() && !isLoading ? "pointer" : "not-allowed",
                transition: "all 0.2s ease"
              }}
            >
              {channelMode === "sms" || channelMode === "whatsapp" ? "" : (isLoading ? "..." : "Send")}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    {/* Channel Toggle (only show if prop is true) */}
    {showChannelToggle && (
      <div
        style={{
          marginTop: 16,
          background: "#ffffff",
          borderRadius: 16,
          padding: "16px",
          boxShadow: "0 4px 12px rgba(20, 40, 87, 0.08)"
        }}
      >
        <div style={{ fontSize: "0.85em", color: SLATE, fontWeight: 600, marginBottom: 12, textAlign: "center" }}>
           Switch Communication Channel
        </div>
        <div style={{ display: "flex", gap: 12 }}>
          <button
            onClick={() => {
              console.log("SMS clicked");
              setChannelMode("sms");
            }}
            onMouseOver={(e) => {
              if (channelMode !== "sms") {
                e.currentTarget.style.background = "#e3f2fd";
                e.currentTarget.style.transform = "scale(1.02)";
              }
            }}
            onMouseOut={(e) => {
              if (channelMode !== "sms") {
                e.currentTarget.style.background = "#f0f0f0";
                e.currentTarget.style.transform = "scale(1)";
              }
            }}
            style={{
              flex: 1,
              padding: "12px 20px",
              background: channelMode === "sms" ? "#007AFF" : "#f0f0f0",
              color: channelMode === "sms" ? "#fff" : SLATE,
              border: "none",
              borderRadius: 10,
              fontSize: "0.9em",
              fontWeight: 600,
              cursor: "pointer",
              transition: "all 0.3s ease"
            }}
          >
             SMS
          </button>
          <button
            onClick={() => {
              console.log("WhatsApp clicked");
              setChannelMode("whatsapp");
            }}
            onMouseOver={(e) => {
              if (channelMode !== "whatsapp") {
                e.currentTarget.style.background = "#e8f5e9";
                e.currentTarget.style.transform = "scale(1.02)";
              }
            }}
            onMouseOut={(e) => {
              if (channelMode !== "whatsapp") {
                e.currentTarget.style.background = "#f0f0f0";
                e.currentTarget.style.transform = "scale(1)";
              }
            }}
            style={{
              flex: 1,
              padding: "12px 20px",
              background: channelMode === "whatsapp" ? "#25D366" : "#f0f0f0",
              color: channelMode === "whatsapp" ? "#fff" : SLATE,
              border: "none",
              borderRadius: 10,
              fontSize: "0.9em",
              fontWeight: 600,
              cursor: "pointer",
              transition: "all 0.3s ease",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 6
            }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" fill={channelMode === "whatsapp" ? "#fff" : "#25D366"}/>
            </svg>
            WhatsApp
          </button>
        </div>
      </div>
    )}
    </>
  );
}

function Hero() {
  return (
    <section style={{ background: "#ffffff" }}>
      <div
        style={{
          maxWidth: 1280,
          margin: "0 auto",
          padding: "48px 40px 40px",
          display: "flex",
          alignItems: "flex-start",
          justifyContent: "space-between",
          gap: 48,
          flexWrap: "wrap"
        }}
      >
        <div
          style={{
            flex: "1 1 520px",
            maxWidth: 560,
            display: "flex",
            flexDirection: "column",
            gap: 22
          }}
        >
          <div>
            <h1
              style={{
                fontSize: "3.6em",
                lineHeight: 1.1,
                margin: 0,
                color: NAVY,
                letterSpacing: "-0.015em"
              }}
            >
              Unlock Your Financial Future with Confidence.
            </h1>
            <p
              style={{
                marginTop: 16,
                fontSize: "1.16em",
                color: SLATE,
                lineHeight: 1.65
              }}
            >
              Secure all the ProVisions you need to experience real successpowered by AI-guided expertise, trusted advisors, and effortless engagement every step of your journey.
            </p>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
              gap: 16
            }}
          >
            {[
              "Intelligent, Personalized Advice",
              "Book Seminars and Appointments Instantly",
              "Multi-Channel Reminders (SMS, WhatsApp, Web)",
              "Compliant, Secure, and Always On",
              "Seamless Client SupportEverywhere You Are"
            ].map((bullet) => (
              <div
                key={bullet}
                style={{
                  display: "flex",
                  alignItems: "flex-start",
                  gap: 12
                }}
              >
                <span
                  style={{
                    width: 10,
                    height: 10,
                    borderRadius: "50%",
                    background: GOLD,
                    marginTop: 6,
                    flexShrink: 0
                  }}
                />
                <span
                  style={{
                    color: SLATE,
                    fontSize: "0.98em",
                    lineHeight: 1.6,
                    fontWeight: 500
                  }}
                >
                  {bullet}
                </span>
              </div>
            ))}
          </div>

          <div
            style={{
              marginTop: 4,
              fontSize: "0.96em",
              color: "#5A6483",
              lineHeight: 1.6,
              maxWidth: 520
            }}
          >
            Join the next generation of clients achieving more, faster, with ProVision's blend of experience and innovation. Your peace of minddelivered.
          </div>
        </div>

        <div
          style={{
            flex: "0 1 360px",
            display: "flex",
            justifyContent: "flex-end",
            marginLeft: "auto"
          }}
        >
          <DeviceMock />
        </div>
      </div>
    </section>
  );
}

function SeminarRegistrationPage() {
  return (
    <section style={{ background: "#ffffff" }}>
      <div
        style={{
          maxWidth: 1280,
          margin: "0 auto",
          padding: "48px 40px 64px",
          display: "flex",
          gap: 56,
          alignItems: "flex-start",
          flexWrap: "wrap"
        }}
      >
        <div
          style={{
            flex: "1 1 520px",
            maxWidth: 600
          }}
        >
          <h2
            style={{
              fontSize: "2.6em",
              marginBottom: 16,
              color: NAVY,
              letterSpacing: "-0.01em"
            }}
          >
            Seminar Registration
          </h2>
          <p
            style={{
              fontSize: "1.08em",
              lineHeight: 1.7,
              color: SLATE,
              marginBottom: 22
            }}
          >
            Launch high-converting landing pages and automate every RSVP from the moment a guest discovers your seminar. Branded forms, instant confirmations, and advisor routing are built to keep your pipeline full.
          </p>
          <ul
            style={{
              margin: 0,
              paddingLeft: 22,
              lineHeight: 1.7,
              color: SLATE,
              fontSize: "1.02em"
            }}
          >
            <li>Responsive registration flows with compliance-ready disclosures</li>
            <li>Payment and ticketing options for premium or hybrid events</li>
            <li>Automatic calendar invites and nurture reminders</li>
            <li>Built-in segmentation to prioritize high-value prospects</li>
          </ul>
        </div>
        <div
          style={{
            flex: "1 1 320px",
            minWidth: 280,
            background: CLOUD,
            borderRadius: 24,
            border: `1px solid ${BORDER}`,
            padding: "28px 30px",
            color: SLATE,
            boxShadow: "0 18px 30px rgba(20, 40, 87, 0.08)"
          }}
        >
          <div
            style={{
              fontWeight: 700,
              color: NAVY,
              marginBottom: 12
            }}
          >
            Launch Checklist
          </div>
          <ol
            style={{
              paddingLeft: 20,
              margin: "0 0 18px 0",
              lineHeight: 1.6
            }}
          >
            <li>Pick your audience segment and registration template</li>
            <li>Configure reminders across SMS, WhatsApp, and email</li>
            <li>Publish the campaign in under five minutes</li>
            <li>Monitor real-time registrations and VIP alerts</li>
          </ol>
          <div style={{ fontSize: "0.96em", lineHeight: 1.6 }}>
            Need inspiration? Import last quarter's top-performing funnel and personalize messaging with one click.
          </div>
        </div>
      </div>
    </section>
  );
}

function SeminarAttendancePage() {
  return (
    <section style={{ background: "#ffffff" }}>
      <div
        style={{
          maxWidth: 1280,
          margin: "0 auto",
          padding: "48px 40px 64px",
          display: "flex",
          gap: 56,
          alignItems: "flex-start",
          flexWrap: "wrap"
        }}
      >
        <div
          style={{
            flex: "1 1 520px",
            maxWidth: 600
          }}
        >
          <h2
            style={{
              fontSize: "2.6em",
              marginBottom: 16,
              color: NAVY,
              letterSpacing: "-0.01em"
            }}
          >
            Seminar Attendance
          </h2>
          <p
            style={{
              fontSize: "1.08em",
              lineHeight: 1.7,
              color: SLATE,
              marginBottom: 22
            }}
          >
            Track arrivals, engagement, and audience sentiment in real time. Our attendance dashboard keeps advisors informed while your AI concierge handles check-ins and live support.
          </p>
          <ul
            style={{
              margin: 0,
              paddingLeft: 22,
              lineHeight: 1.7,
              color: SLATE,
              fontSize: "1.02em"
            }}
          >
            <li>Instant check-in via QR code or concierge confirmation</li>
            <li>Live attendee heatmaps to surface high-intent prospects</li>
            <li>Feedback surveys crafted for compliance and insights</li>
            <li>Post-session summaries automatically routed to advisors</li>
          </ul>
        </div>
        <div
          style={{
            flex: "1 1 320px",
            minWidth: 280,
            background: "#ffffff",
            borderRadius: 24,
            border: `1px solid ${BORDER}`,
            padding: "28px 30px",
            color: SLATE,
            boxShadow: "0 18px 30px rgba(20, 40, 87, 0.08)"
          }}
        >
          <div
            style={{
              fontWeight: 700,
              color: NAVY,
              marginBottom: 12
            }}
          >
            Metrics Dashboard
          </div>
          <div style={{ display: "flex", gap: 24, marginBottom: 16 }}>
            <div>
              <div style={{ fontSize: "2.1em", fontWeight: 700, color: NAVY }}>92%</div>
              <div style={{ fontSize: "0.9em" }}>Show Rate</div>
            </div>
            <div>
              <div style={{ fontSize: "2.1em", fontWeight: 700, color: NAVY }}>47%</div>
              <div style={{ fontSize: "0.9em" }}>Live Interactions</div>
            </div>
          </div>
          <div style={{ fontSize: "0.96em", lineHeight: 1.6 }}>
            Export attendance data straight into your CRM or marketing automation tools. Trigger follow-up cadences in seconds without leaving the dashboard.
          </div>
        </div>
      </div>
    </section>
  );
}

function AppointmentConversionPage() {
  return (
    <section style={{ background: "#ffffff" }}>
      <div
        style={{
          maxWidth: 1280,
          margin: "0 auto",
          padding: "48px 40px 64px",
          display: "flex",
          gap: 56,
          alignItems: "flex-start",
          flexWrap: "wrap"
        }}
      >
        <div
          style={{
            flex: "1 1 520px",
            maxWidth: 600
          }}
        >
          <h2
            style={{
              fontSize: "2.6em",
              marginBottom: 16,
              color: NAVY,
              letterSpacing: "-0.01em"
            }}
          >
            Appointment Conversion
          </h2>
          <p
            style={{
              fontSize: "1.08em",
              lineHeight: 1.7,
              color: SLATE,
              marginBottom: 22
            }}
          >
            Convert attendees into loyal clients with coordinated advisor follow-up, qualification scoring, and scheduling automation that never sleeps.
          </p>
          <ul
            style={{
              margin: 0,
              paddingLeft: 22,
              lineHeight: 1.7,
              color: SLATE,
              fontSize: "1.02em"
            }}
          >
            <li>AI-prioritized callbacks based on event engagement signals</li>
            <li>Instant booking links tied to advisor calendars and routing rules</li>
            <li>Warm handoff scripts and compliance notes in one workspace</li>
            <li>Pipeline reporting to track conversion rates and revenue impact</li>
          </ul>
        </div>
        <div
          style={{
            flex: "1 1 320px",
            minWidth: 280,
            background: CLOUD,
            borderRadius: 24,
            border: `1px solid ${BORDER}`,
            padding: "28px 30px",
            color: SLATE,
            boxShadow: "0 18px 30px rgba(20, 40, 87, 0.08)"
          }}
        >
          <div
            style={{
              fontWeight: 700,
              color: NAVY,
              marginBottom: 12
            }}
          >
            Conversion Playbook
          </div>
          <ol
            style={{
              paddingLeft: 20,
              margin: "0 0 18px 0",
              lineHeight: 1.6
            }}
          >
            <li>Send tailored recap and replay within one hour</li>
            <li>Deliver advisor introduction paired with self-booking link</li>
            <li>Automate two-touch reminder cadence for undecided prospects</li>
            <li>Capture outcomes and notes directly in CRM workflows</li>
          </ol>
          <div style={{ fontSize: "0.96em", lineHeight: 1.6 }}>
            Advisors stay focused on relationships while ProVision orchestrates every digital touchpoint to close the loop.
          </div>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer
      style={{
        background: "#ffffff",
        borderTop: `1px solid ${BORDER}`
      }}
    >
      <div
        style={{
          maxWidth: 1280,
          margin: "0 auto",
          padding: "22px 40px 28px",
          color: SLATE
        }}
      >
        <div
          style={{
            display: "flex",
            gap: 28,
            marginBottom: 12
          }}
        >
          <a
            href="https://provisionbrokerage.com/privacy-policy"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              textDecoration: "none",
              color: "inherit",
              fontWeight: 500,
              transition: "color 0.2s ease"
            }}
            onMouseOver={(e) => {
              e.target.style.color = GOLD;
            }}
            onMouseOut={(e) => {
              e.target.style.color = "inherit";
            }}
          >
            Privacy Policy
          </a>
          <a
            href="https://provisionbrokerage.com/terms-of-service"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              textDecoration: "none",
              color: "inherit",
              fontWeight: 500,
              transition: "color 0.2s ease"
            }}
            onMouseOver={(e) => {
              e.target.style.color = GOLD;
            }}
            onMouseOut={(e) => {
              e.target.style.color = "inherit";
            }}
          >
            Terms of Service
          </a>
          <a
            href="https://provisionbrokerage.com/compliance"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              textDecoration: "none",
              color: "inherit",
              fontWeight: 500,
              transition: "color 0.2s ease"
            }}
            onMouseOver={(e) => {
              e.target.style.color = GOLD;
            }}
            onMouseOut={(e) => {
              e.target.style.color = "inherit";
            }}
          >
            Compliance
          </a>
        </div>
        <div
          style={{
            fontSize: "0.94em",
            lineHeight: 1.6
          }}
        >
           2023 ProVision Brokerage. All rights reserved. | 123 Finance St. Moneyville, USA | (123) 456-7890 | contact@provision.com
        </div>
      </div>
    </footer>
  );
}

function ChatbotPage() {
  const [messages, setMessages] = useState([
    {
      role: "agent",
      sender: "Sarah - ProVision Brokerage",
      text: "Hi! I'm Sarah from ProVision Brokerage. I'm here to help you with retirement planning, annuities, and booking consultations with our advisors. What's on your mind today?",
      timestamp: new Date().toISOString()
    }
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      role: "user",
      sender: "You",
      text: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage("");
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          session_id: sessionId,
          channel: "web",
          context: {
            page: "home"
          }
        })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      const agentMessage = {
        role: "agent",
        sender: "AI Agent",
        text: data.message,
        timestamp: new Date().toISOString(),
        sources: data.knowledge_sources || []
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: "agent",
        sender: "AI Agent",
        text: "I apologize, but I'm experiencing technical difficulties. Please try again or contact our support team.",
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <section style={{ background: "#ffffff", minHeight: "80vh" }}>
      <div
        style={{
          maxWidth: 1280,
          margin: "0 auto",
          padding: "48px 40px 64px",
          display: "flex",
          gap: 40,
          alignItems: "flex-start",
          flexWrap: "wrap"
        }}
      >
        <div
          style={{
            flex: "1 1 600px",
            maxWidth: 700,
            background: "#ffffff",
            borderRadius: 24,
            border: `1px solid ${BORDER}`,
            boxShadow: "0 18px 30px rgba(20, 40, 87, 0.08)",
            overflow: "hidden"
          }}
        >
          <div
            style={{
              background: NAVY,
              color: "#ffffff",
              padding: "24px 30px",
              textAlign: "center"
            }}
          >
            <h2
              style={{
                fontSize: "1.8em",
                margin: 0,
                fontWeight: 700,
                letterSpacing: "-0.01em"
              }}
            >
              AI Financial Assistant
            </h2>
            <p
              style={{
                margin: "8px 0 0 0",
                fontSize: "1em",
                opacity: 0.9
              }}
            >
              Powered by ProVision Brokerage Knowledge Base
            </p>
          </div>
          
          <div
            style={{
              height: "500px",
              overflowY: "auto",
              padding: "24px 30px",
              background: "#ffffff"
            }}
          >
            {messages.map((message, index) => (
              <div key={index}>
                <ChatMessage {...message} />
                {message.sources && message.sources.length > 0 && (
                  <div
                    style={{
                      fontSize: "0.8em",
                      color: "#8D97AF",
                      marginTop: "-10px",
                      marginBottom: "20px",
                      paddingLeft: "48px"
                    }}
                  >
                    Sources: {message.sources.slice(0, 2).join(", ")}
                    {message.sources.length > 2 && ` +${message.sources.length - 2} more`}
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                  marginBottom: 20
                }}
              >
                <div
                  style={{
                    width: 36,
                    height: 36,
                    borderRadius: "50%",
                    background: "#f0f0f0",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center"
                  }}
                >
                  
                </div>
                <div
                  style={{
                    background: CLOUD,
                    padding: "14px 16px",
                    borderRadius: "18px 18px 18px 4px",
                    fontSize: "0.96em",
                    color: SLATE
                  }}
                >
                  <div style={{ display: "flex", gap: 4 }}>
                    <div style={{ width: 8, height: 8, background: "#8D97AF", borderRadius: "50%", animation: "pulse 1.4s infinite" }}></div>
                    <div style={{ width: 8, height: 8, background: "#8D97AF", borderRadius: "50%", animation: "pulse 1.4s infinite 0.2s" }}></div>
                    <div style={{ width: 8, height: 8, background: "#8D97AF", borderRadius: "50%", animation: "pulse 1.4s infinite 0.4s" }}></div>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          <div
            style={{
              padding: "20px 30px",
              borderTop: `1px solid ${BORDER}`,
              background: "#fafbfc"
            }}
          >
            <div
              style={{
                display: "flex",
                gap: 12,
                alignItems: "flex-end"
              }}
            >
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me about retirement planning, annuities, or book a consultation..."
                style={{
                  flex: 1,
                  minHeight: "44px",
                  maxHeight: "120px",
                  padding: "12px 16px",
                  border: `1px solid ${BORDER}`,
                  borderRadius: 22,
                  fontSize: "0.96em",
                  fontFamily: "inherit",
                  resize: "none",
                  outline: "none",
                  background: "#ffffff"
                }}
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={!inputMessage.trim() || isLoading}
                style={{
                  background: inputMessage.trim() && !isLoading ? GOLD : "#e0e0e0",
                  color: inputMessage.trim() && !isLoading ? NAVY : "#999",
                  border: "none",
                  borderRadius: 22,
                  padding: "12px 24px",
                  fontSize: "0.96em",
                  fontWeight: 600,
                  cursor: inputMessage.trim() && !isLoading ? "pointer" : "not-allowed",
                  transition: "all 0.2s ease",
                  minWidth: "80px"
                }}
              >
                {isLoading ? "..." : "Send"}
              </button>
            </div>
          </div>
        </div>

        <div
          style={{
            flex: "1 1 300px",
            minWidth: 280,
            background: CLOUD,
            borderRadius: 24,
            border: `1px solid ${BORDER}`,
            padding: "28px 30px",
            color: SLATE,
            boxShadow: "0 18px 30px rgba(20, 40, 87, 0.08)"
          }}
        >
          <div
            style={{
              fontWeight: 700,
              color: NAVY,
              marginBottom: 16,
              fontSize: "1.2em"
            }}
          >
             Try asking about:
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {[
              "What are the different types of annuities?",
              "How do fixed annuities work?",
              "What are the tax benefits of annuities?",
              "How do I choose the right annuity?",
              "What are annuity surrender charges?",
              "How do annuities provide guaranteed income?"
            ].map((suggestion, index) => (
              <button
                key={index}
                onClick={() => setInputMessage(suggestion)}
                style={{
                  background: "#ffffff",
                  border: `1px solid ${BORDER}`,
                  borderRadius: 12,
                  padding: "12px 16px",
                  textAlign: "left",
                  color: SLATE,
                  fontSize: "0.9em",
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                  lineHeight: 1.4
                }}
                onMouseOver={(e) => {
                  e.target.style.background = GOLD;
                  e.target.style.color = NAVY;
                }}
                onMouseOut={(e) => {
                  e.target.style.background = "#ffffff";
                  e.target.style.color = SLATE;
                }}
              >
                {suggestion}
              </button>
            ))}
          </div>
          
          <div
            style={{
              marginTop: 24,
              padding: "16px",
              background: "#ffffff",
              borderRadius: 12,
              border: `1px solid ${BORDER}`,
              fontSize: "0.85em",
              lineHeight: 1.5
            }}
          >
            <div style={{ fontWeight: 600, color: NAVY, marginBottom: 8 }}>
               Compliance Notice
            </div>
            <div style={{ color: "#666" }}>
              This AI assistant provides educational information only and does not offer investment advice. All responses are sourced from our knowledge base.
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

// Coming Soon Page Components
function SeminarsPage() {
  const [seminars, setSeminars] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [selectedSeminar, setSelectedSeminar] = React.useState(null);
  const [showRegistrationForm, setShowRegistrationForm] = React.useState(false);
  const [registrationSuccess, setRegistrationSuccess] = React.useState(false);
  const [formData, setFormData] = React.useState({
    name: '',
    email: '',
    phone: ''
  });

  // Fetch seminars from backend
  React.useEffect(() => {
    fetch(`${API_BASE_URL}/api/seminars/upcoming`)
      .then(res => res.json())
      .then(data => {
        setSeminars(data.seminars || []);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching seminars:', err);
        setLoading(false);
      });
  }, []);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    });
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric',
      minute: '2-digit'
    });
  };

  const handleRegisterClick = (seminar) => {
    setSelectedSeminar(seminar);
    setShowRegistrationForm(true);
    setRegistrationSuccess(false);
    setFormData({ name: '', email: '', phone: '' });
  };

  const handleSubmitRegistration = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/seminars/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          seminar_id: selectedSeminar.id,
          guest_name: formData.name,
          guest_email: formData.email,
          guest_phone: formData.phone,
          reminder_preference: 'email'
        })
      });

      if (response.ok) {
        setRegistrationSuccess(true);
        // Refresh seminars list to update registration count
        const updatedSeminars = await fetch(`${API_BASE_URL}/api/seminars/upcoming`).then(r => r.json());
        setSeminars(updatedSeminars.seminars || []);
        
        // Close form after 2 seconds
        setTimeout(() => {
          setShowRegistrationForm(false);
          setSelectedSeminar(null);
        }, 2500);
      } else {
        const errorData = await response.json();
        alert('Registration failed: ' + (errorData.detail || 'Please try again.'));
      }
    } catch (error) {
      console.error('Error registering:', error);
      alert('Registration failed. Please try again.');
    }
  };

  return (
    <div style={{ display: "flex", minHeight: "calc(100vh - 200px)", position: "relative" }}>
      {/* Left Side - Seminars List */}
      <div style={{ flex: 1, padding: "40px", background: "#f8fafc", overflowY: "auto", maxHeight: "calc(100vh - 200px)" }}>
        <div style={{ maxWidth: "800px", margin: "0 auto" }}>
          <h1 style={{ fontSize: "2.5em", color: NAVY, marginBottom: 12, fontWeight: 700 }}>
            Upcoming Seminars
          </h1>
          <p style={{ fontSize: "1.1em", color: SLATE, marginBottom: 40, lineHeight: 1.6 }}>
            Join our educational seminars on retirement planning, annuities, and financial security
          </p>
          
          {loading ? (
            <div style={{ textAlign: "center", padding: "60px", color: SLATE }}>
              <div style={{ fontSize: "2em", marginBottom: 12 }}></div>
              <div>Loading seminars...</div>
            </div>
          ) : seminars.length === 0 ? (
            <div style={{ textAlign: "center", padding: "60px", color: SLATE, background: "#ffffff", borderRadius: 16 }}>
              <div style={{ fontSize: "3em", marginBottom: 12 }}></div>
              <div style={{ fontSize: "1.2em", fontWeight: 600, marginBottom: 8 }}>No upcoming seminars</div>
              <div style={{ fontSize: "0.95em" }}>Check back soon or ask Sarah about future events!</div>
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              {seminars.map((seminar) => {
                const availableSeats = seminar.capacity - seminar.registered_count;
                const isAlmostFull = availableSeats <= 5 && availableSeats > 0;
                const isFull = availableSeats <= 0;
                
                return (
                  <div
                    key={seminar.id}
                    style={{
                      background: "#ffffff",
                      border: `2px solid ${isFull ? '#ef4444' : (isAlmostFull ? '#f59e0b' : '#e5e7eb')}`,
                      borderRadius: 16,
                      padding: "24px",
                      transition: "all 0.3s ease",
                      opacity: isFull ? 0.8 : 1,
                      cursor: "pointer"
                    }}
                    onClick={() => !isFull && handleRegisterClick(seminar)}
                    onMouseOver={(e) => {
                      if (!isFull) {
                        e.currentTarget.style.boxShadow = "0 8px 24px rgba(20, 40, 87, 0.15)";
                        e.currentTarget.style.transform = "translateY(-2px)";
                      }
                    }}
                    onMouseOut={(e) => {
                      e.currentTarget.style.boxShadow = "none";
                      e.currentTarget.style.transform = "translateY(0)";
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
                      <h3 style={{ fontSize: "1.4em", color: NAVY, margin: 0, flex: 1, lineHeight: 1.3, fontWeight: 700 }}>
                        {seminar.title}
                      </h3>
                      <div
                        style={{
                          background: isFull ? '#ef4444' : (isAlmostFull ? '#f59e0b' : '#10b981'),
                          color: "#ffffff",
                          padding: "6px 14px",
                          borderRadius: 12,
                          fontSize: "0.75em",
                          fontWeight: 700,
                          marginLeft: 16,
                          whiteSpace: "nowrap"
                        }}
                      >
                        {isFull ? ' FULL' : (isAlmostFull ? ` ${availableSeats} LEFT` : ` ${availableSeats} SEATS`)}
                      </div>
                    </div>
                    
                    <p style={{ color: SLATE, fontSize: "0.95em", lineHeight: 1.6, margin: "12px 0 16px 0" }}>
                      {seminar.description}
                    </p>
                    
                    <div style={{ display: "flex", gap: 24, flexWrap: "wrap", marginBottom: 16 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: "0.9em", color: SLATE }}>
                        <span style={{ fontSize: "1.2em" }}></span>
                        <div>
                          <div style={{ fontWeight: 600, color: NAVY }}>{formatDate(seminar.date)}</div>
                          <div style={{ fontSize: "0.85em", color: "#64748b" }}>{formatTime(seminar.date)}</div>
                        </div>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: "0.9em", color: SLATE }}>
                        <span style={{ fontSize: "1.2em" }}></span>
                        <div>
                          <div style={{ fontWeight: 600, color: NAVY }}>{seminar.duration} mins</div>
                        </div>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: "0.9em", color: SLATE }}>
                        <span style={{ fontSize: "1.2em" }}></span>
                        <div>
                          <div style={{ fontWeight: 600, color: NAVY, textTransform: "capitalize" }}>{seminar.location_type}</div>
                        </div>
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: "0.9em", color: SLATE }}>
                        <span style={{ fontSize: "1.2em" }}></span>
                        <div>
                          <div style={{ fontWeight: 600, color: NAVY }}>{seminar.registered_count}/{seminar.capacity}</div>
                        </div>
                      </div>
                    </div>
                    
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        if (!isFull) handleRegisterClick(seminar);
                      }}
                      disabled={isFull}
                      style={{
                        width: "100%",
                        padding: "14px 24px",
                        background: isFull ? '#9ca3af' : NAVY,
                        color: "#ffffff",
                        border: "none",
                        borderRadius: 10,
                        fontSize: "1em",
                        fontWeight: 700,
                        cursor: isFull ? "not-allowed" : "pointer",
                        transition: "all 0.3s ease"
                      }}
                      onMouseOver={(e) => {
                        if (!isFull) {
                          e.target.style.background = GOLD;
                        }
                      }}
                      onMouseOut={(e) => {
                        if (!isFull) {
                          e.target.style.background = NAVY;
                        }
                      }}
                    >
                      {isFull ? ' Seminar Full' : ' Click to Register'}
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
      
      {/* Right Side - Chat Widget */}
      <div style={{ width: "420px", padding: "20px", background: "#e2e8f0" }}>
        <DeviceMock 
          pageContext="seminars"
          initialMessage="Hi! I'm Sarah from ProVision Brokerage. I can help you find and register for our upcoming seminars. Check out the list on the left, or tell me what topics interest you most!"
          showChannelToggle={true}
        />
      </div>
      
      {/* Registration Form Modal */}
      {showRegistrationForm && selectedSeminar && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: "rgba(0, 0, 0, 0.6)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
            backdropFilter: "blur(4px)"
          }}
          onClick={() => setShowRegistrationForm(false)}
        >
          <div
            style={{
              background: "#ffffff",
              borderRadius: 24,
              padding: "40px",
              maxWidth: "500px",
              width: "90%",
              boxShadow: "0 30px 60px rgba(20, 40, 87, 0.3)",
              position: "relative"
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setShowRegistrationForm(false)}
              style={{
                position: "absolute",
                top: "16px",
                right: "16px",
                background: "transparent",
                border: "none",
                fontSize: "1.5em",
                cursor: "pointer",
                color: SLATE,
                padding: "8px",
                lineHeight: 1
              }}
            >
              
            </button>
            
            {registrationSuccess ? (
              <div style={{ textAlign: "center", padding: "40px 20px" }}>
                <div style={{ fontSize: "4em", marginBottom: 20 }}></div>
                <h2 style={{ color: NAVY, fontSize: "1.8em", marginBottom: 12 }}>
                  Registered Successfully!
                </h2>
                <p style={{ color: SLATE, fontSize: "1.1em", lineHeight: 1.6 }}>
                  You're all set for <strong>{selectedSeminar.title}</strong>!
                  <br />
                  Check your email for confirmation and details.
                </p>
              </div>
            ) : (
              <>
                <h2 style={{ color: NAVY, fontSize: "1.8em", marginBottom: 8, fontWeight: 700 }}>
                  Register for Seminar
                </h2>
                <p style={{ color: SLATE, marginBottom: 24, fontSize: "0.95em" }}>
                  {selectedSeminar.title}
                </p>
                
                <form onSubmit={handleSubmitRegistration}>
                  <div style={{ marginBottom: 20 }}>
                    <label style={{ display: "block", color: NAVY, fontWeight: 600, marginBottom: 8, fontSize: "0.9em" }}>
                      Full Name *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      placeholder="John Doe"
                      style={{
                        width: "100%",
                        padding: "12px 16px",
                        border: `2px solid ${BORDER}`,
                        borderRadius: 10,
                        fontSize: "1em",
                        outline: "none",
                        transition: "border-color 0.3s"
                      }}
                      onFocus={(e) => e.target.style.borderColor = GOLD}
                      onBlur={(e) => e.target.style.borderColor = BORDER}
                    />
                  </div>
                  
                  <div style={{ marginBottom: 20 }}>
                    <label style={{ display: "block", color: NAVY, fontWeight: 600, marginBottom: 8, fontSize: "0.9em" }}>
                      Email Address *
                    </label>
                    <input
                      type="email"
                      required
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                      placeholder="john@example.com"
                      style={{
                        width: "100%",
                        padding: "12px 16px",
                        border: `2px solid ${BORDER}`,
                        borderRadius: 10,
                        fontSize: "1em",
                        outline: "none",
                        transition: "border-color 0.3s"
                      }}
                      onFocus={(e) => e.target.style.borderColor = GOLD}
                      onBlur={(e) => e.target.style.borderColor = BORDER}
                    />
                  </div>
                  
                  <div style={{ marginBottom: 28 }}>
                    <label style={{ display: "block", color: NAVY, fontWeight: 600, marginBottom: 8, fontSize: "0.9em" }}>
                      Phone Number *
                    </label>
                    <input
                      type="tel"
                      required
                      value={formData.phone}
                      onChange={(e) => setFormData({...formData, phone: e.target.value})}
                      placeholder="+1 (555) 123-4567"
                      style={{
                        width: "100%",
                        padding: "12px 16px",
                        border: `2px solid ${BORDER}`,
                        borderRadius: 10,
                        fontSize: "1em",
                        outline: "none",
                        transition: "border-color 0.3s"
                      }}
                      onFocus={(e) => e.target.style.borderColor = GOLD}
                      onBlur={(e) => e.target.style.borderColor = BORDER}
                    />
                  </div>
                  
                  <button
                    type="submit"
                    style={{
                      width: "100%",
                      padding: "16px 24px",
                      background: NAVY,
                      color: "#ffffff",
                      border: "none",
                      borderRadius: 12,
                      fontSize: "1.1em",
                      fontWeight: 700,
                      cursor: "pointer",
                      transition: "all 0.3s ease"
                    }}
                    onMouseOver={(e) => e.target.style.background = GOLD}
                    onMouseOut={(e) => e.target.style.background = NAVY}
                  >
                    Complete Registration
                  </button>
                </form>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function AppointmentsPage() {
  return (
    <div style={{ display: "flex", minHeight: "calc(100vh - 200px)" }}>
      {/* Left Side - Feature Content */}
      <div style={{ flex: 1, padding: "40px", background: "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)" }}>
        <div
          style={{
            background: "#ffffff",
            borderRadius: 20,
            padding: "40px",
            boxShadow: "0 20px 40px rgba(20, 40, 87, 0.1)",
            height: "fit-content"
          }}
        >
          <h1 style={{ fontSize: "2.5em", color: NAVY, marginBottom: 12, fontWeight: 700 }}>
            Schedule Your Consultation
          </h1>
          <p style={{ fontSize: "1.1em", color: SLATE, marginBottom: 40, lineHeight: 1.6 }}>
            Book a free consultation with our licensed financial advisors. Choose the appointment type that fits your needs.
          </p>
          
          <div style={{ marginTop: 30, padding: "24px", background: CLOUD, borderRadius: 12, border: `1px solid ${BORDER}` }}>
            <h4 style={{ color: NAVY, marginBottom: 16, fontSize: "1.2em", fontWeight: 700 }}> Book Your Free Consultation</h4>
            <p style={{ color: SLATE, fontSize: "0.95em", marginBottom: 20, lineHeight: 1.6 }}>
              Choose the type of consultation that best fits your needs:
            </p>
            
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {/* Free Initial Consultation */}
              <a
                href="https://cal.com/nishanthreddy-p-h96wap/free-initial-consultation-provision"
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: "block",
                  padding: "16px 20px",
                  background: NAVY,
                  color: "#ffffff",
                  borderRadius: 10,
                  textDecoration: "none",
                  transition: "all 0.3s ease",
                  border: `2px solid ${NAVY}`,
                  boxShadow: "0 4px 12px rgba(20, 40, 87, 0.15)"
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.background = GOLD;
                  e.currentTarget.style.borderColor = GOLD;
                  e.currentTarget.style.transform = "translateY(-2px)";
                  e.currentTarget.style.boxShadow = "0 6px 16px rgba(212, 175, 55, 0.3)";
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.background = NAVY;
                  e.currentTarget.style.borderColor = NAVY;
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow = "0 4px 12px rgba(20, 40, 87, 0.15)";
                }}
              >
                <div style={{ fontWeight: 700, fontSize: "1.05em", marginBottom: 4 }}>
                   Free Initial Consultation
                </div>
                <div style={{ fontSize: "0.9em", opacity: 0.95 }}>
                  Perfect for first-time discussions about retirement planning
                </div>
              </a>

              {/* Retirement Planning Consultation */}
              <a
                href="https://cal.com/nishanthreddy-p-h96wap/retirement-planning-consultation"
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: "block",
                  padding: "16px 20px",
                  background: NAVY,
                  color: "#ffffff",
                  borderRadius: 10,
                  textDecoration: "none",
                  transition: "all 0.3s ease",
                  border: `2px solid ${NAVY}`,
                  boxShadow: "0 4px 12px rgba(20, 40, 87, 0.15)"
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.background = GOLD;
                  e.currentTarget.style.borderColor = GOLD;
                  e.currentTarget.style.transform = "translateY(-2px)";
                  e.currentTarget.style.boxShadow = "0 6px 16px rgba(212, 175, 55, 0.3)";
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.background = NAVY;
                  e.currentTarget.style.borderColor = NAVY;
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow = "0 4px 12px rgba(20, 40, 87, 0.15)";
                }}
              >
                <div style={{ fontWeight: 700, fontSize: "1.05em", marginBottom: 4 }}>
                   Retirement Planning Consultation
                </div>
                <div style={{ fontSize: "0.9em", opacity: 0.95 }}>
                  In-depth analysis of your retirement strategy and goals
                </div>
              </a>

              {/* Annuity Product Consultation */}
              <a
                href="https://cal.com/nishanthreddy-p-h96wap/annuity-product-consultation"
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: "block",
                  padding: "16px 20px",
                  background: NAVY,
                  color: "#ffffff",
                  borderRadius: 10,
                  textDecoration: "none",
                  transition: "all 0.3s ease",
                  border: `2px solid ${NAVY}`,
                  boxShadow: "0 4px 12px rgba(20, 40, 87, 0.15)"
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.background = GOLD;
                  e.currentTarget.style.borderColor = GOLD;
                  e.currentTarget.style.transform = "translateY(-2px)";
                  e.currentTarget.style.boxShadow = "0 6px 16px rgba(212, 175, 55, 0.3)";
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.background = NAVY;
                  e.currentTarget.style.borderColor = NAVY;
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow = "0 4px 12px rgba(20, 40, 87, 0.15)";
                }}
              >
                <div style={{ fontWeight: 700, fontSize: "1.05em", marginBottom: 4 }}>
                   Annuity Product Consultation
                </div>
                <div style={{ fontSize: "0.9em", opacity: 0.95 }}>
                  Detailed review of annuity products and income strategies
                </div>
              </a>
            </div>
            
            <div style={{ marginTop: 20, padding: "12px", background: "#ffffff", borderRadius: 8, border: "1px solid #e2e8f0" }}>
              <div style={{ fontSize: "0.9em", color: SLATE, lineHeight: 1.5 }}>
                 <strong>Not sure which to choose?</strong> Ask Sarah in the chat, and she'll help you pick the right option!
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Right Side - Chat Widget */}
      <div style={{ width: "420px", padding: "20px", background: "#e2e8f0" }}>
        <DeviceMock 
          pageContext="appointments"
          initialMessage="Hi! I'm Sarah from ProVision Brokerage. I'd be happy to help you schedule a free consultation. You can click any booking option on the left, or tell me about your situation and I'll help you choose the right appointment type!"
          showChannelToggle={true}
        />
      </div>
    </div>
  );
}

function FacebookPage() {
  return (
    <div style={{ display: "flex", minHeight: "calc(100vh - 200px)" }}>
      {/* Left Side - Facebook Content */}
      <div style={{ flex: 1, padding: "40px", background: "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)" }}>
        <div
          style={{
            background: "#ffffff",
            borderRadius: 20,
            padding: "40px",
            boxShadow: "0 20px 40px rgba(20, 40, 87, 0.1)",
            height: "fit-content"
          }}
        >
          {/* Facebook Badge */}
          <div
            style={{
              background: "linear-gradient(135deg, #0084ff 0%, #0066cc 100%)",
              color: "#ffffff",
              padding: "12px 28px",
              borderRadius: 25,
              fontSize: "0.9em",
              fontWeight: 700,
              display: "inline-flex",
              alignItems: "center",
              gap: 10,
              marginBottom: 24,
              boxShadow: "0 4px 12px rgba(0, 132, 255, 0.3)"
            }}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
            <span>CONNECT ON FACEBOOK</span>
          </div>
          
          <h1 style={{ fontSize: "2.2em", color: NAVY, marginBottom: 16, fontWeight: 700 }}>
            Message Us on Facebook
          </h1>
          <p style={{ fontSize: "1.1em", color: SLATE, marginBottom: 30, lineHeight: 1.6 }}>
            Connect with ProVision Brokerage through Facebook Messenger for instant retirement planning assistance and personalized financial guidance.
          </p>
          
          {/* Facebook Stats */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 20, marginBottom: 30, padding: "20px", background: "linear-gradient(135deg, #f0f7ff 0%, #e6f2ff 100%)", borderRadius: 12 }}>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: "2em", fontWeight: 700, color: "#0084ff", marginBottom: 4 }}>2,500+</div>
              <div style={{ fontSize: "0.85em", color: SLATE }}>Followers</div>
            </div>
            <div style={{ textAlign: "center", borderLeft: "1px solid #d4e4f7", borderRight: "1px solid #d4e4f7" }}>
              <div style={{ fontSize: "2em", fontWeight: 700, color: "#0084ff", marginBottom: 4 }}>500+</div>
              <div style={{ fontSize: "0.85em", color: SLATE }}>Messages/Month</div>
            </div>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: "2em", fontWeight: 700, color: "#0084ff", marginBottom: 4 }}>4.9 Star</div>
              <div style={{ fontSize: "0.85em", color: SLATE }}>Rating</div>
            </div>
          </div>
          
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginTop: 30 }}>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Instant Messaging</h3>
              <ul style={{ color: SLATE, lineHeight: 1.8, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>Real-time responses via Messenger</li>
                <li>Quick retirement questions answered</li>
                <li>Share documents securely</li>
                <li>Schedule appointments instantly</li>
              </ul>
            </div>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Personalized Help</h3>
              <ul style={{ color: SLATE, lineHeight: 1.8, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>AI-powered lead qualification</li>
                <li>Retirement planning guidance</li>
                <li>Seminar registration via chat</li>
                <li>Connect with licensed advisors</li>
              </ul>
            </div>
          </div>
          
          {/* Facebook CTA */}
          <div style={{ marginTop: 30, padding: "24px", background: "linear-gradient(135deg, #0084ff 0%, #0066cc 100%)", borderRadius: 16, color: "#fff" }}>
            <h4 style={{ marginBottom: 12, fontSize: "1.2em", fontWeight: 700 }}>Find Us on Facebook</h4>
            <p style={{ marginBottom: 16, opacity: 0.95, lineHeight: 1.6 }}>
              Follow <strong>@ProVisionBrokerage</strong> for daily retirement tips, live Q&A sessions, and exclusive Facebook-only content!
            </p>
            <a
              href="https://www.facebook.com/profile.php?id=61571125691935"
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: "inline-block",
                background: "#fff",
                color: "#0084ff",
                border: "none",
                padding: "12px 24px",
                borderRadius: 25,
                fontWeight: 700,
                fontSize: "0.95em",
                cursor: "pointer",
                boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
                textDecoration: "none",
                transition: "all 0.3s ease"
              }}
              onMouseOver={(e) => {
                e.target.style.transform = "scale(1.05)";
                e.target.style.boxShadow = "0 6px 16px rgba(0, 0, 0, 0.2)";
              }}
              onMouseOut={(e) => {
                e.target.style.transform = "scale(1)";
                e.target.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.15)";
              }}
            >
              Visit Our Facebook Page
            </a>
          </div>
          
          <div style={{ marginTop: 30, padding: "20px", background: CLOUD, borderRadius: 12, border: `1px solid ${BORDER}` }}>
            <h4 style={{ color: NAVY, marginBottom: 12, fontSize: "1.1em" }}>Try the Facebook Messenger demo:</h4>
            <ul style={{ color: SLATE, lineHeight: 1.8, paddingLeft: 20, fontSize: "0.95em", margin: 0 }}>
              <li>"I saw your post about retirement planning"</li>
              <li>"Can you help me understand annuities?"</li>
              <li>"I want to schedule a consultation"</li>
              <li>"Tell me about your seminars"</li>
            </ul>
          </div>
        </div>
      </div>
      
      {/* Right Side - Facebook Messenger Widget */}
      <div style={{ width: "420px", padding: "20px", background: "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)" }}>
        <DeviceMock 
          pageContext="facebook"
          channelMode="facebook"
          initialMessage="Hi! Thanks for connecting with us on Facebook!  I'm Sarah, and I help people just like you create worry-free retirement plans. What's your biggest concern about retirement right now?"
        />
      </div>
    </div>
  );
}

function InstagramPage() {
  return (
    <div style={{ display: "flex", minHeight: "calc(100vh - 200px)" }}>
      {/* Left Side - Instagram Content */}
      <div style={{ flex: 1, padding: "40px", background: "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)" }}>
        <div
          style={{
            background: "#ffffff",
            borderRadius: 20,
            padding: "40px",
            boxShadow: "0 20px 40px rgba(20, 40, 87, 0.1)",
            height: "fit-content"
          }}
        >
          {/* Instagram Badge */}
          <div
            style={{
              background: "linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)",
              color: "#ffffff",
              padding: "12px 28px",
              borderRadius: 25,
              fontSize: "0.9em",
              fontWeight: 700,
              display: "inline-flex",
              alignItems: "center",
              gap: 10,
              marginBottom: 24,
              boxShadow: "0 4px 12px rgba(188, 24, 136, 0.4)"
            }}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
            </svg>
            <span>FOLLOW US ON INSTAGRAM</span>
          </div>
          
          <h1 style={{ fontSize: "2.2em", color: NAVY, marginBottom: 16, fontWeight: 700 }}>
            Connect via Instagram DMs
          </h1>
          <p style={{ fontSize: "1.1em", color: SLATE, marginBottom: 30, lineHeight: 1.6 }}>
            Slide into our DMs! Get retirement planning tips, seminar updates, and personalized financial guidance through Instagram Direct Messages.
          </p>
          
          {/* Instagram Stats */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 20, marginBottom: 30, padding: "20px", background: "linear-gradient(135deg, #ffeef8 0%, #ffe8f5 100%)", borderRadius: 12 }}>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: "2em", fontWeight: 700, background: "linear-gradient(45deg, #f09433, #dc2743, #bc1888)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", marginBottom: 4 }}>3,200+</div>
              <div style={{ fontSize: "0.85em", color: SLATE }}>Followers</div>
            </div>
            <div style={{ textAlign: "center", borderLeft: "1px solid #f5d5e8", borderRight: "1px solid #f5d5e8" }}>
              <div style={{ fontSize: "2em", fontWeight: 700, background: "linear-gradient(45deg, #f09433, #dc2743, #bc1888)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", marginBottom: 4 }}>850+</div>
              <div style={{ fontSize: "0.85em", color: SLATE }}>DMs/Month</div>
            </div>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: "2em", fontWeight: 700, background: "linear-gradient(45deg, #f09433, #dc2743, #bc1888)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", marginBottom: 4 }}>98%</div>
              <div style={{ fontSize: "0.85em", color: SLATE }}>Engagement</div>
            </div>
          </div>
          
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginTop: 30 }}>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Visual Storytelling</h3>
              <ul style={{ color: SLATE, lineHeight: 1.8, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>Daily retirement planning tips & reels</li>
                <li>Story Q&A sessions with advisors</li>
                <li>Behind-the-scenes office content</li>
                <li>Client success story highlights</li>
              </ul>
            </div>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Direct Messaging</h3>
              <ul style={{ color: SLATE, lineHeight: 1.8, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>Instant DM responses from Sarah AI</li>
                <li>Quick question answering</li>
                <li>Seminar registration via DMs</li>
                <li>Book consultations instantly</li>
              </ul>
            </div>
          </div>
          
          {/* Instagram CTA */}
          <div style={{ marginTop: 30, padding: "24px", background: "linear-gradient(135deg, #f09433 0%, #dc2743 50%, #bc1888 100%)", borderRadius: 16, color: "#fff" }}>
            <h4 style={{ marginBottom: 12, fontSize: "1.2em", fontWeight: 700 }}>Follow @provisionbrokerage</h4>
            <p style={{ marginBottom: 16, opacity: 0.95, lineHeight: 1.6 }}>
              Join our Instagram community for <strong>daily retirement tips, live Q&As, inspiring reels</strong>, and exclusive giveaways!
            </p>
            <div style={{ display: "flex", gap: 12 }}>
              <button style={{
                background: "#fff",
                color: "#dc2743",
                border: "none",
                padding: "12px 24px",
                borderRadius: 25,
                fontWeight: 700,
                fontSize: "0.95em",
                cursor: "pointer",
                boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
                flex: 1
              }}>
                Follow Us
              </button>
              <button style={{
                background: "rgba(255, 255, 255, 0.2)",
                color: "#fff",
                border: "2px solid #fff",
                padding: "12px 24px",
                borderRadius: 25,
                fontWeight: 700,
                fontSize: "0.95em",
                cursor: "pointer",
                flex: 1
              }}>
                Send DM
              </button>
            </div>
          </div>
          
          <div style={{ marginTop: 30, padding: "20px", background: CLOUD, borderRadius: 12, border: `1px solid ${BORDER}` }}>
            <h4 style={{ color: NAVY, marginBottom: 12, fontSize: "1.1em" }}>Try the Instagram DM demo:</h4>
            <ul style={{ color: SLATE, lineHeight: 1.8, paddingLeft: 20, fontSize: "0.95em", margin: 0 }}>
              <li>"I saw your reel about retirement planning!"</li>
              <li>"Can you help me understand annuities?"</li>
              <li>"When is your next seminar?"</li>
              <li>"I'd like to schedule a free consultation"</li>
            </ul>
          </div>
        </div>
      </div>
      
      {/* Right Side - Instagram DM Widget */}
      <div style={{ width: "420px", padding: "20px", background: "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)" }}>
        <DeviceMock 
          pageContext="instagram"
          channelMode="instagram"
          initialMessage="Hey there! Love that you found us on Instagram! I'm Sarah from ProVision Brokerage. Quick question - are you planning your own retirement, or helping a family member? Let's chat about how we can help!"
        />
      </div>
    </div>
  );
}

function WebsiteLeadsPage() {
  return (
    <div style={{ display: "flex", minHeight: "calc(100vh - 200px)" }}>
      {/* Left Side - NeuralApps Content */}
      <div style={{ flex: 1, padding: "40px", background: "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)" }}>
        <div
          style={{
            background: "#ffffff",
            borderRadius: 20,
            padding: "40px",
            boxShadow: "0 20px 40px rgba(20, 40, 87, 0.1)",
            height: "fit-content"
          }}
        >
          {/* NeuralApps Badge */}
          <div
            style={{
              background: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
              color: "#ffffff",
              padding: "12px 28px",
              borderRadius: 25,
              fontSize: "0.9em",
              fontWeight: 700,
              display: "inline-flex",
              alignItems: "center",
              gap: 10,
              marginBottom: 24,
              boxShadow: "0 4px 12px rgba(99, 102, 241, 0.4)"
            }}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5.5-2.5l7.51-3.49L17.5 6.5 9.99 9.99 6.5 17.5zm5.5-6.6c.61 0 1.1.49 1.1 1.1s-.49 1.1-1.1 1.1-1.1-.49-1.1-1.1.49-1.1 1.1-1.1z"/>
            </svg>
            <span>POWERED BY NEURALAPPS.AI</span>
          </div>
          
          <h1 style={{ fontSize: "2.2em", color: NAVY, marginBottom: 16, fontWeight: 700 }}>
            AI-Powered Lead Conversion
          </h1>
          <p style={{ fontSize: "1.1em", color: SLATE, marginBottom: 30, lineHeight: 1.6 }}>
            This intelligent chatbot was built by <strong>NeuralApps.ai</strong> to transform website visitors into qualified leads through conversational AI and smart qualification.
          </p>
          
          {/* Conversion Stats */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 20, marginBottom: 30, padding: "20px", background: "linear-gradient(135deg, #f0f2ff 0%, #e9ecff 100%)", borderRadius: 12 }}>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: "2em", fontWeight: 700, background: "linear-gradient(135deg, #6366f1, #8b5cf6)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", marginBottom: 4 }}>3.2x</div>
              <div style={{ fontSize: "0.85em", color: SLATE }}>Lead Conversion</div>
            </div>
            <div style={{ textAlign: "center", borderLeft: "1px solid #d4d9f7", borderRight: "1px solid #d4d9f7" }}>
              <div style={{ fontSize: "2em", fontWeight: 700, background: "linear-gradient(135deg, #6366f1, #8b5cf6)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", marginBottom: 4 }}>87%</div>
              <div style={{ fontSize: "0.85em", color: SLATE }}>Qualification Rate</div>
            </div>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: "2em", fontWeight: 700, background: "linear-gradient(135deg, #6366f1, #8b5cf6)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", marginBottom: 4 }}>24/7</div>
              <div style={{ fontSize: "0.85em", color: SLATE }}>Availability</div>
            </div>
          </div>
          
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginTop: 30 }}>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Smart Qualification</h3>
              <ul style={{ color: SLATE, lineHeight: 1.8, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>Conversational lead capture</li>
                <li>7-question qualification flow</li>
                <li>Retirement timeline assessment</li>
                <li>Asset & income evaluation</li>
                <li>Pain point identification</li>
              </ul>
            </div>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Instant Conversion</h3>
              <ul style={{ color: SLATE, lineHeight: 1.8, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>Real-time appointment booking</li>
                <li>Seminar registration in chat</li>
                <li>Personalized recommendations</li>
                <li>Multi-channel follow-up</li>
                <li>CRM integration ready</li>
              </ul>
            </div>
          </div>
          
          {/* How It Converts Section */}
          <div style={{ marginTop: 30, padding: "24px", background: "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)", borderRadius: 16, color: "#fff" }}>
            <h4 style={{ marginBottom: 16, fontSize: "1.3em", fontWeight: 700, display: "flex", alignItems: "center", gap: 10 }}>
              <span>How NeuralApps Converts Leads</span>
            </h4>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              <div style={{ padding: "16px", background: "rgba(99, 102, 241, 0.15)", borderRadius: 12, border: "1px solid rgba(99, 102, 241, 0.3)" }}>
                <div style={{ fontWeight: 700, marginBottom: 8, fontSize: "1.1em" }}>1. Engage Instantly</div>
                <div style={{ fontSize: "0.9em", opacity: 0.9, lineHeight: 1.5 }}>
                  AI greets visitors within seconds, asks about their retirement concerns, and builds rapport naturally.
                </div>
              </div>
              <div style={{ padding: "16px", background: "rgba(99, 102, 241, 0.15)", borderRadius: 12, border: "1px solid rgba(99, 102, 241, 0.3)" }}>
                <div style={{ fontWeight: 700, marginBottom: 8, fontSize: "1.1em" }}>2. Qualify Smartly</div>
                <div style={{ fontSize: "0.9em", opacity: 0.9, lineHeight: 1.5 }}>
                  Asks 7 strategic questions to understand age, timeline, assets, and pain points - without feeling like a form.
                </div>
              </div>
              <div style={{ padding: "16px", background: "rgba(99, 102, 241, 0.15)", borderRadius: 12, border: "1px solid rgba(99, 102, 241, 0.3)" }}>
                <div style={{ fontWeight: 700, marginBottom: 8, fontSize: "1.1em" }}>3. Provide Value</div>
                <div style={{ fontSize: "0.9em", opacity: 0.9, lineHeight: 1.5 }}>
                  Shares retirement insights, answers questions using ProVision's knowledge base, builds trust through education.
                </div>
              </div>
              <div style={{ padding: "16px", background: "rgba(99, 102, 241, 0.15)", borderRadius: 12, border: "1px solid rgba(99, 102, 241, 0.3)" }}>
                <div style={{ fontWeight: 700, marginBottom: 8, fontSize: "1.1em" }}>4. Convert Now</div>
                <div style={{ fontSize: "0.9em", opacity: 0.9, lineHeight: 1.5 }}>
                  Suggests immediate appointment booking or seminar registration based on their needs and urgency level.
                </div>
              </div>
            </div>
          </div>
          
          <div style={{ marginTop: 30, padding: "20px", background: CLOUD, borderRadius: 12, border: `1px solid ${BORDER}` }}>
            <h4 style={{ color: NAVY, marginBottom: 12, fontSize: "1.1em" }}>Experience the NeuralApps AI:</h4>
            <ul style={{ color: SLATE, lineHeight: 1.8, paddingLeft: 20, fontSize: "0.95em", margin: 0 }}>
              <li>"I need help planning my retirement"</li>
              <li>"How much do I need to retire comfortably?"</li>
              <li>"I'm worried about running out of money"</li>
              <li>"Can you help me understand annuities?"</li>
            </ul>
          </div>
          
          {/* NeuralApps CTA */}
          <div style={{ marginTop: 24, padding: "20px", background: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)", borderRadius: 12, color: "#fff", textAlign: "center" }}>
            <div style={{ fontSize: "0.9em", opacity: 0.95, marginBottom: 8 }}>
              Want AI-powered lead conversion for your business?
            </div>
            <div style={{ fontWeight: 700, fontSize: "1.1em" }}>
              Visit <span style={{ textDecoration: "underline" }}>NeuralApps.ai</span> to get started
            </div>
          </div>
        </div>
      </div>
      
      {/* Right Side - NeuralApps Widget */}
      <div style={{ width: "420px", padding: "20px", background: "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)" }}>
        <DeviceMock 
          pageContext="leads"
          channelMode="neuralapps"
          initialMessage="Hi! I'm Sarah from ProVision Brokerage!  I can see you're serious about your retirement - that's amazing! Let me ask you 3 quick questions so I can create a custom plan for YOUR situation. First - how soon are you planning to retire?"
        />
      </div>
    </div>
  );
}

// ClientServicePage removed - functionality consolidated into other pages

function App() {
  const [activePage, setActivePage] = useState("home");

  const renderContent = () => {
    switch (activePage) {
      case "Seminars":
        return <SeminarsPage />;
      case "Appointments":
        return <AppointmentsPage />;
      case "Facebook":
        return <FacebookPage />;
      case "Instagram":
        return <InstagramPage />;
      case "Website Leads":
        return <WebsiteLeadsPage />;
      default:
        return <Hero />;
    }
  };

  return (
    <div
      style={{
        background: "#ffffff",
        minHeight: "100vh",
        fontFamily: "'Inter', 'Arial', sans-serif",
        color: NAVY
      }}
    >
      <Header activePage={activePage} onNavigate={setActivePage} />
      {renderContent()}
      <Footer />
    </div>
  );
}


const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
