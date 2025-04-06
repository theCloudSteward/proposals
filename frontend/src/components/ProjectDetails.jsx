import React from 'react';

function ProjectDetails({data}) {
  return (
      <div className="max-w-5xl mx-auto px-4 py-8">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            {data.project_name}
          </h2>
          <h3 className="mb-2 font-bold">
            <strong>Prepared for:</strong> {data.company_name}
          </h3>
          <p className="mb-2 font-bold">
            <strong>Contact:</strong> {data.client_name}
          </p>
          <div>
            <h3 className="mb-2 font-bold"><strong>Project Description</strong></h3>
            <div
              className="prose mb-6 text-gray-800"
              dangerouslySetInnerHTML={{ __html: data.project_summary }}
            />
          </div>
          <div>
            <h3 className="mb-2 font-bold"><strong>Objectives</strong></h3>
            <div
              className="prose mb-6 text-gray-800"
              dangerouslySetInnerHTML={{ __html: data.project_objectives }}
            />
          </div>
      </div>
  );
}

export default ProjectDetails;