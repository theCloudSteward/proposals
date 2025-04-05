import React from 'react';

function Summary({
  isProjectOnly,
  originalProjectPrice,
  finalProjectPrice,
  monthlyCost,
  activePlan
}) {
  return (
    <section className="max-w-5xl mx-auto px-4 my-8">
      <div className="bg-white p-6 rounded shadow">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">Summary</h3>

        {isProjectOnly ? (
          <>
            <p className="mb-2 text-gray-700">
              <strong>Option:</strong> Project Only
            </p>
            <p className="mb-2 text-gray-700">
              <strong>Project Price:</strong> $
              {originalProjectPrice.toFixed(2)}
            </p>
            <hr className="my-4" />
            <p className="text-lg text-gray-800">
              <strong>Monthly Fee:</strong> $0
            </p>
            <p className="text-lg text-gray-800">
              <strong>One-time Cost:</strong> $
              {originalProjectPrice.toFixed(2)}
            </p>
          </>
        ) : (
          <>
            <p className="mb-2 text-gray-700">
              <strong>Option:</strong> {activePlan?.label || 'N/A'} Subscription
              (20% off project)
            </p>
            <p className="mb-2 text-gray-700">
              <strong>Discounted Project Price:</strong> $
              {finalProjectPrice.toFixed(2)}
            </p>
            <p className="mb-2 text-gray-700">
              <strong>Monthly Fee:</strong> ${monthlyCost.toFixed(2)}
            </p>
            <hr className="my-4" />
            <p className="text-lg text-gray-800">
              <strong>Total Monthly Fee:</strong> ${monthlyCost.toFixed(2)}
            </p>
            <p className="text-lg text-gray-800">
              <strong>One-time Cost:</strong> $
              {finalProjectPrice.toFixed(2)}
            </p>
          </>
        )}
      </div>
    </section>
  );
}

export default Summary;
