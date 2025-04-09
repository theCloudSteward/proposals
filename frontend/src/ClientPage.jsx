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

function ClientPage() {
  const { slug } = useParams();
  const [data, setData] = useState(null);
  const [notFound, setNotFound] = useState(false);

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
  return (
    <div className="min-h-screen flex flex-col font-sans">
      <Helmet>
        <title>{pageTitle}</title>
      </Helmet>

      {/* Gradient section that covers the top of the page */}
      <section
        className="min-h-screen"
        style={{ background: 'linear-gradient(142deg, rgba(253,240,249,1) 0%, rgba(181,218,247,1) 100%)' }}
      >
        <ClientHeader />
        <main className="flex-grow">
          <ProjectDetails
            data={data}
          />
          <SubscriptionPlans
            data={data}
          />
          <PlanComparison
            data={data}
          />
          <SingleProjectOption
            data={data}
          />
        </main>
      </section>

      {/* Section that stops the gradient */}
      <section className="bg-white">
        <FrequentlyAskedQuestions/>
        <Footer />
      </section>
    </div>
  );
}

export default ClientPage;