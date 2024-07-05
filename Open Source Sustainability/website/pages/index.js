import Link from 'next/link';
import React from 'react';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold">Welcome to the Open-Source Sustainability Project!</h1>
      <div>
        <br />
        <h1 className="text-2xl">Computational models for your open-source software community</h1>
        <br />
      </div>
      <div className="ml-[6rem] mr-[6rem] border-black border-2 rounded-lg p-4 bg-gray-200">
        <p className="text-center">The Open-Source Sustainability Project is the brainchild of the Orthogonal Research and Education Lab, whose intent is to explore the sustainability of open-source projects via Agent-based Modelling. If you&apos;re interested in modeling your community, all you need is a GitHub account to get started. Click the button below to connect your GitHub account, and get modeling!</p>
      </div>
      <Link href="/home">
        <button className="bg-blue-950 text-white rounded-md p-3 mt-4">Get started</button>
      </Link>
    </div>
  );
}
