import React from 'react';

export default function Custom404() {
  const styles = {
    container: {
      minHeight: "100vh",
      background: "linear-gradient(135deg, #6F1D1B 0%, #432818 100%)",
      padding: "2rem",
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      display: "flex",
      alignItems: "center",
      justifyContent: "center"
    },
    card: {
      maxWidth: "500px",
      backgroundColor: "#FFE6A7",
      borderRadius: "20px",
      padding: "3rem 2.5rem",
      boxShadow: "0 20px 40px rgba(0,0,0,0.3)",
      border: "2px solid #BB9457",
      textAlign: "center"
    },
    errorCode: {
      fontSize: "8rem",
      fontWeight: "bold",
      color: "#6F1D1B",
      marginBottom: "1rem",
      textShadow: "3px 3px 6px rgba(0,0,0,0.2)",
      lineHeight: "1"
    },
    title: {
      color: "#6F1D1B",
      fontSize: "2.5rem",
      fontWeight: "bold",
      marginBottom: "1rem",
      textShadow: "2px 2px 4px rgba(0,0,0,0.1)"
    },
    message: {
      color: "#99582A",
      fontSize: "1.2rem",
      marginBottom: "2.5rem",
      lineHeight: "1.6"
    },
    buttonGroup: {
      display: "flex",
      flexDirection: "column",
      gap: "1rem"
    },
    button: {
      padding: "1.2rem",
      fontSize: "1.1rem",
      fontWeight: "bold",
      color: "#FFE6A7",
      backgroundColor: "#99582A",
      border: "none",
      borderRadius: "12px",
      cursor: "pointer",
      transition: "all 0.3s ease",
      boxShadow: "0 6px 12px rgba(0,0,0,0.2)",
      textDecoration: "none",
      display: "inline-block",
      textAlign: "center"
    },
    secondaryButton: {
      backgroundColor: "#BB9457",
      color: "#432818"
    },
    icon: {
      fontSize: "4rem",
      marginBottom: "1rem"
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.icon}>🔍</div>
        <div style={styles.errorCode}>404</div>
        <h1 style={styles.title}>Page Not Found</h1>
        <p style={styles.message}>
          Oops! The page you're looking for seems to have wandered off. 
          Let's get you back to calculating those GST rates!
        </p>
        <div style={styles.buttonGroup}>
          <a 
            href="/"
            style={styles.button}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = "#6F1D1B";
              e.target.style.transform = "translateY(-2px)";
              e.target.style.boxShadow = "0 8px 16px rgba(0,0,0,0.3)";
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = "#99582A";
              e.target.style.transform = "translateY(0)";
              e.target.style.boxShadow = "0 6px 12px rgba(0,0,0,0.2)";
            }}
          >
            🏠 Go Home
          </a>
          <a 
            href="/admin"
            style={{...styles.button, ...styles.secondaryButton}}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = "#99582A";
              e.target.style.color = "#FFE6A7";
              e.target.style.transform = "translateY(-2px)";
              e.target.style.boxShadow = "0 8px 16px rgba(0,0,0,0.3)";
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = "#BB9457";
              e.target.style.color = "#432818";
              e.target.style.transform = "translateY(0)";
              e.target.style.boxShadow = "0 6px 12px rgba(0,0,0,0.2)";
            }}
          >
            🔧 Admin Panel
          </a>
        </div>
      </div>
    </div>
  );
}
