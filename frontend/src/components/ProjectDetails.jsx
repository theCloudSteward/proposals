import React from 'react';

function ProjectDetails({data}) {
  return (
      <div className="max-w-5xl mx-auto px-4 py-8">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            {data.project_name}
          </h2>
          <h3 className="text-gray-700 mb-2">
            {data.company_name}
          </h3>
          <p className="text-gray-700 mb-2">
            <strong>Contact:</strong> {data.client_name}
          </p>
          <div
            className="prose mb-6 text-gray-800"
            dangerouslySetInnerHTML={{ __html: data.project_summary }}
          />
          <p className="text-gray-700 mb-2">
            <strong>Objectives</strong> {data.project_objectives}
          </p>
      </div>
  );
}

export default ProjectDetails;