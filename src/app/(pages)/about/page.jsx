import React from 'react';

const Page = () => {
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4 text-blue-800">Context for RNAseek Project</h1>
      <p className="mb-6">
        RNA sequencing (RNA-seq) is a powerful and widely used technology in molecular biology, enabling researchers to analyze gene expression and uncover biological insights across diverse organisms and experimental conditions. However, RNA-seq data analysis involves a complex, multi-step computational workflow that can be a barrier for researchers without specialized bioinformatics expertise.
      </p>
      <p className="mb-6">
        RNAseek is being developed as a web-based platform to simplify and automate the RNA-seq analysis process. Designed for both novice and experienced users, RNAseek transforms raw sequencing data into interpretable results, offering an intuitive interface to execute and visualize bioinformatics workflows. By combining quality control, alignment, expression quantification, and functional analysis into a seamless pipeline, RNAseek empowers researchers to focus on their biological questions rather than technical hurdles.
      </p>
      <p className="mb-6">
        The platform integrates industry-standard tools such as FASTQC, Trimmomatic, HISAT2, STAR, FeatureCounts, DESeq2, edgeR, GSEA, and PathBank, and provides visualization with HeatMapper2. RNAseek is designed to be accessible through any modern web browser, eliminating the need for local software installations. With its user-first design, it bridges the gap between raw RNA-seq data and meaningful biological insights, promoting data-driven research and discovery.
      </p>
    </div>
  );
};

export default Page;