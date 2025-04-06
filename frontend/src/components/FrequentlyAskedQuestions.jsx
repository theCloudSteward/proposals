import React, { useState } from 'react';

function FrequentlyAskedQuestions({
  data,
  originalProjectPrice,
  isProjectOnly,
  setSelectedOption,
  selectedOption
}) {
  // State to manage which accordion item is open
  const [openIndex, setOpenIndex] = useState(null);

  // Sample Q&A data
  const faqs = [
    {
      question: "What is included in the project?",
      answer: "The project includes all core features as outlined in the project details, with no additional monthly fees."
    },
    {
      question: "How long will the project take?",
      answer: "The timeline depends on the scope, but typically ranges from 4 to 12 weeks."
    },
    {
      question: "Can I upgrade my plan later?",
      answer: "Yes, you can contact us to discuss upgrading to a higher tier or adding features."
    },
    {
      question: "What payment methods are accepted?",
      answer: "We accept credit cards, bank transfers, and PayPal for all project payments."
    }
  ];

  // Toggle accordion item
  const toggleAccordion = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section className="py-12" style={{ backgroundColor: '#596E5C' }}>
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
            <strong>Regular Project Price:</strong> $
            {originalProjectPrice.toFixed(2)}
          </p>

          <div
            className="prose mb-6 text-gray-800"
            dangerouslySetInnerHTML={{ __html: data.project_details }}
          />

          {/* FAQ Layout */}
          <div className="flex flex-col md:flex-row md:space-x-6">
            {/* Left Side: FAQ Header */}
            <div className="md:w-1/3 mb-6 md:mb-0">
              <h3 className="text-2xl font-semibold text-gray-800">
                Frequently Asked Questions
              </h3>
            </div>

            {/* Right Side: Accordion */}
            <div className="md:w-2/3">
              {faqs.map((faq, index) => (
                <div key={index} className="mb-4">
                  <button
                    onClick={() => toggleAccordion(index)}
                    className="w-full text-left py-3 px-4 bg-gray-100 rounded-t focus:outline-none flex justify-between items-center"
                  >
                    <span className="text-lg font-medium text-gray-800">
                      {faq.question}
                    </span>
                    <span className="text-gray-600">
                      {openIndex === index ? '-' : '+'}
                    </span>
                  </button>
                  {openIndex === index && (
                    <div className="p-4 bg-gray-50 rounded-b text-gray-700">
                      {faq.answer}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default FrequentlyAskedQuestions;