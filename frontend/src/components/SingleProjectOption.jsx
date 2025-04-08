import React from 'react';

function SingleProjectOption({
  data,
  originalProjectPrice,
  isProjectOnly,
  setSelectedOption,
}) {
  // Calculate the actual and discounted price. For example, if project_only_price is 2500,
  // the discounted price is 20% less (i.e., 2000).
  const actualPrice = parseFloat(data.project_only_price);
  const discountedPrice = actualPrice * 0.8;

  return (
    <div className="max-w-5xl mx-auto my-5 py-5">
      <div className="bg-white bg-opacity-30 border border-dashed border-gray-800 rounded-lg p-6 mb-10">
        <h3 className="text-center text-3xl font-bold py-4 mb-6">
          Compare Plans
        </h3>
        {/* Project-Only Card */}
        <div className="p-4 flex flex-col items-center md:flex-row md:justify-between">
          <div>
            <p className="font-bold text-gray-600">
              Pay once for the project, no monthly fees.
            </p>
          </div>
          <div className="mt-4 md:mt-0">
            <p className="text-2xl font-bold text-gray-800">
              ${actualPrice}
              <span className="ml-2 text-base line-through text-red-600">
                ${discountedPrice.toFixed(0)}
              </span>
            </p>
          </div>
          <button
            onClick={() => setSelectedOption('project-only')}
            className={`mt-4 md:mt-0 ml-0 md:ml-4 py-2 px-4 rounded transition-colors border ${
              isProjectOnly
                ? 'bg-[#435B45] border-[#435B45] text-white hover:bg-[#3A513C]'
                : 'bg-white text-gray-800 hover:bg-gray-200'
            }`}
          >
            {isProjectOnly ? 'Selected' : 'Select'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default SingleProjectOption;
