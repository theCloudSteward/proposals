// Success.jsx
import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const Success = () => {
  const location = useLocation();
  const sessionId = new URLSearchParams(location.search).get('session_id');

  const [sessionDetails, setSessionDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Set the tab title
  useEffect(() => {
    document.title = "Payment Successful";
  }, []);

  useEffect(() => {
    if (!sessionId) {
      setError('No session ID provided.');
      setLoading(false);
      return;
    }

    async function fetchSessionDetails() {
      try {
        const response = await fetch(`/api/order/success?session_id=${sessionId}`);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setSessionDetails(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    }

    fetchSessionDetails();
  }, [sessionId]);

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Payment Successful!</h1>
      {loading && <p className="text-lg">Loading order details...</p>}
      {error && <p className="text-red-500 text-lg">Error: {error}</p>}
      {sessionDetails && (
        <div className="bg-white shadow-md rounded p-6 mb-6">
          <p className="text-xl mb-2">
            Thank you for your order, <span className="font-semibold">{sessionDetails.customer_name}</span>!
          </p>
          <p className="mb-2">
            Total Charged: <span className="font-semibold">
              ${(sessionDetails.amount_total / 100).toFixed(2)} {sessionDetails.currency.toUpperCase()}
            </span>
          </p>
          {sessionDetails.receipt_url ? (
            <a
              href={sessionDetails.receipt_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline font-medium"
            >
              Download Receipt
            </a>
          ) : (
            <p className="text-gray-700">No receipt available.</p>
          )}
        </div>
      )}
      <nav className="mt-4">
        <a
          href="https://www.thecloudsteward.com/"
          className="text-blue-500 hover:underline mr-4"
        >
          Return Home
        </a>
        <a
          href="https://www.thecloudsteward.com/contact"
          className="text-blue-500 hover:underline"
        >
          Contact Support
        </a>
      </nav>
    </div>
  );
};

export default Success;
