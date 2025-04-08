import React from 'react';

function CheckoutButton({ slug, option, title }) {
  const handleClick = async () => {
    try {
      const response = await fetch("/api/create-checkout-session/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ slug, option }),
      });
      const data = await response.json();
      console.log(data); // Log the response to inspect
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
    <div className="flex flex-col items-center">
      <button
        onClick={handleClick}
        className="px-4 py-2 mt-12 bg-opacity-80 bg-blue-500 text-white shadow-md rounded hover:bg-blue-700"
      >
        {title}
      </button>
      <p className="italic text-xs mt-2 text-gray-400">Secure Checkout with Stripe</p>
    </div>
  );
}

export default CheckoutButton;
