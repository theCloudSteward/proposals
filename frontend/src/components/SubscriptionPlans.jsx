import React from 'react';

function SubscriptionPlans({
  subscriptionPlans,
  originalProjectPrice,
  selectedOption,
  setSelectedOption
}) {
  return (
    <section className="bg-gray-900 text-white py-16">
      <div className="max-w-6xl mx-auto px-4 text-center">
        <h2 className="text-4xl font-extrabold mb-4 tracking-tight">
          Become a Cloud Steward Member
        </h2>
        <p className="text-gray-300 mb-8 max-w-xl mx-auto">
          Select a subscription plan below, and we’ll knock 20% off
          all projects for as long as you're subscribed.
        </p>

        <div className="bg-[#435B45] rounded-lg shadow-lg p-6 my-10 inline-block">
          <p className="text-center">
            <span className="text-sm font-bold text-red-200 line-through block">
              ${originalProjectPrice.toFixed(2)}
            </span>
            <span className="text-3xl font-bold text-white">
              {(originalProjectPrice * (1 - 0.2)).toFixed(2)}
            </span>
          </p>
          <p className="mt-2 text-sm text-white/80">
            20% off while subscribed!
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {subscriptionPlans.map((plan) => {
            const isActive = plan.id === selectedOption;
            return (
              <div
                key={plan.id}
                className="bg-gray-800 rounded-lg shadow-lg p-6 flex flex-col items-center"
              >
                <h3 className="text-2xl font-bold mb-2">{plan.label}</h3>
                <p className="text-4xl font-bold mb-2">${plan.monthlyPrice}</p>
                <p className="mb-4 text-gray-400">/ month</p>

                <button
                  onClick={() => setSelectedOption(plan.id)}
                  className={`py-2 px-4 rounded transition-colors border 
                    ${
                      isActive
                        ? 'bg-[#596E5C] border-[#596E5C] text-white hover:bg-[#4F604F]'
                        : 'bg-white text-gray-800 hover:bg-gray-200'
                    }
                  `}
                >
                  {isActive ? 'Selected' : 'Select'}
                </button>

                <ul className="mt-6 text-gray-300 text-left space-y-1">
                  {plan.features.map((feat, i) => (
                    <li key={i}>✓ {feat}</li>
                  ))}
                </ul>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

export default SubscriptionPlans;
