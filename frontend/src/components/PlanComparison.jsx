import React from 'react';

function PlanComparison({
  data,
  originalProjectPrice,
  setSelectedOption,
  selectedOption
}) {
  // Example tier prices (keeping the same as your original code)
  const basicPrice = originalProjectPrice * 0.8; // 20% less than original
  const standardPrice = originalProjectPrice;    // Same as original
  const premiumPrice = originalProjectPrice * 1.5; // 50% more than original

  return (
    <section
      className="py-12"
    >
      <div className="max-w-5xl mx-auto px-4">
        <div className="bg-white shadow-md rounded p-6 mb-10">
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

          {/* Plan Comparison Table */}
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-left">
              <thead>
                <tr>
                  <th className="p-4"></th>
                  <th className="p-4 text-center">
                    <h3 className="text-xl font-semibold text-gray-800">Basic</h3>
                    <p className="text-2xl font-bold text-gray-800">
                      ${basicPrice.toFixed(2)}
                    </p>
                    <button
                      onClick={() => setSelectedOption('basic')}
                      className={`mt-2 py-2 px-4 rounded transition-colors border 
                        ${
                          selectedOption === 'basic'
                            ? 'bg-[#435B45] border-[#435B45] text-white hover:bg-[#3A513C]'
                            : 'bg-white text-gray-800 hover:bg-gray-200'
                        }`}
                    >
                      {selectedOption === 'basic' ? 'Selected' : 'Select'}
                    </button>
                  </th>
                  <th className="p-4 text-center">
                    <h3 className="text-xl font-semibold text-gray-800">Standard</h3>
                    <p className="text-2xl font-bold text-gray-800">
                      ${standardPrice.toFixed(2)}
                    </p>
                    <button
                      onClick={() => setSelectedOption('standard')}
                      className={`mt-2 py-2 px-4 rounded transition-colors border 
                        ${
                          selectedOption === 'standard'
                            ? 'bg-[#435B45] border-[#435B45] text-white hover:bg-[#3A513C]'
                            : 'bg-white text-gray-800 hover:bg-gray-200'
                        }`}
                    >
                      {selectedOption === 'standard' ? 'Selected' : 'Select'}
                    </button>
                  </th>
                  <th className="p-4 text-center">
                    <h3 className="text-xl font-semibold text-gray-800">Premium</h3>
                    <p className="text-2xl font-bold text-gray-800">
                      ${premiumPrice.toFixed(2)}
                    </p>
                    <button
                      onClick={() => setSelectedOption('premium')}
                      className={`mt-2 py-2 px-4 rounded transition-colors border 
                        ${
                          selectedOption === 'premium'
                            ? 'bg-[#435B45] border-[#435B45] text-white hover:bg-[#3A513C]'
                            : 'bg-white text-gray-800 hover:bg-gray-200'
                        }`}
                    >
                      {selectedOption === 'premium' ? 'Selected' : 'Select'}
                    </button>
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
    </section>
  );
}

export default PlanComparison;