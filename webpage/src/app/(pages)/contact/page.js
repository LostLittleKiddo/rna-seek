import React from 'react';

function page() {
  return (
        <div className="p-6 max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold mb-4  text-red-800">Troubleshooting</h1>
          <p className="mb-6">
            Please reach us through <a href="mailto:dwishart@ualberta.ca" className="text-blue-500 hover:underline">dwishart@ualberta.ca</a>. Your questions and our answers will benefit other users.
          </p>
        
          <h2 className="text-2xl font-semibold mb-2 text-red-800">Have you tried our example data to see if the issue still exists?</h2>
          <p className="mb-4">
            Most of the time, the issue is related to improper data format. Although we try to give informative error messages during the data uploading stage, there are always exceptions. Here are three tips:
          </p>
          <ul className="list-disc list-inside mb-6 space-y-2">
            <li>
              Open your file in a text editor (not a spreadsheet program) to see the details — are these values comma-separated (<code>.csv</code>) or tab-separated (<code>.txt</code>)?
            </li>
            <li>
              You may need to search "How to save my file in a <code>.csv</code> format" to get more detailed instructions.
            </li>
            <li>
              We offered a wide variety of example datasets. Please choose the one that matches your data type to see if the issue still appears. Download and open the data in a text editor for details.
            </li>
          </ul>
        
          <h2 className="text-2xl font-semibold mb-2  text-red-800">Did you provide enough details so that the issue can be reproduced?</h2>
          <p className="mb-4">
            Remote troubleshooting requires more information in order to figure out the exact cause of the issue. Please:
          </p>
          <ul className="list-disc list-inside mb-6 space-y-2">
            <li>Indicate which example data you used, or provide a copy of your data.</li>
            <li>Document all steps leading to the issue. Sometimes screenshots may be necessary.</li>
          </ul>
        
          <h2 className="text-2xl font-semibold mb-2  text-red-800">Support for New Features</h2>
          <p>
            Bugs are usually dealt with immediately (or within 3 days) once we have received and validated the bug report. New features will be evaluated based on the overall feedback from other users. Top-ranked features will be added as a minor release (3-month or 6-month period) depending on the available resources.
          </p>
        </div>
  );
}

export default page;
