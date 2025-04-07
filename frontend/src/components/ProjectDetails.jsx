import React from 'react';

function ProjectDetails({ data }) {
  return (
    <div className="relative w-full mb-10">
      <div className="px-4 py-8 bg-white bg-opacity-40 shadow-lg">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold mb-4">{data.project_name}</h1>
          <h3 className="mb-2 font-bold">
            <strong>Prepared for:</strong> {data.company_name}
          </h3>
          <p className="mb-8 font-bold">
            <strong>Contact:</strong> {data.client_name}
          </p>
          <div>
            <h3 className="mb-1 font-bold"><strong>Project Description</strong></h3>
            <div
              className="prose mb-7"
              dangerouslySetInnerHTML={{ __html: data.project_summary }}
            />
          </div>
          <div>
            <h3 className="mb-1 font-bold"><strong>Objectives</strong></h3>
            <div className="prose mb-7" style={{ whiteSpace: 'pre-line' }}>
              {data.project_objectives}
            </div>
          </div>
        </div>
      </div>

      {/* SVG divider for a subtle, non-symmetrical curved bottom edge */}
      <div className="absolute bottom-0 left-0 w-full overflow-hidden leading-0">
        <svg
          className="relative block w-full h-16"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 1200 120"
          preserveAspectRatio="none"
        >
          <path
            d="M0,30 C300,50 900,10 1200,30 L1200,120 L0,120 Z"
            className="fill-white"
            fillOpacity="0.4"
          />
        </svg>
      </div>
    </div>
  );
}

export default ProjectDetails;
