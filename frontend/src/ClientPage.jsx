// src/ClientPage.jsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Helmet } from "react-helmet";

function ClientPage() {
  const { slug } = useParams();
  const [data, setData] = useState(null);
  const [notFound, setNotFound] = useState(false);

  // The user can pick "project-only" or one of the subscription plans below.
  const [selectedOption, setSelectedOption] = useState("project-only");

  // Subscription plans
  const SUBSCRIPTION_PLANS = [
    {
      id: "tier1",
      label: "Tier 1",
      monthlyPrice: 299,
      discountPercent: 20, // 20% discount on project price
      features: [
        "INDIA-based tech support",
        "Free ongoing maintenance for all Cloud Steward scripts",
        "Resolve script errors within hours",
        "100% uptime for Cloud Steward scripts",
        "Peace of mind, knowing that all Cloud Steward scripts are maintained",
      ],
    },
    {
      id: "tier2",
      label: "Tier 2",
      monthlyPrice: 1750,
      discountPercent: 20,
      features: [
        "Everything in Tier 1, plus...",
        "Monitor ALL script errors across system",
        "Resolve ANY script errors for free",
        "24/7 VIP tech support access",
        "USA-based tech support",
        "Access to Ben's personal phone number for emergencies",
        "Peace of mind, knowing that all system scripts are maintained",
      ],
    },
  ];

  // Fetch data for the current slug
  useEffect(() => {
    fetch(`/api/pages/${slug}/`)
      .then((res) => {
        if (res.status === 404) {
          setNotFound(true);
          return null;
        }
        return res.json();
      })
      .then((pageData) => {
        if (pageData) setData(pageData);
      })
      .catch((err) => console.error(err));
  }, [slug]);

  if (notFound) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100 font-sans">
        <h1 className="text-3xl font-bold text-red-600">
          This page does not exist or has expired.
        </h1>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 font-sans">
        <p className="text-lg text-gray-700">Loading...</p>
      </div>
    );
  }

  // Original project price from server
  const originalProjectPrice = parseFloat(data.project_price) || 0;

  // Check if the user selected "project-only" or a subscription plan
  const isProjectOnly = selectedOption === "project-only";
  const activePlan =
    SUBSCRIPTION_PLANS.find((p) => p.id === selectedOption) || null;

  // If they selected a subscription plan, discount the project by that plan’s discount
  let finalProjectPrice = originalProjectPrice;
  let monthlyCost = 0;

  if (!isProjectOnly && activePlan) {
    const discount = (activePlan.discountPercent || 0) / 100; // 20% => 0.2
    finalProjectPrice = originalProjectPrice * (1 - discount);
    monthlyCost = activePlan.monthlyPrice;
  }

  // Dynamically set the browser tab title: "{company_name} Proposal"
  const pageTitle = `${data.company_name} Proposal`;

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      <Helmet>
        <title>{pageTitle}</title>
      </Helmet>

      {/* Header */}
      <header className="w-full bg-white py-6 shadow-sm">
        <div className="max-w-6xl mx-auto px-4">
          <h1 className="text-3xl font-extrabold text-gray-800 tracking-tight">
            Cloud Steward
          </h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow">
        {/* Project / Client Details & Project-Only Option */}
        <section className="py-12" style={{ backgroundColor: "#596E5C" }}>
          <div className="max-w-5xl mx-auto px-4">
            <div className="bg-white shadow-md rounded p-6 mb-10">
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
                <strong>Regular Project Price:</strong>{" "}
                ${originalProjectPrice.toFixed(2)}
              </p>

              {/* If `project_details` is rich HTML */}
              <div
                className="prose mb-6 text-gray-800"
                dangerouslySetInnerHTML={{ __html: data.project_details }}
              />

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
                  onClick={() => setSelectedOption("project-only")}
                  className={`mt-4 md:mt-0 ml-0 md:ml-4 py-2 px-4 rounded transition-colors border 
                    ${
                      isProjectOnly
                        ? "bg-[#435B45] border-[#435B45] text-white hover:bg-[#3A513C]"
                        : "bg-white text-gray-800 hover:bg-gray-200"
                    }`}
                >
                  {isProjectOnly ? "Selected" : "Select"}
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Subscription Plans */}
        <section className="bg-gray-900 text-white py-16">
          <div className="max-w-6xl mx-auto px-4 text-center">
            <h2 className="text-4xl font-extrabold mb-4 tracking-tight">
              Become a Cloud Steward Member
            </h2>
            <p className="text-gray-300 mb-8 max-w-xl mx-auto">
              Select a subscription plan below, and we’ll knock 20% off all
              projects for as long as you're subscribed.
            </p>

            <div className="bg-[#435B45] rounded-lg shadow-lg p-6 my-10 inline-block">
              <p className="text-center">
                <span className="text-sm font-bold text-red-200 line-through block">
                  ${originalProjectPrice.toFixed(2)}
                </span>
                <span className="text-3xl font-bold text-white">
                  {(originalProjectPrice * (1 - 0.2)).toFixed(2)}
                </span>
              </p>
              <p className="mt-2 text-sm text-white/80">
                20% off while subscribed!
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {SUBSCRIPTION_PLANS.map((plan) => {
                const isActive = plan.id === selectedOption;
                return (
                  <div
                    key={plan.id}
                    className="bg-gray-800 rounded-lg shadow-lg p-6 flex flex-col items-center"
                  >
                    <h3 className="text-2xl font-bold mb-2">{plan.label}</h3>
                    <p className="text-4xl font-bold mb-2">
                      ${plan.monthlyPrice}
                    </p>
                    <p className="mb-4 text-gray-400">/ month</p>

                    <button
                      onClick={() => setSelectedOption(plan.id)}
                      className={`py-2 px-4 rounded transition-colors border 
                        ${
                          isActive
                            ? "bg-[#596E5C] border-[#596E5C] text-white hover:bg-[#4F604F]"
                            : "bg-white text-gray-800 hover:bg-gray-200"
                        }
                      `}
                    >
                      {isActive ? "Selected" : "Select"}
                    </button>

                    <ul className="mt-6 text-gray-300 text-left space-y-1">
                      {plan.features.map((feat, i) => (
                        <li key={i}>✓ {feat}</li>
                      ))}
                    </ul>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* Summary Section */}
        <section className="max-w-5xl mx-auto px-4 my-8">
          <div className="bg-white p-6 rounded shadow">
            <h3 className="text-xl font-semibold mb-4 text-gray-800">
              Summary
            </h3>
            {isProjectOnly ? (
              <>
                <p className="mb-2 text-gray-700">
                  <strong>Option:</strong> Project Only
                </p>
                <p className="mb-2 text-gray-700">
                  <strong>Project Price:</strong>{" "}
                  ${originalProjectPrice.toFixed(2)}
                </p>
                <hr className="my-4" />
                <p className="text-lg text-gray-800">
                  <strong>Monthly Fee:</strong> $0
                </p>
                <p className="text-lg text-gray-800">
                  <strong>One-time Cost:</strong>{" "}
                  ${originalProjectPrice.toFixed(2)}
                </p>
              </>
            ) : (
              <>
                <p className="mb-2 text-gray-700">
                  <strong>Option:</strong> {activePlan?.label || "N/A"}{" "}
                  Subscription (20% off project)
                </p>
                <p className="mb-2 text-gray-700">
                  <strong>Discounted Project Price:</strong>{" "}
                  ${finalProjectPrice.toFixed(2)}
                </p>
                <p className="mb-2 text-gray-700">
                  <strong>Monthly Fee:</strong> ${monthlyCost.toFixed(2)}
                </p>
                <hr className="my-4" />
                <p className="text-lg text-gray-800">
                  <strong>Total Monthly Fee:</strong> ${monthlyCost.toFixed(2)}
                </p>
                <p className="text-lg text-gray-800">
                  <strong>One-time Cost:</strong> ${finalProjectPrice.toFixed(2)}
                </p>
              </>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default ClientPage;
