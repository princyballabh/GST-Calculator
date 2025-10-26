import React, { useState } from "react";

export default function GSTCalculator() {
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [inclusive, setInclusive] = useState(false);
  const [result, setResult] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setSuggestions([]);
    try {
      const res = await fetch(`${process.env.NODE_ENV === 'production' ? process.env.NEXT_PUBLIC_API_URL || 'https://gst-calculator-backend-production.railway.app' : 'http://127.0.0.1:8000'}/api/calc`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description, price: Number(price), inclusive }),
      });
      const data = await res.json();
      if (data.matched) {
        // Store full response object for display
        setResult(data);
      } else {
        setSuggestions(data.suggestions || []);
      }
    } catch (err) {
      setResult({ error: "Error calculating GST." });
    }
    setLoading(false);
  };

  const styles = {
    container: {
      minHeight: "100vh",
      background: "linear-gradient(135deg, #6F1D1B 0%, #432818 100%)",
      padding: "2rem",
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    },
    card: {
      maxWidth: "500px",
      margin: "0 auto",
      backgroundColor: "#FFE6A7",
      borderRadius: "20px",
      padding: "2.5rem",
      boxShadow: "0 20px 40px rgba(0,0,0,0.3)",
      border: "2px solid #BB9457",
    },
    title: {
      textAlign: "center",
      color: "#6F1D1B",
      fontSize: "2.5rem",
      fontWeight: "bold",
      marginBottom: "2rem",
      textShadow: "2px 2px 4px rgba(0,0,0,0.1)",
    },
    form: {
      display: "flex",
      flexDirection: "column",
      gap: "1.5rem",
    },
    input: {
      padding: "1rem",
      fontSize: "1.1rem",
      border: "2px solid #BB9457",
      borderRadius: "12px",
      backgroundColor: "rgba(255,255,255,0.9)",
      color: "#432818",
      outline: "none",
      transition: "all 0.3s ease",
      boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
    },
    inputFocus: {
      borderColor: "#99582A",
      transform: "translateY(-2px)",
      boxShadow: "0 6px 12px rgba(0,0,0,0.15)",
    },
    checkboxContainer: {
      display: "flex",
      alignItems: "center",
      gap: "0.5rem",
      padding: "0.5rem",
      fontSize: "1.1rem",
      color: "#432818",
      fontWeight: "500",
    },
    checkbox: {
      width: "20px",
      height: "20px",
      accentColor: "#99582A",
    },
    button: {
      padding: "1.2rem",
      fontSize: "1.2rem",
      fontWeight: "bold",
      color: "#FFE6A7",
      backgroundColor: "#99582A",
      border: "none",
      borderRadius: "12px",
      cursor: "pointer",
      transition: "all 0.3s ease",
      boxShadow: "0 6px 12px rgba(0,0,0,0.2)",
      textTransform: "uppercase",
      letterSpacing: "1px",
    },
    buttonHover: {
      backgroundColor: "#6F1D1B",
      transform: "translateY(-2px)",
      boxShadow: "0 8px 16px rgba(0,0,0,0.3)",
    },
    buttonDisabled: {
      backgroundColor: "#BB9457",
      cursor: "not-allowed",
      transform: "none",
    },
    resultCard: {
      marginTop: "2rem",
      padding: "1.5rem",
      backgroundColor: "rgba(255,255,255,0.95)",
      borderRadius: "15px",
      border: "2px solid #99582A",
      boxShadow: "0 8px 16px rgba(0,0,0,0.1)",
    },
    resultItem: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      padding: "0.8rem 0",
      borderBottom: "1px solid #BB9457",
      fontSize: "1.1rem",
      color: "#432818",
    },
    resultLabel: {
      fontWeight: "600",
    },
    resultValue: {
      fontWeight: "bold",
      color: "#6F1D1B",
    },
    gstBreakdown: {
      fontSize: "0.9rem",
      color: "#99582A",
      fontStyle: "italic",
      marginTop: "0.3rem",
    },
    errorCard: {
      marginTop: "2rem",
      padding: "1.5rem",
      backgroundColor: "#ff6b6b",
      color: "white",
      borderRadius: "15px",
      textAlign: "center",
      fontWeight: "bold",
    },
    suggestions: {
      marginTop: "2rem",
      padding: "1.5rem",
      backgroundColor: "rgba(255,255,255,0.95)",
      borderRadius: "15px",
      border: "2px solid #BB9457",
    },
    suggestionsList: {
      listStyle: "none",
      padding: "0",
      margin: "1rem 0 0 0",
    },
    suggestionItem: {
      padding: "0.8rem",
      marginBottom: "0.5rem",
      backgroundColor: "rgba(187, 148, 87, 0.1)",
      borderRadius: "8px",
      color: "#432818",
      border: "1px solid #BB9457",
    },
    adminLink: {
      display: "block",
      textAlign: "center",
      marginTop: "2rem",
      padding: "1rem",
      color: "#000000ff",
      textDecoration: "none",
      backgroundColor: "rgba(255,255,255,0.1)",
      borderRadius: "10px",
      border: "2px solid rgba(255,255,255,0.2)",
      fontSize: "1.1rem",
      fontWeight: "500",
      transition: "all 0.3s ease",
    },
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>GST Calculator</h1>
        <form onSubmit={handleSubmit} style={styles.form}>
          <input
            type="text"
            placeholder="Enter product name or description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            style={styles.input}
            onFocus={(e) => Object.assign(e.target.style, styles.inputFocus)}
            onBlur={(e) => Object.assign(e.target.style, styles.input)}
          />
          <input
            type="number"
            placeholder="Enter price (₹)"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
            style={styles.input}
            onFocus={(e) => Object.assign(e.target.style, styles.inputFocus)}
            onBlur={(e) => Object.assign(e.target.style, styles.input)}
          />
          <label style={styles.checkboxContainer}>
            <input
              type="checkbox"
              checked={inclusive}
              onChange={(e) => setInclusive(e.target.checked)}
              style={styles.checkbox}
            />
            Price includes GST
          </label>
          <button
            type="submit"
            disabled={loading}
            style={{
              ...styles.button,
              ...(loading ? styles.buttonDisabled : {}),
            }}
            onMouseEnter={(e) =>
              !loading &&
              Object.assign(e.target.style, {
                ...styles.button,
                ...styles.buttonHover,
              })
            }
            onMouseLeave={(e) =>
              !loading && Object.assign(e.target.style, styles.button)
            }
          >
            {loading ? "Calculating..." : "Calculate GST"}
          </button>
        </form>

        {result && !result.error && (
          <div style={styles.resultCard}>
            <div style={styles.resultItem}>
              <span style={styles.resultLabel}>GST Rate:</span>
              <span style={styles.resultValue}>{result.calc.rate}%</span>
            </div>
            <div style={styles.resultItem}>
              <span style={styles.resultLabel}>Base Price:</span>
              <span style={styles.resultValue}>₹{result.calc.base}</span>
            </div>
            <div style={styles.resultItem}>
              <span style={styles.resultLabel}>GST Amount:</span>
              <div>
                <span style={styles.resultValue}>₹{result.calc.gst}</span>
                {result.calc.cgst && result.calc.sgst && (
                  <div style={styles.gstBreakdown}>
                    CGST: ₹{result.calc.cgst} + SGST: ₹{result.calc.sgst}
                  </div>
                )}
              </div>
            </div>
            <div
              style={{
                ...styles.resultItem,
                borderBottom: "none",
                fontSize: "1.3rem",
                fontWeight: "bold",
              }}
            >
              <span style={styles.resultLabel}>Total Price:</span>
              <span style={{ ...styles.resultValue, fontSize: "1.4rem" }}>
                ₹{result.calc.total}
              </span>
            </div>
          </div>
        )}

        {result && result.error && (
          <div style={styles.errorCard}>{result.error}</div>
        )}

        {suggestions.length > 0 && (
          <div style={styles.suggestions}>
            <h3 style={{ color: "#432818", marginTop: 0 }}>
              No exact match found. Did you mean:
            </h3>
            <ul style={styles.suggestionsList}>
              {suggestions.map((s, i) => (
                <li key={i} style={styles.suggestionItem}>
                  {s.description} <strong>(Match: {s.score}%)</strong>
                </li>
              ))}
            </ul>
          </div>
        )}

        <a
          href="/admin"
          style={styles.adminLink}
          onMouseEnter={(e) => {
            e.target.style.backgroundColor = "rgba(255,255,255,0.2)";
            e.target.style.transform = "translateY(-2px)";
          }}
          onMouseLeave={(e) => {
            e.target.style.backgroundColor = "rgba(255,255,255,0.1)";
            e.target.style.transform = "translateY(0)";
          }}
        >
          🔧 Admin Panel - Upload GST PDFs
        </a>
      </div>
    </div>
  );
}
