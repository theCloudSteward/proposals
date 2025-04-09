// src/ClientPage.jsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Helmet } from "react-helmet";

// Our sub-components
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
  const [error, setError] = useState(null); // Added error state for better handling

  // Fetch data with improved error handling
  useEffect(() => {
    fetch(`/api/pages/${slug}/`)
      .then((res) => {
        if (res.status === 404) {
          setNotFound(true);
          return null;
        }
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((pageData) => {
        if (pageData) setData(pageData);
      })
      .catch((err) => {
        setError(err); // Capture errors instead of just logging them
      });
  }, [slug]);

  // Use process.env.PUBLIC_URL with a fallback for dynamic paths
  const publicUrl = process.env.PUBLIC_URL || "";

  // Handle error state first
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100 font-sans">
        <Helmet>
          <title>Error</title>
          <meta name="description" content="An error occurred while loading the proposal." />
          <meta property="og:title" content="Error" />
          <meta property="og:description" content="An error occurred while loading the proposal." />
          <meta property="og:image" content={`${publicUrl}/android-chrome-192x192.png`} />
        </Helmet>
        <h1 className="text-3xl">An error occurred: {error.message}</h1>
      </div>
    );
  }

  // Handle 404 case
  if (notFound) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100 font-sans">
        <Helmet>
          <title>Page Not Found</title>
          <meta name="description" content="The requested proposal page does not exist or has expired." />
          <meta property="og:title" content="Page Not Found" />
          <meta property="og:description" content="The requested proposal page does not exist or has expired." />
          <meta property="og:image" content={`${publicUrl}/android-chrome-192x192.png`} />
        </Helmet>
        <h1 className="text-3xl">This page does not exist or has expired.</h1>
      </div>
    );
  }

  // Handle loading state
  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 font-sans">
        <Helmet>
          <title>Loading...</title>
          <meta name="description" content="Loading the proposal page..." />
          <meta property="og:title" content="Loading..." />
          <meta property="og:description" content="Loading the proposal page..." />
          <meta property="og:image" content={`${publicUrl}/android-chrome-192x192.png`} />
        </Helmet>
        <p className="text-lg text-gray-700 font-bold">Loading...</p>
      </div>
    );
  }

  // Main content when data is loaded
  const pageTitle = `${data.company_name} Proposal`;
  const pageDescription = `View the proposal for ${data.company_name}, including project details and subscription plans.`;

  return (
    <div className="min-h-screen flex flex-col font-sans">
      <Helmet>
        <title>{pageTitle}</title>
        <meta name="description" content={pageDescription} />
        <meta property="og:title" content={pageTitle} />
        <meta property="og:description" content={pageDescription} />
        <meta property="og:image" content={`${publicUrl}/android-chrome-192x192.png`} />
        <meta property="og:type" content="website" />
      </Helmet>

      {/* Gradient section that covers the top of the page */}
      <section
        className="min-h-screen"
        style={{
          background: "linear-gradient(142deg, rgba(253,240,249,1) 0%, rgba(181,218,247,1) 100%)",
        }}
      >
        <ClientHeader />
        <main className="flex-grow">
          <ProjectDetails data={data} />
          <SubscriptionPlans data={data} />
          <PlanComparison data={data} />
          <SingleProjectOption data={data} />
        </main>
      </section>

      {/* Section that stops the gradient */}
      <section className="bg-white">
        <FrequentlyAskedQuestions />
        <Footer />
      </section>
    </div>
  );
}

export default ClientPage;