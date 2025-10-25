const { useState } = React;

const GOLD = "#FFC72C";
const NAVY = "#142857";
const SLATE = "#1C2540";
const CLOUD = "#F5F7FB";
const BORDER = "rgba(20, 40, 87, 0.12)";

const navLinks = ["Seminars", "Appointments", "Facebook", "Website Leads", "Client Service"];

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

function DeviceMock() {
  const [messages, setMessages] = useState([
    {
      role: "agent",
      sender: "AI Agent",
      text: "Welcome to ProVision Brokerage! How can I help you today? I can assist with lead qualification, booking appointments, answering FAQs, and more."
    }
  ]);
  const [inputMessage, setInputMessage] = useState("");
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
      const response = await fetch('http://localhost:8001/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          session_id: sessionId,
          context: {}
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

  return (
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
          background: NAVY,
          borderRadius: 42,
          padding: "28px 24px",
          boxShadow: "0 30px 60px rgba(20, 40, 87, 0.28)",
          zIndex: 1
        }}
      >
        <div
          style={{
            background: "#ffffff",
            borderRadius: 30,
            padding: "35px 28px",
            minHeight: 580,
            boxShadow: "0 18px 28px rgba(20, 40, 87, 0.12)"
          }}
        >
          <div
            style={{
              textTransform: "uppercase",
              fontSize: "0.72em",
              letterSpacing: "0.14em",
              color: "#8D97AF",
              fontWeight: 600,
              marginBottom: 18
            }}
          >
            AI Agent
          </div>
          
          <div
            style={{
              height: "480px",
              overflowY: "auto",
              marginBottom: "20px"
            }}
          >
            {messages.map((message, index) => (
              <ChatMessage key={index} {...message} />
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
                  🤖
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
              display: "flex",
              gap: 8,
              alignItems: "center"
            }}
          >
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything..."
              style={{
                flex: 1,
                padding: "8px 12px",
                border: "1px solid #ddd",
                borderRadius: 20,
                fontSize: "0.9em",
                outline: "none"
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
                borderRadius: 20,
                padding: "8px 16px",
                fontSize: "0.9em",
                fontWeight: 600,
                cursor: inputMessage.trim() && !isLoading ? "pointer" : "not-allowed",
                transition: "all 0.2s ease"
              }}
            >
              {isLoading ? "..." : "Send"}
            </button>
          </div>
        </div>
      </div>
    </div>
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
              Secure all the ProVisions you need to experience real success—powered by AI-guided expertise, trusted advisors, and effortless engagement every step of your journey.
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
              "Seamless Client Support—Everywhere You Are"
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
            Join the next generation of clients achieving more, faster, with ProVision's blend of experience and innovation. Your peace of mind—delivered.
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
          © 2023 ProVision Brokerage. All rights reserved. | 123 Finance St. Moneyville, USA | (123) 456-7890 | contact@provision.com
        </div>
      </div>
    </footer>
  );
}

