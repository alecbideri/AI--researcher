import React from 'react';

const ResearchReport = ({ report }) => {
  const handleDownload = async () => {
    try {
      const response = await fetch(`http://localhost:8000/generate_pdf?content=${encodeURIComponent(report)}`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = "research_report.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (e) {
      console.error("Download failed", e);
    }
  };

  return (
    <div className="bg-black rounded-none border border-gray-800 p-8 shadow-2xl mt-12 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 to-purple-500"></div>
      <div className="flex justify-between items-center mb-8 border-b border-gray-800 pb-4">
        <h2 className="text-xl font-bold text-white tracking-widest uppercase">Research Report</h2>
        <button
          onClick={handleDownload}
          className="bg-white text-black hover:bg-gray-200 font-bold py-2 px-6 text-xs tracking-widest uppercase transition border border-transparent"
        >
          Download PDF
        </button>
      </div>
      <div className="prose prose-invert max-w-none">
        <pre className="whitespace-pre-wrap font-sans text-gray-300 leading-relaxed text-sm">{report}</pre>
      </div>
    </div>
  );
};

export default ResearchReport;
