// src/ClientPage.jsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Helmet } from "react-helmet";

// Our new sub-components
import ClientHeader from "./components/ClientHeader";
import ProjectDetails from "./components/ProjectDetails";
import SubscriptionPlans from "./components/SubscriptionPlans";
import PlanComparison from "./components/PlanComparison";
import SingleProjectOption from "./components/SingleProjectOption";
import FrequentlyAskedQuestions from "./components/FrequentlyAskedQuestions";
import Footer from "./components/Footer";

// Import the CheckoutButton component
import CheckoutButton from "./components/CheckoutButton";

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
        <h1 className="text-3xl">
          This page does not exist or has expired.
        </h1>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 font-sans">
        <p className="text-lg text-gray-700 font-bold">Loading...</p>
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

        <section
          className="py-12"
          style={{
            background: 'linear-gradient(142deg, rgba(253,240,249,1) 0%, rgba(181,218,247,1) 100%)',
          }}
        >
          <SubscriptionPlans
            data={data}
            subscriptionPlans={SUBSCRIPTION_PLANS}
            originalProjectPrice={originalProjectPrice}
            selectedOption={selectedOption}
            setSelectedOption={setSelectedOption}
          />

          <PlanComparison
            data={data}
            originalProjectPrice={originalProjectPrice}
            selectedOption={selectedOption}
            setSelectedOption={setSelectedOption}
          />

          <SingleProjectOption
            originalProjectPrice={originalProjectPrice}
            setSelectedOption={setSelectedOption}
            isProjectOnly={isProjectOnly}
          />
        </section>


        <FrequentlyAskedQuestions
          data={data}
          originalProjectPrice={originalProjectPrice}
        />

        <Footer/>

        {/* 
          The CheckoutButton uses `slug` and the current `selectedOption`
          to call your Stripe session endpoint and redirect the user.
        */}
        {/* <div className="mt-6 mb-10 text-center">
          <CheckoutButton slug={slug} option={finalOption} />
        </div> */}
      </main>
    </div>
  );
}

export default ClientPage;
