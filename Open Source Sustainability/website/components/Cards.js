import React from 'react';

const Cards = ({ detailsData }) => {
    return (
        <div className="detail-container">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                {detailsData.map((detail) => (
                    <div key={detail.id} className="bg-white border p-4 rounded-lg shadow-md">
                        <div className={`text-${detail.color} text-4xl mb-2`}>
                            {detail.icon}
                        </div>
                        <div className="text-black">
                            <h4 className="text-lg font-semibold">{detail.value}</h4>
                            <p className="text-gray-500">{detail.title}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Cards;
