import React, { useState } from 'react';

function SubscriptionCard({
  title,
  subtitle,
  price,
  option,
  selectedOption,
  setSelectedOption,
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
        <button
          onClick={() => setSelectedOption(option)}
          className={`my-8 py-2 px-4 rounded transition-colors border ${
            selectedOption === option
              ? 'bg-[#435B45] border-[#435B45] text-white hover:bg-[#3A513C]'
              : 'bg-white text-gray-800 hover:bg-gray-200'
          }`}
        >
          {selectedOption === option ? 'Selected' : 'Subscribe'}
        </button>
      </div>
    </div>
  );
}

function SubscriptionPlans({
  data,
  originalProjectPrice,
  setSelectedOption,
  selectedOption,
}) {
  return (
    <div className="my-10 py-10">
      <h2 className="max-w-5xl mx-auto text-center px-4 font-bold mb-4">Membership Pricing</h2>
      <div className="max-w-5xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Basic Card with extra details */}
          <SubscriptionCard
            title="Basic"
            subtitle="A Fresh Start"
            price={data.tier_1_subscription_price}
            option="basic"
            selectedOption={selectedOption}
            setSelectedOption={setSelectedOption}
          >
            <div className="mt-4 w-full text-left">
              <div className="flex items-center">
                <span className="mr-2 text-xl">➕</span>
                <span className="text-sm font-bold">
                  $800 One-Time Payment for Project 
                </span>
             <div class="flex justify-center items-center rounded-lg bg-opacity-70 bg-red-600 py-0.5 px-1 border border-transparent text-sm text-white transition-all shadow-md">
              20% Off
            </div>
              </div>
              <hr className="my-3 border-gray-300" />
              <div className="flex items-center">
                <span className="mr-2 text-xl">✔️</span>
                <span className="text-sm">Maintain 100% Uptime for All Cloud Steward Customizations</span>
              </div>
              <hr className="my-3 border-gray-300" />
              <div className="flex items-center">
                <span className="mr-2 text-xl">✔️</span>
                <span className="text-sm">Resolve Cloud Steward Script Errors within Hours for Free</span>
              </div>
            </div>
          </SubscriptionCard>

          {/* Standard Card */}
          <SubscriptionCard
            title="Standard"
            subtitle="Full System Maintenance"
            price={data.tier_2_subscription_price}
            option="standard"
            selectedOption={selectedOption}
            setSelectedOption={setSelectedOption}
          />

          {/* Premium Card */}
          <SubscriptionCard
            title="Premium"
            subtitle="VIP Support"
            price={data.tier_3_subscription_price}
            option="premium"
            selectedOption={selectedOption}
            setSelectedOption={setSelectedOption}
          />
        </div>
      </div>
    </div>
  );
}

export default SubscriptionPlans;
