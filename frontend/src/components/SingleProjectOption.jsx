import React from 'react';

function SingleProjectOption({
  originalProjectPrice,
  isProjectOnly,
  setSelectedOption,
}) {
  return (
    <section className="py-12" style={{ backgroundColor: '#596E5C' }}>
      <div className="max-w-5xl mx-auto px-4">
        <div className="bg-white shadow-md rounded p-6 mb-10">
          {/* Project-Only Card */}
          <div className="bg-gray-100 p-4 rounded shadow-inner flex flex-col items-center md:flex-row md:justify-between">
            <div>
              <h3 className="text-xl font-semibold text-gray-800">
                Project Only
              </h3>
              <p className="text-gray-600">
                Pay once for the project, no monthly fees.
              </p>
            </div>
            <div className="mt-4 md:mt-0">
              <p className="text-2xl font-bold text-gray-800">
                ${originalProjectPrice.toFixed(2)}
              </p>
            </div>
            <button
              onClick={() => setSelectedOption('project-only')}
              className={`mt-4 md:mt-0 ml-0 md:ml-4 py-2 px-4 rounded transition-colors border 
                ${
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
    </section>
  );
}

export default SingleProjectOption;
