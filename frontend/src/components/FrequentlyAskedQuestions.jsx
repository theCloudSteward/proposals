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
    <section className="py-12" style={{ backgroundColor: '#383838' }}>
      <div className="max-w-5xl mx-auto px-4 text-white">
          {/* FAQ Layout */}
          <div className="flex flex-col md:flex-row md:space-x-6">
            {/* Left Side: FAQ Header */}
            <div className="md:w-1/3 mb-6 md:mb-0">
              <h3 className="text-2xl font-semibold text-white">
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
                    <span className="text-lg font-medium text-black">
                      {faq.question}
                    </span>
                    <span className="text-black">
                      {openIndex === index ? '-' : '+'}
                    </span>
                  </button>
                  {openIndex === index && (
                    <div className="p-4 bg-gray-50 rounded-b text-black">
                      {faq.answer}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
    </section>
  );
}

export default FrequentlyAskedQuestions;