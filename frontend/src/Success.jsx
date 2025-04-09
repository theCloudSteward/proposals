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
        if (data.error) {
          throw new Error(data.error);
        }
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
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-green-600 mb-4 text-center">
          Payment Successful!
        </h1>
        {loading && (
          <p className="text-gray-600 text-center">Loading your order details...</p>
        )}
        {error && (
          <p className="text-red-500 font-medium text-center">Error: {error}</p>
        )}
        {sessionDetails && (
          <div className="space-y-4">
            <p className="text-lg">
              Thank you, <span className="font-semibold">{sessionDetails.customer_name}</span>!
              Your payment has been processed successfully.
            </p>
            <p className="text-gray-700">
              Total Charged:{' '}
              <span className="font-semibold">
                ${(sessionDetails.amount_total / 100).toFixed(2)}{' '}
                {sessionDetails.currency.toUpperCase()}
              </span>
            </p>
            {sessionDetails.receipt_url ? (
              <a
                href={sessionDetails.receipt_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block w-full px-4 py-2 text-center text-white bg-blue-600 rounded hover:bg-blue-700 transition"
              >
                Download Receipt
              </a>
            ) : (
              <p className="text-gray-500 italic">
                No receipt available at this time.
              </p>
            )}
          </div>
        )}
        <nav className="mt-6 flex justify-between text-sm">
          <a
            href="https://www.thecloudsteward.com/"
            className="text-blue-500 hover:underline"
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
    </div>
  );
};

export default Success;