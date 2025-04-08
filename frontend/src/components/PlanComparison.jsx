import React from 'react';

function PlanComparison({
  data,
  originalProjectPrice,
  setSelectedOption,
  selectedOption,
}) {
  return (
    <div className="my-5 py-5">
      <div className="max-w-5xl mx-auto px-4">
        <div className="bg-white bg-opacity-50 shadow-md rounded-lg p-6 mb-10">
          <h2 className="text-center text-3xl font-bold py-4 mb-6">
            Compare Plans
          </h2>
          {/* Plan Comparison Table */}
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-left">
              <thead>
                <tr>
                  <td className="p-4 bg-white rounded-tl-md bg-opacity-60 font-semibold text-gray-800"> Features</td>
                  <td className="p-3 m-3 text-xl bg-white bg-opacity-60 font-bold"><h3>Basic</h3></td>
                  <td className="p-3 m-3 text-xl bg-white bg-opacity-60 font-bold"><h3>Standard</h3></td>
                  <td className="p-3 m-3 text-xl bg-white rounded-r-md bg-opacity-60 font-bold"><h3>Premium</h3></td>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="p-4 bg-white bg-opacity-30">Monthly Fees</td>
                  <td className="p-4">
                    <p className="text-base font-bold text-gray-800">
                      ${data.tier_1_subscription_price}
                      <span className="text-xs text-gray-500">/month</span>
                    </p>
                  </td>
                  <td className="p-4">
                    <p className="text-base font-bold text-gray-800">
                      ${data.tier_2_subscription_price}
                      <span className="text-xs text-gray-500">/month</span>
                    </p>
                  </td>
                  <td className="p-4">
                     <p className="text-base font-bold text-gray-800">
                      ${data.tier_3_subscription_price}
                      <span className="text-xs text-gray-500">/month</span>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td className="p-4 bg-white bg-opacity-30">Project Price</td>
                  <td className="p-4 font-bold">${data.project_with_subscription_price} 
                    <span className="inline-flex items-center justify-center rounded-lg bg-green-700 bg-opacity-60 font-bold ml-2 p-2 border border-transparent text-xs text-white transition-all shadow-sm">
                      20% Off
                    </span>
                  </td>
                  <td className="p-4 font-bold">${data.project_with_subscription_price} 
                    <span className="inline-flex items-center justify-center rounded-lg bg-green-700 bg-opacity-60 font-bold ml-2 p-2 border border-transparent text-xs text-white transition-all shadow-sm">
                      20% Off
                    </span>
                  </td>
                  <td className="p-4 font-bold">${data.project_with_subscription_price} 
                    <span className="inline-flex items-center justify-center rounded-lg bg-green-700 bg-opacity-60 font-bold ml-2 p-2 border border-transparent text-xs text-white transition-all shadow-sm">
                      20% Off
                    </span>
                  </td>
                </tr>
                <tr>
                  <td className="p-4 bg-white bg-opacity-30">Support Priority</td>
                  <td className="p-4">Basic</td>
                  <td className="p-4">Standard</td>
                  <td className="p-4">Priority</td>
                </tr>
                <tr>
                  <td className="p-4 bg-white bg-opacity-30">USA-Based Tech Support</td>
                  <td className="p-4">✔</td>
                  <td className="p-4">✔</td>
                  <td className="p-4">✔</td>
                </tr>
                <tr>
                  <td className="p-4 bg-white bg-opacity-30">Latest SuiteScript 2.1 Technology</td>
                  <td className="p-4">✔</td>
                  <td className="p-4">✔</td>
                  <td className="p-4">✔</td>
                </tr>
                <tr>
                  <td className="p-4 bg-white bg-opacity-30">24/7 Error Monitoring</td>
                  <td className="p-4">✔</td>
                  <td className="p-4">✔</td>
                  <td className="p-4">✔</td>
                </tr>
                <tr>
                  <td className="p-4 bg-white bg-opacity-30">100% Uptime for Cloud Steward Automations</td>
                  <td className="p-4">✔</td>
                  <td className="p-4">✔</td>
                  <td className="p-4">✔</td>
                </tr>
                <tr>
                  <td className="p-4 bg-white rounded-b-md bg-opacity-30">100% Uptime for All System-Critical SuiteScripts and Workflows</td>
                  <td className="p-4">—</td>
                  <td className="p-4">✔</td>
                  <td className="p-4">✔</td>
                </tr>
                <tr>
                  <td className="p-4 bg-white rounded-b-md bg-opacity-30">Optimize Transaction Form Performance</td>
                  <td className="p-4">—</td>
                  <td className="p-4">—</td>
                  <td className="p-4">✔</td>
                </tr>
                <tr>
                  <td className="p-4 bg-white rounded-b-md bg-opacity-30">Exclusive VIP Discounts for Future Projects</td>
                  <td className="p-4">—</td>
                  <td className="p-4">—</td>
                  <td className="p-4">✔</td>
                </tr>
                <tr>
                  <td className="p-4 bg-white rounded-b-md bg-opacity-30">Monthly System Health Report</td>
                  <td className="p-4">—</td>
                  <td className="p-4">—</td>
                  <td className="p-4">✔</td>
                </tr>
                <tr>
                  <td className="p-4 bg-white rounded-b-md bg-opacity-30">VIP Access to Ben's Personal Phone for Emergencies</td>
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
