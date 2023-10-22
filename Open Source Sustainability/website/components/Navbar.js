import React from 'react';
import Image from 'next/image';

const Navbar = () => {
  return (
    <nav className="bg-slate-300">
      <div className="flex justify-center items-center">
        <div className="w-16 h-16">
          <Image
            src="https://user-images.githubusercontent.com/92572013/266610534-0b13f675-40f1-4b16-b9cd-19f5ff21619e.png"
            alt=""
            width={100}
            height={100}
          />
        </div>
        <h1 className="text-3xl font-bold mt-19 ml-4">OREL - Open Source Sustainability</h1>
      </div>
    </nav>
  );
};

export default Navbar;