function ChatbotPage() {
  const [messages, setMessages] = useState([
    {
      role: "agent",
      sender: "AI Agent",
      text: "Hello! I'm your AI assistant for ProVision Brokerage. I can help you with retirement planning questions, annuity information, and booking consultations. What would you like to know?",
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
      const response = await fetch('http://localhost:8001/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          session_id: sessionId,
          context: {}
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
                  🤖
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
            💡 Try asking about:
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
              🔒 Compliance Notice
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
  return (
    <div style={{ display: "flex", minHeight: "calc(100vh - 200px)" }}>
      {/* Left Side - Coming Soon Content */}
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
          <div
            style={{
              background: GOLD,
              color: NAVY,
              padding: "8px 24px",
              borderRadius: 20,
              fontSize: "0.9em",
              fontWeight: 700,
              display: "inline-block",
              marginBottom: 24
            }}
          >
            COMING SOON
          </div>
          <h1 style={{ fontSize: "2.2em", color: NAVY, marginBottom: 16, fontWeight: 700 }}>
            Seminar Management System
          </h1>
          <p style={{ fontSize: "1.1em", color: SLATE, marginBottom: 30, lineHeight: 1.6 }}>
            Complete seminar registration, history tracking, and feedback system with AI-powered assistance
          </p>
          
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginTop: 30 }}>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Seminar Registration</h3>
              <ul style={{ color: SLATE, lineHeight: 1.6, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>Interactive registration flow</li>
                <li>Seminar topics from ProVision content</li>
                <li>SMS/WhatsApp reminder options</li>
                <li>Privacy consent and compliance</li>
                <li>AI-guided registration process</li>
              </ul>
            </div>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>History & Feedback</h3>
              <ul style={{ color: SLATE, lineHeight: 1.6, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>Past seminar tracking</li>
                <li>Rating and feedback system</li>
                <li>Follow-up booking options</li>
                <li>Completion certificates</li>
                <li>Personalized recommendations</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      {/* Right Side - Chat Widget */}
      <div style={{ width: "420px", padding: "20px", background: "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)" }}>
        <DeviceMock />
      </div>
    </div>
  );
}

function AppointmentsPage() {
  return (
    <div style={{ display: "flex", minHeight: "calc(100vh - 200px)" }}>
      {/* Left Side - Coming Soon Content */}
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
          <div
            style={{
              background: GOLD,
              color: NAVY,
              padding: "8px 24px",
              borderRadius: 20,
              fontSize: "0.9em",
              fontWeight: 700,
              display: "inline-block",
              marginBottom: 24
            }}
          >
            COMING SOON
          </div>
          <h1 style={{ fontSize: "2.2em", color: NAVY, marginBottom: 16, fontWeight: 700 }}>
            Smart Appointment Booking
          </h1>
          <p style={{ fontSize: "1.1em", color: SLATE, marginBottom: 30, lineHeight: 1.6 }}>
            AI-powered qualification and scheduling system with multi-channel reminders
          </p>
          
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginTop: 30 }}>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Smart Workflow</h3>
              <ul style={{ color: SLATE, lineHeight: 1.6, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>AI qualification questions</li>
                <li>Advisor availability calendar</li>
                <li>Time slot selection</li>
                <li>Confirmation system</li>
                <li>Source-based recommendations</li>
              </ul>
            </div>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Multi-Channel</h3>
              <ul style={{ color: SLATE, lineHeight: 1.6, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>SMS reminder previews</li>
                <li>WhatsApp integration</li>
                <li>Email confirmations</li>
                <li>Phone call scheduling</li>
                <li>ProVision expertise citations</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      {/* Right Side - Chat Widget */}
      <div style={{ width: "420px", padding: "20px", background: "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)" }}>
        <DeviceMock />
      </div>
    </div>
  );
}

function FacebookPage() {
  return (
    <div style={{ display: "flex", minHeight: "calc(100vh - 200px)" }}>
      {/* Left Side - Coming Soon Content */}
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
          <div
            style={{
              background: GOLD,
              color: NAVY,
              padding: "8px 24px",
              borderRadius: 20,
              fontSize: "0.9em",
              fontWeight: 700,
              display: "inline-block",
              marginBottom: 24
            }}
          >
            COMING SOON
          </div>
          <h1 style={{ fontSize: "2.2em", color: NAVY, marginBottom: 16, fontWeight: 700 }}>
            Social Media Integration
          </h1>
          <p style={{ fontSize: "1.1em", color: SLATE, marginBottom: 30, lineHeight: 1.6 }}>
            Facebook Messenger integration for lead capture and qualification with AI assistance
          </p>
          
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginTop: 30 }}>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Lead Capture</h3>
              <ul style={{ color: SLATE, lineHeight: 1.6, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>Facebook Messenger interface</li>
                <li>Direct message conversations</li>
                <li>Lead qualification questions</li>
                <li>Quick answer responses</li>
                <li>Booking escalation prompts</li>
              </ul>
            </div>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Social Workflow</h3>
              <ul style={{ color: SLATE, lineHeight: 1.6, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>Modern messaging UI</li>
                <li>Real-time typing indicators</li>
                <li>Message status tracking</li>
                <li>Call-to-action buttons</li>
                <li>Source-based content</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      {/* Right Side - Chat Widget */}
      <div style={{ width: "420px", padding: "20px", background: "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)" }}>
        <DeviceMock />
      </div>
    </div>
  );
}

function WebsiteLeadsPage() {
  return (
    <div style={{ display: "flex", minHeight: "calc(100vh - 200px)" }}>
      {/* Left Side - Coming Soon Content */}
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
          <div
            style={{
              background: GOLD,
              color: NAVY,
              padding: "8px 24px",
              borderRadius: 20,
              fontSize: "0.9em",
              fontWeight: 700,
              display: "inline-block",
              marginBottom: 24
            }}
          >
            COMING SOON
          </div>
          <h1 style={{ fontSize: "2.2em", color: NAVY, marginBottom: 16, fontWeight: 700 }}>
            Lead Management Dashboard
          </h1>
          <p style={{ fontSize: "1.1em", color: SLATE, marginBottom: 30, lineHeight: 1.6 }}>
            Comprehensive lead collection, tracking, and follow-up system with multi-channel integration
          </p>
          
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginTop: 30 }}>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Lead Collection</h3>
              <ul style={{ color: SLATE, lineHeight: 1.6, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>Visitor information forms</li>
                <li>Chat-driven lead collection</li>
                <li>Interest qualification</li>
                <li>Preferred channel selection</li>
                <li>Source tracking</li>
              </ul>
            </div>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Follow-up System</h3>
              <ul style={{ color: SLATE, lineHeight: 1.6, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>SMS follow-up previews</li>
                <li>WhatsApp integration</li>
                <li>Email sequence automation</li>
                <li>Lead nurturing workflows</li>
                <li>ProVision content citations</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      {/* Right Side - Chat Widget */}
      <div style={{ width: "420px", padding: "20px", background: "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)" }}>
        <DeviceMock />
      </div>
    </div>
  );
}

function ClientServicePage() {
  return (
    <div style={{ display: "flex", minHeight: "calc(100vh - 200px)" }}>
      {/* Left Side - Coming Soon Content */}
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
          <div
            style={{
              background: GOLD,
              color: NAVY,
              padding: "8px 24px",
              borderRadius: 20,
              fontSize: "0.9em",
              fontWeight: 700,
              display: "inline-block",
              marginBottom: 24
            }}
          >
            COMING SOON
          </div>
          <h1 style={{ fontSize: "2.2em", color: NAVY, marginBottom: 16, fontWeight: 700 }}>
            Enhanced Client Support
          </h1>
          <p style={{ fontSize: "1.1em", color: SLATE, marginBottom: 30, lineHeight: 1.6 }}>
            AI-powered self-service FAQ system with live agent escalation and transparent sourcing
          </p>
          
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginTop: 30 }}>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Self-Service FAQ</h3>
              <ul style={{ color: SLATE, lineHeight: 1.6, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>Account management help</li>
                <li>Product information</li>
                <li>Service request handling</li>
                <li>Document access</li>
                <li>Search functionality</li>
              </ul>
            </div>
            <div style={{ textAlign: "left" }}>
              <h3 style={{ color: NAVY, marginBottom: 12, fontSize: "1.2em" }}>Escalation & Logging</h3>
              <ul style={{ color: SLATE, lineHeight: 1.6, paddingLeft: 20, fontSize: "0.95em" }}>
                <li>Live agent escalation</li>
                <li>Call-back request system</li>
                <li>Query logging</li>
                <li>Source attribution</li>
                <li>Transparent citations</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      {/* Right Side - Chat Widget */}
      <div style={{ width: "420px", padding: "20px", background: "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)" }}>
        <DeviceMock />
      </div>
    </div>
  );
}

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
      case "Website Leads":
        return <WebsiteLeadsPage />;
      case "Client Service":
        return <ClientServicePage />;
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
