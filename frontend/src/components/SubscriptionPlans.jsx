import React from 'react';

function SubscriptionPlans({
  data,
  originalProjectPrice,
  setSelectedOption,
  selectedOption
}) {
  return (
      <div>
        <h2 className="text-2xl font-bold mb-4">Membership Pricing</h2>
        <div className="max-w-5xl mx-auto px-4 py-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Tier 1: Basic */}
            <div className="bg-white shadow-md rounded p-6 flex flex-col items-center">
              <div>
                <h3 className="text-xl font-semibold text-gray-800">Basic</h3>
                <p className="text-gray-600">
                  A Fresh Start
                </p>
              </div>
              <div className="mt-4">
                <p className="text-2xl font-bold text-gray-800">
                  ${data.tier_1_subscription_price}
                </p>
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
            <div className="bg-white shadow-md rounded p-6 flex flex-col items-center">
              <div>
                <h3 className="text-xl font-semibold text-gray-800">Standard</h3>
                <p className="text-gray-600">
                  Full System Maintenance
                </p>
              </div>
              <div className="mt-4">
                <p className="text-2xl font-bold text-gray-800">
                  ${data.tier_2_subscription_price}
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
            <div className="bg-white shadow-md rounded p-6 flex flex-col items-center">
              <div>
                <h3 className="text-xl font-semibold text-gray-800">Premium</h3>
                <p className="text-gray-600">
                  VIP Support
                </p>
              </div>
              <div className="mt-4">
                <p className="text-2xl font-bold text-gray-800">
                  ${data.tier_1_subscription_price}
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