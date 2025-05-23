import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const Success = () => {
  const location   = useLocation();
  const sessionId  = new URLSearchParams(location.search).get('session_id');

  const [sessionDetails, setSessionDetails] = useState(null);
  const [loading,         setLoading]       = useState(true);
  const [error,           setError]         = useState(null);

  /* -------------------------------------------------- */
  /*  Set tab title                                     */
  /* -------------------------------------------------- */
  useEffect(() => {
    document.title = 'Payment Successful';
  }, []);

  /* -------------------------------------------------- */
  /*  Fetch session details from backend                */
  /* -------------------------------------------------- */
  useEffect(() => {
    if (!sessionId) {
      setError(
        'Missing session ID. Please check the URL or contact support.',
      );
      console.error('Missing session ID. Please check the URL.');
      setLoading(false);
      return;
    }

    (async () => {
      try {
        const resp = await fetch(`/api/order/success?session_id=${sessionId}`);
        if (!resp.ok) {
          console.error(
            `Failed to fetch session details. Status: ${resp.status}`,
          );
          throw new Error(`Failed to fetch session details. Status: ${resp.status}`);
        }

        const data = await resp.json();
        if (data.error) {
          console.error(data.error);
          throw new Error(data.error);
        }

        setSessionDetails(data);
      } catch (err) {
        setError(`Unable to retrieve payment details: ${err.message}`);
      } finally {
        setLoading(false);
      }
    })();
  }, [sessionId]);

  /* -------------------------------------------------- */
  /*  Render                                            */
  /* -------------------------------------------------- */
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-green-600 mb-6 text-center">
          Payment&nbsp;Successful!
        </h1>

        {loading && (
          <p className="text-gray-600 text-center">
            Loading your order details…
          </p>
        )}

        {error && (
          <div className="mb-4 p-4 bg-red-100 text-red-700 rounded">
            <p className="font-medium">Oops! Something went wrong.</p>
            <p>{error}</p>
            <p className="mt-2">
              Please try refreshing the page or contact support for assistance.
            </p>
          </div>
        )}

        {sessionDetails && (
          <div className="space-y-4">
            <p className="text-lg">
              Thank you,&nbsp;
              <span className="font-semibold">
                {sessionDetails.customer_name}
              </span>
              ! Your payment has been processed successfully.
            </p>

            {/* ---------- receipt link OR friendly fallback ---------- */}
            {sessionDetails.receipt_url ? (
              <a
                href={sessionDetails.receipt_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block w-full px-4 py-2 text-center text-white bg-blue-600 rounded hover:bg-blue-700 transition"
              >
                View Receipt
              </a>
            ) : (
              <p className="text-gray-500 italic">
                {sessionDetails.message ??
                  'Thank you for your purchase. You should receive a confirmation email shortly with your receipt.'}
              </p>
            )}
          </div>
        )}

        <nav className="mt-6 flex justify-between text-sm">
          <a
            href="https://www.thecloudsteward.com/"
            className="text-blue-500 hover:underline"
          >
            Return Home
          </a>
          <a
            href="https://www.thecloudsteward.com/contact"
            className="text-blue-500 hover:underline"
          >
            Contact Support
          </a>
        </nav>
      </div>
    </div>
  );
};

export default Success;
