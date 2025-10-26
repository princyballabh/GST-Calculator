import React, { useState } from "react";

export default function AdminUpload() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [adminKey, setAdminKey] = useState("");
  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();
    // For demo, just set loggedIn if adminKey is entered
    if (adminKey.trim().length > 0) {
      setLoggedIn(true);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setUploadResult(null);
    const fd = new FormData();
    fd.append("file", file);
    try {
      const res = await fetch(`${process.env.NODE_ENV === 'production' ? process.env.NEXT_PUBLIC_API_URL || 'https://gst-calculator-backend-production.railway.app' : 'http://127.0.0.1:8000'}/admin/upload-pdf`, {
        method: "POST",
        body: fd,
      });
      const data = await res.json();
      console.log("Upload response:", data);
      setUploadResult(data);
    } catch (err) {
      console.error("Upload error:", err);
      setUploadResult({ error: "Upload failed." });
    }
    setLoading(false);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === "application/pdf") {
        setFile(droppedFile);
      }
    }
  };

  const styles = {
    container: {
      minHeight: "100vh",
      background: "linear-gradient(135deg, #432818 0%, #6F1D1B 100%)",
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
      marginBottom: "1rem",
      textShadow: "2px 2px 4px rgba(0,0,0,0.1)",
    },
    subtitle: {
      textAlign: "center",
      color: "#99582A",
      fontSize: "1.2rem",
      marginBottom: "2rem",
      fontStyle: "italic",
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
    dropZone: {
      border: `3px dashed ${dragActive ? "#99582A" : "#BB9457"}`,
      borderRadius: "15px",
      padding: "3rem 2rem",
      textAlign: "center",
      backgroundColor: dragActive
        ? "rgba(153, 88, 42, 0.1)"
        : "rgba(255,255,255,0.5)",
      transition: "all 0.3s ease",
      cursor: "pointer",
      position: "relative",
    },
    dropZoneContent: {
      color: "#432818",
      fontSize: "1.1rem",
    },
    fileIcon: {
      fontSize: "3rem",
      marginBottom: "1rem",
      color: "#99582A",
    },
    fileInput: {
      position: "absolute",
      inset: 0,
      opacity: 0,
      cursor: "pointer",
    },
    selectedFile: {
      marginBottom: "1rem",
      padding: "1rem",
      backgroundColor: "rgba(153, 88, 42, 0.1)",
      borderRadius: "10px",
      border: "1px solid #99582A",
      color: "#432818",
    },
    fileName: {
      fontWeight: "bold",
      color: "#6F1D1B",
    },
    resultCard: {
      marginTop: "2rem",
      padding: "1.5rem",
      backgroundColor: "rgba(255,255,255,0.95)",
      borderRadius: "15px",
      border: "2px solid #99582A",
      boxShadow: "0 8px 16px rgba(0,0,0,0.1)",
    },
    successResult: {
      backgroundColor: "rgba(76, 175, 80, 0.1)",
      border: "2px solid #4CAF50",
    },
    errorResult: {
      backgroundColor: "rgba(244, 67, 54, 0.1)",
      border: "2px solid #f44336",
    },
    resultText: {
      fontFamily: "monospace",
      fontSize: "0.95rem",
      color: "#432818",
      lineHeight: "1.5",
      whiteSpace: "pre-wrap",
    },
    updatesList: {
      listStyle: "none",
      padding: 0,
      margin: "1rem 0",
    },
    updateItem: {
      padding: "0.8rem",
      marginBottom: "0.5rem",
      backgroundColor: "rgba(76, 175, 80, 0.1)",
      borderRadius: "8px",
      border: "1px solid #4CAF50",
      color: "#432818",
    },
    backLink: {
      display: "inline-flex",
      alignItems: "center",
      gap: "0.5rem",
      marginTop: "2rem",
      padding: "1rem 1.5rem",
      color: "#000000ff",
      textDecoration: "none",
      backgroundColor: "rgba(255,255,255,0.1)",
      borderRadius: "12px",
      border: "2px solid rgba(255,255,255,0.2)",
      fontSize: "1.1rem",
      fontWeight: "500",
      transition: "all 0.3s ease",
    },
    lockIcon: {
      fontSize: "4rem",
      marginBottom: "1rem",
      color: "#99582A",
    },
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  if (!loggedIn) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <div style={{ textAlign: "center", marginBottom: "2rem" }}>
            <div style={styles.lockIcon}>🔐</div>
            <h1 style={styles.title}>Admin Access</h1>
            <p style={styles.subtitle}>Enter your admin key to continue</p>
          </div>
          <form onSubmit={handleLogin} style={styles.form}>
            <input
              type="password"
              placeholder="Enter admin key..."
              value={adminKey}
              onChange={(e) => setAdminKey(e.target.value)}
              required
              style={styles.input}
              onFocus={(e) => Object.assign(e.target.style, styles.inputFocus)}
              onBlur={(e) => Object.assign(e.target.style, styles.input)}
            />
            <button
              type="submit"
              style={styles.button}
              onMouseEnter={(e) =>
                Object.assign(e.target.style, {
                  ...styles.button,
                  ...styles.buttonHover,
                })
              }
              onMouseLeave={(e) => Object.assign(e.target.style, styles.button)}
            >
              🚀 Login
            </button>
          </form>
          <a
            href="/"
            style={styles.backLink}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = "rgba(255,255,255,0.2)";
              e.target.style.transform = "translateY(-2px)";
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = "rgba(255,255,255,0.1)";
              e.target.style.transform = "translateY(0)";
            }}
          >
            ← Back to Calculator
          </a>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={{ ...styles.card, maxWidth: "600px" }}>
        <h1 style={styles.title}>🔧 Admin Panel</h1>
        <p style={styles.subtitle}>Upload GST Rate PDFs to Update Database</p>

        <form onSubmit={handleUpload} style={styles.form}>
          <div
            style={styles.dropZone}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files[0] || null)}
              style={styles.fileInput}
            />
            <div style={styles.dropZoneContent}>
              <div style={styles.fileIcon}>📄</div>
              <div>
                <strong>Drag & drop your PDF file here</strong>
                <br />
                or click to browse files
              </div>
              <div
                style={{
                  marginTop: "0.5rem",
                  fontSize: "0.9rem",
                  color: "#99582A",
                }}
              >
                Only PDF files are accepted
              </div>
            </div>
          </div>

          {file && (
            <div style={styles.selectedFile}>
              <div style={styles.fileName}>📄 {file.name}</div>
              <div
                style={{
                  fontSize: "0.9rem",
                  color: "#99582A",
                  marginTop: "0.5rem",
                }}
              >
                Size: {formatFileSize(file.size)} • Ready to upload
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !file}
            style={{
              ...styles.button,
              ...(loading || !file ? styles.buttonDisabled : {}),
            }}
            onMouseEnter={(e) =>
              !(loading || !file) &&
              Object.assign(e.target.style, {
                ...styles.button,
                ...styles.buttonHover,
              })
            }
            onMouseLeave={(e) =>
              !(loading || !file) &&
              Object.assign(e.target.style, styles.button)
            }
          >
            {loading ? "⏳ Processing..." : "🚀 Upload PDF"}
          </button>
        </form>

        {uploadResult && (
          <div
            style={{
              ...styles.resultCard,
              ...(uploadResult.error
                ? styles.errorResult
                : styles.successResult),
            }}
          >
            <h3
              style={{
                color: "#6F1D1B",
                marginTop: 0,
                display: "flex",
                alignItems: "center",
                gap: "0.5rem",
              }}
            >
              {uploadResult.error ? "❌" : "✅"} Upload Result
            </h3>
            {uploadResult.error && (
              <div style={{ ...styles.resultText, color: "#d32f2f" }}>
                {uploadResult.error}
              </div>
            )}
            {uploadResult.message && (
              <div style={styles.resultText}>{uploadResult.message}</div>
            )}
            {uploadResult.ok && uploadResult.parsed_rows !== undefined && (
              <div style={{ marginTop: "1rem" }}>
                <div
                  style={{
                    fontWeight: "bold",
                    color: "#2e7d32",
                    marginBottom: "0.5rem",
                  }}
                >
                  ✅ Upload Successful!
                </div>
              </div>
            )}
            {uploadResult.parsed_rows !== undefined && (
              <div style={{ marginTop: "1rem" }}>
                <div style={{ fontWeight: "bold", color: "#6F1D1B" }}>
                  📊 Parsed {uploadResult.parsed_rows} rows successfully
                </div>
                {uploadResult.updates && (
                  <div style={{ marginTop: "1rem" }}>
                    <div
                      style={{
                        fontWeight: "bold",
                        color: "#6F1D1B",
                        marginBottom: "0.5rem",
                      }}
                    >
                      🔄 Database Updates:
                    </div>
                    <ul style={styles.updatesList}>
                      {uploadResult.updates.map((u, i) => (
                        <li key={i} style={styles.updateItem}>
                          <strong>HSN {u.hsn}:</strong>{" "}
                          {u.old !== null
                            ? `Updated from ${u.old}% to ${u.new}%`
                            : `Added new rate: ${u.new}%`}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {/* Debug section - remove after testing */}
            {process.env.NODE_ENV === "development" && (
              <details style={{ marginTop: "1rem", fontSize: "0.8rem" }}>
                <summary style={{ cursor: "pointer", color: "#666" }}>
                  Debug: Raw Response
                </summary>
                <pre
                  style={{
                    backgroundColor: "#f5f5f5",
                    padding: "0.5rem",
                    overflow: "auto",
                  }}
                >
                  {JSON.stringify(uploadResult, null, 2)}
                </pre>
              </details>
            )}
          </div>
        )}

        <a
          href="/"
          style={styles.backLink}
          onMouseEnter={(e) => {
            e.target.style.backgroundColor = "rgba(255,255,255,0.2)";
            e.target.style.transform = "translateY(-2px)";
          }}
          onMouseLeave={(e) => {
            e.target.style.backgroundColor = "rgba(255,255,255,0.1)";
            e.target.style.transform = "translateY(0)";
          }}
        >
          ← Back to Calculator
        </a>
      </div>
    </div>
  );
}
