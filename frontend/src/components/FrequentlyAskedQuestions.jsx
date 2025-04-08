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
      question: "Can I cancel my subscription if I change my mind?",
      answer: "Yes. You can cancel at any time without obligation. Just send an email to ben@thecloudsteward.com."
    },
    {
      question: "Why do you have a subscription model?",
      answer: "The mission of Cloud Steward is to be the best steward of NetSuite systems. We need to build long-term business relationships to accomplish that."
    },
    {
      question: "Can I upgrade my plan later?",
      answer: "Yes, you can contact us to discuss upgrading to a higher tier."
    },
    {
      question: "What payment methods are accepted?",
      answer: "We accept credit cards and bank transfers through Stripe."
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
              <p className="text-lg font-semibold text-white">
                Have more questions? <a className="text-blue-300" href="https://www.thecloudsteward.com/contact">Contact Ben</a>.
              </p>
            </div>

            {/* Right Side: Accordion */}
            <div className="md:w-2/3">
              {faqs.map((faq, index) => (
                <div key={index} className="mb-4">
                  <button
                    onClick={() => toggleAccordion(index)}
                    className="w-full text-left py-3 px-4 bg-white bg-opacity-90 rounded-t-md focus:outline-none flex justify-between items-center"
                  >
                    <span className="text-base font-medium text-black">
                      {faq.question}
                    </span>
                    <span className="text-black">
                      {openIndex === index ? '-' : '+'}
                    </span>
                  </button>
                  {openIndex === index && (
                    <div className="p-4 bg-white bg-opacity-80 rounded-b-md text-black">
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