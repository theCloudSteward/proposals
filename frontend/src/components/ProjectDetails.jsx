import React from 'react';

function ProjectDetails({ data }) {
  return (
    <div
      className="w-full px-4 py-8 bg-white bg-opacity-40 shadow-lg mb-10"
      style={{
        clipPath: 'ellipse(150% 100% at 50% 100%)',
      }}
    >
      <div className="max-w-5xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">{data.project_name}</h1>
        <h3 className="mb-2 font-bold">
          <strong>Prepared for:</strong> {data.company_name}
        </h3>
        <p className="mb-8 font-bold">
          <strong>Contact:</strong> {data.client_name}
        </p>
        <div>
          <h3 className="mb-1 font-bold">
            <strong>Project Description</strong>
          </h3>
          <div
            className="prose mb-7"
            dangerouslySetInnerHTML={{ __html: data.project_summary }}
          />
        </div>
        <div>
          <h3 className="mb-1 font-bold">
            <strong>Objectives</strong>
          </h3>
          <div className="prose mb-7" style={{ whiteSpace: 'pre-line' }}>
            {data.project_objectives}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProjectDetails;
