import React from 'react';

function Footer() {
  // Function to scroll to the top of the page
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth' // Smooth scrolling effect
    });
  };

  return (
    <footer className="py-6" style={{ backgroundColor: '#383838' }}>
      <div className="max-w-5xl mx-auto px-4 flex justify-center">
        <button
          onClick={scrollToTop}
          className="py-2 px-6 bg-white bg-opacity-60 text-gray-800 rounded shadow-md hover:bg-gray-200 transition-colors"
        >
          Back to Top
        </button>
      </div>
    </footer>
  );
}

export default Footer;