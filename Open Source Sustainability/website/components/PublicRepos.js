import Link from 'next/link';
import React from 'react';

const PublicRepos = ({ data }) => {
    return (
        <div className="detail user-detail-1 border p-3">
            <div className="flex justify-between items-center mb-3">
                <div>
                    <h4 className="">User Repositories</h4>
                    {data.repositories && (
                        <p className="text-gray-500">
                            {data.repositories.nodes.length} / {data.repositories.totalCount}
                        </p>
                    )}
                </div>
                {data.repositories && data.repositories.nodes.length > 0 && (
                    <div>
                        <Link href="/repositories">
                            <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 focus:outline-none focus:ring focus:bg-blue-600">
                                View More
                            </button>
                        </Link>
                    </div>
                )}
            </div>
            <ul className="list-none">
                {data.repositories &&
                    data.repositories.nodes.map((repo) => {
                        return (
                            <li key={repo.id}>
                                <Link key={repo.id} href={repo.url} className="text-blue-600 hover:underline text-base">
                                    {repo.name}
                                </Link>
                            </li>
                        );
                    })}
            </ul>
        </div>
    );
};

export default PublicRepos;
