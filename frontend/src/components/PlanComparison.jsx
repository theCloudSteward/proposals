import React from 'react';

function PlanComparison({
  data,
  originalProjectPrice,
  setSelectedOption,
  selectedOption
}) {
  return (
    <div className="my-5 py-5">
      <div className="max-w-5xl mx-auto px-4">
        <div className="bg-white bg-opacity-50 shadow-md rounded-lg p-6 mb-10">
          <h2 className="mx-auto text-center px-4 font-bold m-8">Compare Plans</h2>
          {/* Plan Comparison Table */}
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-left">
              <thead>
                <tr>
                  <th className="p-4"></th>
                  <th className="p-4">
                    <h3 className="mx-auto p-4 font-bold m-6">Basic</h3>
                    <div className="w-full">
                      <p className="text-3xl font-bold text-gray-800">
                        ${data.tier_1_subscription_price}
                        <span className="text-base text-gray-500">/month</span>
                      </p>
                    </div>
                  </th>
                  <th className="p-4">
                    <h3 className="mx-auto p-4 font-bold m-6">Standard</h3>
                    <div className="w-full">
                      <p className="text-3xl font-bold text-gray-800">
                        ${data.tier_2_subscription_price}
                        <span className="text-base text-gray-500">/month</span>
                      </p>
                    </div>
                  </th>
                  <th className="p-4">
                    <h3 className="mx-auto p-4 font-bold m-6">Premium</h3>
                    <div className="w-full">
                      <p className="text-3xl font-bold text-gray-800">
                        ${data.tier_3_subscription_price}
                        <span className="text-base text-gray-500">/month</span>
                      </p>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody>
                {/* Features Section */}
                <tr className="bg-gray-100">
                  <td className="p-4 font-semibold text-gray-800">Features</td>
                  <td className="p-4"></td>
                  <td className="p-4"></td>
                  <td className="p-4"></td>
                </tr>
                <tr>
                  <td className="p-4">Project Scope</td>
                  <td className="p-4">Core features</td>
                  <td className="p-4">Full scope</td>
                  <td className="p-4">Enhanced features</td>
                </tr>
                <tr>
                  <td className="p-4">Payment Type</td>
                  <td className="p-4">One-time</td>
                  <td className="p-4">One-time</td>
                  <td className="p-4">One-time</td>
                </tr>
                <tr>
                  <td className="p-4">Monthly Fees</td>
                  <td className="p-4">None</td>
                  <td className="p-4">None</td>
                  <td className="p-4">None</td>
                </tr>
                <tr>
                  <td className="p-4">Support Level</td>
                  <td className="p-4">Basic</td>
                  <td className="p-4">Standard</td>
                  <td className="p-4">Priority</td>
                </tr>
                <tr>
                  <td className="p-4">Custom Features</td>
                  <td className="p-4">—</td>
                  <td className="p-4">—</td>
                  <td className="p-4">✔</td>
                </tr>
                <tr>
                  <td className="p-4">Team Collaboration</td>
                  <td className="p-4">—</td>
                  <td className="p-4">—</td>
                  <td className="p-4">✔</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PlanComparison;