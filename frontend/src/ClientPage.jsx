// src/ClientPage.jsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Helmet } from "react-helmet";

// Our new sub-components
import ClientHeader from "./components/ClientHeader";
import ProjectDetails from "./components/ProjectDetails";
import SubscriptionPlans from "./components/SubscriptionPlans";
import Summary from "./components/Summary";

function ClientPage() {
  const { slug } = useParams();
  const [data, setData] = useState(null);
  const [notFound, setNotFound] = useState(false);
  const [selectedOption, setSelectedOption] = useState("project-only");

  // Subscription plans
  const SUBSCRIPTION_PLANS = [
    {
      id: "tier1",
      label: "Tier 1",
      monthlyPrice: 299,
      discountPercent: 20,
      features: [
        "USA-based tech support",
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

  // Fetch data
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

  const pageTitle = `${data.company_name} Proposal`;

  // Price calculations
  const originalProjectPrice = parseFloat(data.project_price) || 0;
  const isProjectOnly = selectedOption === "project-only";
  const activePlan = SUBSCRIPTION_PLANS.find((p) => p.id === selectedOption) || null;

  let finalProjectPrice = originalProjectPrice;
  let monthlyCost = 0;
  if (!isProjectOnly && activePlan) {
    const discount = (activePlan.discountPercent || 0) / 100;
    finalProjectPrice = originalProjectPrice * (1 - discount);
    monthlyCost = activePlan.monthlyPrice;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      <Helmet>
        <title>{pageTitle}</title>
      </Helmet>

      <ClientHeader />

      <main className="flex-grow">
        <ProjectDetails
          data={data}
          originalProjectPrice={originalProjectPrice}
          selectedOption={selectedOption}
          setSelectedOption={setSelectedOption}
          isProjectOnly={isProjectOnly}
        />

        <SubscriptionPlans
          subscriptionPlans={SUBSCRIPTION_PLANS}
          originalProjectPrice={originalProjectPrice}
          selectedOption={selectedOption}
          setSelectedOption={setSelectedOption}
        />

        <Summary
          isProjectOnly={isProjectOnly}
          originalProjectPrice={originalProjectPrice}
          finalProjectPrice={finalProjectPrice}
          monthlyCost={monthlyCost}
          activePlan={activePlan}
        />
      </main>
    </div>
  );
}

export default ClientPage;
