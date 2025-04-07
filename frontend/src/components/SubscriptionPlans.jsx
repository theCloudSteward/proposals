import React from 'react';

function SubscriptionPlans({
  data,
  originalProjectPrice,
  setSelectedOption,
  selectedOption
}) {
  return (
    <div className="mb-4">
      <h2 className="max-w-5xl mx-auto px-4 font-bold mb-4">Membership Pricing</h2>
      <div className="max-w-5xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Tier 1: Basic */}
          <div className="bg-white bg-opacity-50 shadow-md rounded p-6 flex flex-col items-center">
            {/* Gradient Header Box */}
            <div 
              className="w-full p-3 text-center rounded-t" 
              style={{ background: 'linear-gradient(142deg, rgba(253,240,249,1) 0%, rgba(181,218,247,1) 100%)' }}
            >
              <h3 className="text-xl font-semibold text-gray-800">Basic</h3>
              <p className="text-gray-600">A Fresh Start</p>
            </div>
            
            {/* Price Display */}
            <div className="w-full text-center mt-4">
              <p className="text-3xl font-bold text-gray-800">
                ${data.tier_1_subscription_price}
                <span className="text-xl text-gray-600">/month</span>
              </p>
            </div>
            
            {/* Extra details for Basic card */}
            <div className="mt-2 w-full text-left">
              <div className="flex items-center">
                <span className="mr-2 text-lg">➕</span>
                <span className="text-sm">$800 Single-Time Payment for Project (20% Off)</span>
              </div>
              <hr className="my-2 border-gray-300" />
              <div className="flex items-center">
                <span className="mr-2 text-lg">✔️</span>
                <span className="text-sm">Maintain 100% Uptime for All Cloud Steward Customizations</span>
              </div>
              <hr className="my-2 border-gray-300" />
              <div className="flex items-center">
                <span className="mr-2 text-lg">✔️</span>
                <span className="text-sm">Resolve Cloud Steward Script Errors within Hours for Free</span>
              </div>
            </div>
            
            <button
              onClick={() => setSelectedOption('basic')}
              className={`mt-4 py-2 px-4 rounded transition-colors border ${
                selectedOption === 'basic'
                  ? 'bg-[#435B45] border-[#435B45] text-white hover:bg-[#3A513C]'
                  : 'bg-white text-gray-800 hover:bg-gray-200'
              }`}
            >
              {selectedOption === 'basic' ? 'Selected' : 'Subscribe'}
            </button>
          </div>
          
          {/* Tier 2: Standard */}
          <div className="bg-white bg-opacity-60 shadow-md rounded p-6 flex flex-col items-center">
            {/* Gradient Header Box */}
            <div 
              className="w-full p-3 text-center rounded-t" 
              style={{ background: 'linear-gradient(142deg, rgba(253,240,249,1) 0%, rgba(181,218,247,1) 100%)' }}
            >
              <h3 className="text-xl font-semibold text-gray-800">Standard</h3>
              <p className="text-gray-600">Full System Maintenance</p>
            </div>
            
            {/* Price Display */}
            <div className="w-full text-center mt-4">
              <p className="text-3xl font-bold text-gray-800">
                ${data.tier_2_subscription_price}
                <span className="text-xl text-gray-600">/month</span>
              </p>
            </div>
            
            <button
              onClick={() => setSelectedOption('standard')}
              className={`mt-4 py-2 px-4 rounded transition-colors border ${
                selectedOption === 'standard'
                  ? 'bg-[#435B45] border-[#435B45] text-white hover:bg-[#3A513C]'
                  : 'bg-white text-gray-800 hover:bg-gray-200'
              }`}
            >
              {selectedOption === 'standard' ? 'Selected' : 'Subscribe'}
            </button>
          </div>
          
          {/* Tier 3: Premium */}
          <div className="bg-white bg-opacity-50 shadow-md rounded p-6 flex flex-col items-center">
            {/* Gradient Header Box */}
            <div 
              className="w-full p-3 text-center rounded-t" 
              style={{ background: 'linear-gradient(142deg, rgba(253,240,249,1) 0%, rgba(181,218,247,1) 100%)' }}
            >
              <h3 className="text-xl font-semibold text-gray-800">Premium</h3>
              <p className="text-gray-600">VIP Support</p>
            </div>
            
            {/* Price Display */}
            <div className="w-full text-center mt-4">
              <p className="text-3xl font-bold text-gray-800">
                ${data.tier_3_subscription_price}
                <span className="text-xl text-gray-600">/month</span>
              </p>
            </div>
            
            <button
              onClick={() => setSelectedOption('premium')}
              className={`mt-4 py-2 px-4 rounded transition-colors border ${
                selectedOption === 'premium'
                  ? 'bg-[#435B45] border-[#435B45] text-white hover:bg-[#3A513C]'
                  : 'bg-white text-gray-800 hover:bg-gray-200'
              }`}
            >
              {selectedOption === 'premium' ? 'Selected' : 'Subscribe'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SubscriptionPlans;
