import React from 'react';
import CheckoutButton from './CheckoutButton';

function SingleProjectOption({ data }) {
  return (
    <div className="max-w-5xl mx-auto px-4 my-5 py-5">
      <div className="bg-white inset-shadow-lg bg-opacity-20 border border-dashed border-gray-400 rounded-lg p-6 mb-10">
        <h3 className="text-center text-2xl font-bold py-4 mb-6">
          Only Need This Project?
        </h3>
        {/* Project-Only Card */}
        <div className="p-4 flex flex-col items-center md:flex-row md:justify-between">
          <div>
            <p className="font-bold text-gray-600">
              Pay once for the project, no monthly fees.
            </p>
            <p className="text-gray-400">
              This option includes 30-days support for project automations.
            </p>
          </div>
          <div>
            <p className="text-2xl font-bold text-red-800">
              <strong>${data.project_only_price}</strong>
              <span className="ml-2 text-base line-through text-gray-600">
                ${data.project_with_subscription_price}
              </span>
            </p>
          </div>
          <CheckoutButton slug={data.slug} option={'project_only_price'} title="Purchase" />
        </div>
      </div>
    </div>
  );
}

export default SingleProjectOption;
