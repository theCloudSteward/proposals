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
    <div>
      <button
        onClick={handleClick}
        className="px-4 py-2 m-12 bg-opacity-80 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        {title}
      </button>
      <p className="italic">Secure Checkout with Stripe</p>
    </div>
  );
}

export default CheckoutButton;
