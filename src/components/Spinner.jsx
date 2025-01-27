'use client';

import React from "react";
import Image from "next/image";

const Spinner = () => {
  return (
    <div className="w-full h-screen flex items-center justify-center">
      <Image src="/spinner.gif" alt="loading.." width={100} height={100} />
    </div>
  );
};

export default Spinner;
