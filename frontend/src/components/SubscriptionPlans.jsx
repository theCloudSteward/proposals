import React from 'react';

function SubscriptionPlans({
  data,
  originalProjectPrice,
  isProjectOnly,
  setSelectedOption,
  selectedOption
}) {
  // Example tier prices (you can adjust these as needed)
  const basicPrice = originalProjectPrice * 0.8; // 20% less than original
  const standardPrice = originalProjectPrice;    // Same as original
  const premiumPrice = originalProjectPrice * 1.5; // 50% more than original

  return (
    <section
      className="py-12"
      style={{
        background: 'rgb(253,240,249)',
        background: 'linear-gradient(142deg, rgba(253,240,249,1) 0%, rgba(181,218,247,1) 100%)',
      }}
    >
      <div className="max-w-5xl mx-auto px-4">
        <div className="bg-white shadow-md rounded p-6 mb-10">
          {/* Project Details Section */}
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            {data.project_name}
          </h2>
          <p className="text-gray-700 mb-2">
            <strong>Client:</strong> {data.client_name}
          </p>
          <p className="text-gray-700 mb-2">
            <strong>Company:</strong> {data.company_name}
          </p>
          <p className="text-gray-700 mb-2">
            <strong>Regular Project Price:</strong> $
            {originalProjectPrice.toFixed(2)}
          </p>

          <div
            className="prose mb-6 text-gray-800"
            dangerouslySetInnerHTML={{ __html: data.project_details }}
          />

          {/* Tier 1: Basic */}
          <div className="bg-gray-100 p-4 rounded shadow-inner flex flex-col items-center md:flex-row md:justify-between mb-6">
            <div>
              <h3 className="text-xl font-semibold text-gray-800">Basic</h3>
              <p className="text-gray-600">
                Core project features, one-time payment.
              </p>
            </div>
            <div className="mt-4 md:mt-0">
              <p className="text-2xl font-bold text-gray-800">
                ${basicPrice.toFixed(2)}
              </p>
            </div>
            <button
              onClick={() => setSelectedOption('basic')}
              className={`mt-4 md:mt-0 ml-0 md:ml-4 py-2 px-4 rounded transition-colors border 
                ${
                  selectedOption === 'basic'
                    ? 'bg-[#435B45] border-[#435B45] text-white hover:bg-[#3A513C]'
                    : 'bg-white text-gray-800 hover:bg-gray-200'
                }`}
            >
              {selectedOption === 'basic' ? 'Selected' : 'Select'}
            </button>
          </div>

          {/* Tier 2: Standard */}
          <div className="bg-gray-100 p-4 rounded shadow-inner flex flex-col items-center md:flex-row md:justify-between mb-6">
            <div>
              <h3 className="text-xl font-semibold text-gray-800">Standard</h3>
              <p className="text-gray-600">
                Full project scope, no monthly fees.
              </p>
            </div>
            <div className="mt-4 md:mt-0">
              <p className="text-2xl font-bold text-gray-800">
                ${standardPrice.toFixed(2)}
              </p>
            </div>
            <button
              onClick={() => setSelectedOption('standard')}
              className={`mt-4 md:mt-0 ml-0 md:ml-4 py-2 px-4 rounded transition-colors border 
                ${
                  selectedOption === 'standard'
                    ? 'bg-[#435B45] border-[#435B45] text-white hover:bg-[#3A513C]'
                    : 'bg-white text-gray-800 hover:bg-gray-200'
                }`}
            >
              {selectedOption === 'standard' ? 'Selected' : 'Select'}
            </button>
          </div>

          {/* Tier 3: Premium */}
          <div className="bg-gray-100 p-4 rounded shadow-inner flex flex-col items-center md:flex-row md:justify-between">
            <div>
              <h3 className="text-xl font-semibold text-gray-800">Premium</h3>
              <p className="text-gray-600">
                Enhanced features, priority support, one-time payment.
              </p>
            </div>
            <div className="mt-4 md:mt-0">
              <p className="text-2xl font-bold text-gray-800">
                ${premiumPrice.toFixed(2)}
              </p>
            </div>
            <button
              onClick={() => setSelectedOption('premium')}
              className={`mt-4 md:mt-0 ml-0 md:ml-4 py-2 px-4 rounded transition-colors border 
                ${
                  selectedOption === 'premium'
                    ? 'bg-[#435B45] border-[#435B45] text-white hover:bg-[#3A513C]'
                    : 'bg-white text-gray-800 hover:bg-gray-200'
                }`}
            >
              {selectedOption === 'premium' ? 'Selected' : 'Select'}
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}

export default SubscriptionPlans;