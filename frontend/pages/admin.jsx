import { useState } from "react";

export default function Admin() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
  };

  const uploadPDF = async () => {
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload-pdf", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error uploading PDF:", error);
      setResult({ error: "Failed to upload PDF" });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
      <h1>Admin Panel - Upload GST PDF</h1>

      <div style={{ marginBottom: "20px" }}>
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          style={{
            width: "100%",
            padding: "10px",
            fontSize: "16px",
            border: "1px solid #ccc",
            borderRadius: "4px",
          }}
        />

        {file && (
          <div style={{ marginTop: "10px" }}>
            <p>Selected file: {file.name}</p>
            <button
              onClick={uploadPDF}
              disabled={uploading}
              style={{
                padding: "10px 20px",
                fontSize: "16px",
                backgroundColor: "#28a745",
                color: "white",
                border: "none",
                borderRadius: "4px",
                cursor: uploading ? "not-allowed" : "pointer",
              }}
            >
              {uploading ? "Uploading..." : "Upload PDF"}
            </button>
          </div>
        )}
      </div>

      {result && (
        <div
          style={{
            padding: "20px",
            border: "1px solid #ccc",
            borderRadius: "4px",
            backgroundColor: result.error ? "#ffe6e6" : "#d4edda",
          }}
        >
          {result.error ? (
            <p style={{ color: "red" }}>{result.error}</p>
          ) : (
            <div>
              <h3>Upload Successful!</h3>
              <p>
                <strong>Message:</strong> {result.message}
              </p>
              <p>
                <strong>Filename:</strong> {result.filename}
              </p>
              <p>
                <strong>Rates Processed:</strong> {result.rates_count}
              </p>
            </div>
          )}
        </div>
      )}

      <div style={{ marginTop: "40px", textAlign: "center" }}>
        <a href="/" style={{ color: "#0070f3", textDecoration: "underline" }}>
          Back to Calculator
        </a>
      </div>
    </div>
  );
}
