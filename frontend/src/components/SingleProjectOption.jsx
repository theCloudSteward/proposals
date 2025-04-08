import React from 'react';

function SingleProjectOption({
  data,
  originalProjectPrice,
  isProjectOnly,
  setSelectedOption,
}) {
  return (
    <div className="max-w-5xl mx-auto my-5 py-5">
      <div className="bg-white bg-opacity-10 border border-dotted border-gray-300 rounded-lg p-6 mb-10">
        <h2 className="text-center px-4 font-bold mb-8">Project Only?</h2>
        {/* Project-Only Card */}
        <div className="p-4 flex flex-col items-center md:flex-row md:justify-between">
          <div>
            <p className="text-gray-600">
              Pay once for the project, no monthly fees.
            </p>
          </div>
          <div className="mt-4 md:mt-0">
            <p className="text-2xl font-bold text-gray-800">
              ${data.project_only_price}
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
