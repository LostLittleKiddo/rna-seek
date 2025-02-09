export default function Home() {
  return (
    <main className="p-4 " >
      <div className="container mx-auto p-6 rounded-lg">
        <h1 className="text-5xl font-bold mb-6 text-gray-900">Welcome to RNAseek</h1>
        <p className="mb-6 text-lg text-gray-800">
          RNAseek is your one-stop platform for RNA-seq analysis. Designed to simplify and enhance your bioinformatics workflow, our powerful suite of tools is tailored for professionals and researchers alike.
        </p>
        <h2 className="text-3xl font-semibold mb-4 text-gray-900">Get Started</h2>
        <p className="mb-6 text-lg text-gray-800">
          To access our cutting-edge tools for quality control, alignment, quantification, differential expression analysis, and more:
        </p>
        <ul className="list-disc list-inside mb-6 text-lg text-gray-800">
          <li><strong>Login or Sign Up:</strong> Secure your data and personalize your analysis by creating an account or logging in.</li>
          <li><strong>Explore Tools:</strong> Once logged in, you can utilize tools like FASTQC, Trimomatic, HISAT2, DESeq2, and others to process and analyze RNA-seq data effortlessly.</li>
        </ul>
        <h2 className="text-3xl font-semibold mb-4 text-gray-900">Why Choose RNAseek?</h2>
        <ul className="list-disc list-inside mb-6 text-lg text-gray-800">
          <li><strong>Client-Side Security:</strong> Run tools directly on your computer using WebAssembly for optimal data privacy.</li>
          <li><strong>Comprehensive Analysis:</strong> From pre-processing to pathway analysis, RNAseek integrates all essential steps.</li>
          <li><strong>User-Friendly Interface:</strong> Navigate a clean and intuitive platform built with the latest web technologies.</li>
        </ul>
        <p className="text-2xl font-bold text-gray-900">Log in now and revolutionize your RNA-seq research!</p>
      </div>
    </main>
  )
}