import { useState } from 'react';

export default function Home() {
  const [productName, setProductName] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const calculateGST = async () => {
    if (!productName.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/calculate/${encodeURIComponent(productName)}`);
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error calculating GST:', error);
      setResult({ error: 'Failed to calculate GST rate' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h1>GST Calculator</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          placeholder="Enter product name"
          style={{
            width: '100%',
            padding: '10px',
            fontSize: '16px',
            border: '1px solid #ccc',
            borderRadius: '4px'
          }}
          onKeyPress={(e) => e.key === 'Enter' && calculateGST()}
        />
        <button
          onClick={calculateGST}
          disabled={loading}
          style={{
            marginTop: '10px',
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Calculating...' : 'Calculate GST'}
        </button>
      </div>

      {result && (
        <div style={{
          padding: '20px',
          border: '1px solid #ccc',
          borderRadius: '4px',
          backgroundColor: result.error ? '#ffe6e6' : '#e6f7ff'
        }}>
          {result.error ? (
            <p style={{ color: 'red' }}>{result.error}</p>
          ) : (
            <div>
              <h3>GST Rate Found!</h3>
              <p><strong>Product:</strong> {result.product}</p>
              <p><strong>HSN Code:</strong> {result.hsn}</p>
              <p><strong>Description:</strong> {result.description}</p>
              <p><strong>GST Rate:</strong> {result.rate}%</p>
            </div>
          )}
        </div>
      )}
      
      <div style={{ marginTop: '40px', textAlign: 'center' }}>
        <a href="/admin" style={{ color: '#0070f3', textDecoration: 'underline' }}>
          Admin Panel (Upload PDF)
        </a>
      </div>
    </div>
  );
}
