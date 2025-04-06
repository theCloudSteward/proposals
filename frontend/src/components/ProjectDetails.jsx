import React from 'react';

function ProjectDetails({
  data,
  originalProjectPrice,
  isProjectOnly,
  setSelectedOption,
  selectedOption
}) {
  return (
      <div className="max-w-5xl mx-auto px-4 py-8">
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

          {/* Project-Only Text Directly on Page */}
          <div>
            <h3 className="text-xl font-semibold text-gray-800">
              Project Only
            </h3>
            <p className="text-gray-600">
              Pay once for the project, no monthly fees.
            </p>
            <p className="text-2xl font-bold text-gray-800 mt-4">
              ${originalProjectPrice.toFixed(2)}
            </p>
            <button
              onClick={() => setSelectedOption('project-only')}
              className={`mt-4 py-2 px-4 rounded transition-colors border 
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
  );
}

export default ProjectDetails;