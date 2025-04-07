import React from 'react';

function ProjectDetails({data}) {
  return (
      <div className="max-w-5xl mx-auto px-4 py-8">
          <h2 className="text-2xl font-bold mb-4">
            {data.project_name}
          </h2>
          <h3 className="mb-2 font-bold">
            <strong>Prepared for:</strong> {data.company_name}
          </h3>
          <p className="mb-9 font-bold">
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
            <div
              className="prose mb-7"
              style={{ whiteSpace: 'pre-line' }} // This honors line breaks in plain text
            >
              {data.project_objectives}
            </div>
          </div>
      </div>
  );
}

export default ProjectDetails;