import React, { useState } from 'react';
import CheckoutButton from './CheckoutButton';

function SubscriptionCard({
  title,
  subtitle,
  price,
  children, // extra details (for Basic card)
}) {
  // Default background position is centered
  const [bgPos, setBgPos] = useState('50% 50%');

  const handleMouseMove = (e) => {
    const { left, top, width, height } = e.currentTarget.getBoundingClientRect();
    // Calculate cursor position as percentages
    const x = ((e.clientX - left) / width) * 100;
    const y = ((e.clientY - top) / height) * 100;
    // Amplify the effect relative to center (50%, 50%)
    const factor = 1; // Increase this value for a larger effect
    const offsetX = 50 + (x - 50) * factor;
    const offsetY = 50 + (y - 50) * factor;
    setBgPos(`${offsetX}% ${offsetY}%`);
  };

  const handleMouseLeave = () => {
    // Reset to centered gradient when mouse leaves
    setBgPos('50% 50%');
  };

  return (
    <div
      className="group bg-white bg-opacity-40 hover:bg-opacity-60 shadow-md rounded-xl overflow-hidden flex flex-col items-center transition-all duration-300 transform hover:scale-105 hover:shadow-2xl"
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    >
      {/* Header with shifting gradient */}
      <div
        className="w-full transition-all duration-300"
        style={{
          background: 'linear-gradient(142deg, rgba(253,240,249,1) 0%, rgba(181,218,247,1) 100%)',
          backgroundSize: '200% 200%',
          backgroundPosition: bgPos,
          filter: 'brightness(1.05)',
        }}
      >
        <div className="p-3 text-center">
          <h3 className="text-xl font-semibold text-gray-800">{title}</h3>
          <p className="text-gray-600">{subtitle}</p>
        </div>
      </div>

      {/* Card Content */}
      <div className="w-full p-6 flex flex-col items-center">
        {/* Price Display */}
        <div className="w-full text-center my-6">
          <p className="text-3xl font-bold text-gray-800">
            ${price}
            <span className="text-base text-gray-500">/month</span>
          </p>
        </div>
        {children}
      </div>
    </div>
  );
}

function SubscriptionPlans({ data }) {
  return (
    <div className="my-10 py-10">
      <h2 className="max-w-5xl mx-auto text-center px-4 font-bold mb-8">Support Plans</h2>
      <div className="max-w-5xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Basic Card with extra details */}
          <SubscriptionCard
            title="Basic"
            subtitle="Essential Error Support"
            price={data.tier_1_subscription_price}
          >
            <div className="mt-4 w-full text-left">
              <div className="p-3 flex items-center bg-white bg-opacity-30 shadow-md rounded-lg">
                <span className="mr-4 text-xl">➕</span>
                <span className="text-sm font-bold">
                  ${data.project_with_subscription_price} One-Time Project Fee
                </span>
                <span className="inline-flex items-center justify-center rounded-lg bg-green-700 bg-opacity-60 font-bold ml-2 p-2 border border-transparent text-xs text-white transition-all shadow-sm">
                  {data.project_discount_percent}% Off
                </span>
              </div>
              <hr className="my-3 border-gray-300" />
              <div className="flex items-center">
                <span className="mr-2 text-xl">✔️</span>
                <span className="text-sm">24/7 Error Monitoring</span>
              </div>
              <hr className="my-3 border-gray-300" />
              <div className="flex items-center">
                <span className="mr-2 text-xl">✔️</span>
                <span className="text-sm">100% Uptime for <strong>All Cloud Steward</strong> Customizations</span>
              </div>
              <hr className="my-3 border-gray-300" />
              <div className="flex items-center">
                <span className="mr-2 text-xl">✔️</span>
                <span className="text-sm">Resolve Any Cloud Steward Script Errors within Hours</span>
              </div>
            </div>
            <CheckoutButton slug={data.slug} option='tier_1_subscription_price' subscriptionTitle='Basic Support Plan' buttonTitle="Subscribe" />
          </SubscriptionCard>

          {/* Standard Card */}
          <SubscriptionCard
            title="Standard"
            subtitle="Full System Support"
            price={data.tier_2_subscription_price}
          >
            <div className="mt-4 w-full text-left">
              <div className="p-3 flex items-center bg-white bg-opacity-30 shadow-md rounded-lg">
                <span className="mr-4 text-xl">➕</span>
                <span className="text-sm font-bold">
                  ${data.project_with_subscription_price} One-Time Project Fee
                </span>
                <span className="inline-flex items-center justify-center rounded-lg bg-green-700 bg-opacity-60 font-bold ml-2 p-2 border border-transparent text-xs text-white transition-all shadow-sm">
                  {data.project_discount_percent}% Off
                </span>
              </div>
              <hr className="my-3 border-gray-300" />
              <span className="mr-2 text-xl mt-1">✔️</span>
              <span className="text-sm"><strong>Everything in Basic</strong></span>
              <hr className="my-3 border-gray-300" />
              <div className="flex items-center">
                <span className="mr-2 text-xl">✔️</span>
                <span className="text-sm">100% Uptime for <strong>All Essential Scripts and Workflows</strong></span>
              </div>
              <hr className="my-3 border-gray-300" />
              <div className="flex items-center">
                <span className="mr-2 text-xl">✔️</span>
                <span className="text-sm">Resolve <strong>All Essential Automation</strong> Errors within Hours</span>
              </div>
            </div>
            <CheckoutButton slug={data.slug} option='tier_2_subscription_price' subscriptionTitle='Standard Support Plan' buttonTitle="Subscribe" />
          </SubscriptionCard>

          {/* Premium Card */}
          <SubscriptionCard
            title="Premium"
            subtitle="VIP Support"
            price={data.tier_3_subscription_price}
          >
            <div className="mt-4 w-full text-left">
              {/* Top row: One-time payment text and discount badge */}
              <div className="p-3 flex items-center bg-white bg-opacity-30 shadow-md rounded-lg">
                <span className="mr-4 text-xl">➕</span>
                <span className="text-sm font-bold">
                  ${data.project_with_subscription_price} One-Time Project Fee
                </span>
                <span className="inline-flex items-center justify-center rounded-lg bg-green-700 bg-opacity-60 font-bold ml-2 p-2 border border-transparent text-xs text-white transition-all shadow-sm">
                  {data.project_discount_percent}% Off
                </span>
              </div>
              <hr className="my-3 border-gray-300" />
              {/* Details section using semantic markup */}
              <div className="flex items-start">
                <div>
                  <span className="mr-2 text-xl mt-1">✔️</span>
                  <span className="text-sm"><strong>Everything in Standard plus:</strong></span>
                  <ul className="ml-4 mt-2 list-disc text-sm text-gray-700 font-bold">
                    <li>Assist in optimizing transaction forms, improving performance by up to 50%</li>
                    <li className="pt-2">Exclusive VIP Project Discounts</li>
                    <li className="pt-2">Monthly System Health Report</li>
                    <li className="pt-2">VIP access to Ben's personal phone number for emergencies</li>
                  </ul>
                </div>
              </div>
            </div>
            <CheckoutButton slug={data.slug} option='tier_3_subscription_price' subscriptionTitle='Premium Support Plan' buttonTitle="Subscribe" />
          </SubscriptionCard>
        </div>
      </div>
    </div>
  );
}

export default SubscriptionPlans;
