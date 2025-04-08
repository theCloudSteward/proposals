import React from 'react';

function CheckoutButton({ slug, option, title }) {
  const handleClick = async () => {
    try {
      const response = await fetch("/api/create-checkout-session/", {  // exact match
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ slug, option }),
      });
      const data = await response.json();
      if (data.url) {
        window.location = data.url;
      } else {
        console.error("No URL returned from Stripe checkout session.");
      }
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };

  return (
    <button
      onClick={handleClick}
      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
    >
      {title}
    </button>
  );
}

export default CheckoutButton;
