import Image from 'next/image';
import Link from 'next/link';
import React from 'react';
import { CgOrganisation } from 'react-icons/cg';
import { FiLink } from 'react-icons/fi';
import { IoLocationOutline } from 'react-icons/io5';

const UserCard = ({ data, username }) => {
    return (
        <div className="detail user-detail-1 border p-3">
            <div className="flex justify-between my-3">
                <div className="">
                    <h2 className="text-xl font-semibold">{data.name ? data.name : username}</h2>
                    {data.name && (
                        <p>
                            <Link href={`https://github.com/${username}`} className="text-blue-600 hover:underline">
                                @{username}
                            </Link>
                        </p>
                    )}
                </div>
                <div className="mx-2">
                    {data.name && (
                        <Image
                            src={data.avatarUrl}
                            alt={data.name}
                            width={100}
                            height={100}
                            className="rounded-full border-black border-4"
                        />
                    )}
                </div>
            </div>
            <p>{data.bio}</p>
            <ul className="list-none">
                {data.company && (
                    <li className="flex items-center">
                        <span className="mx-2">
                            <CgOrganisation />
                        </span>
                        {data.company}
                    </li>
                )}
                {data.location && (
                    <li className="flex items-center">
                        <span className="mx-2">
                            <IoLocationOutline />
                        </span>
                        {data.location}
                    </li>
                )}
                {data.websiteUrl && (
                    <li className="flex items-center">
                        <span className="mx-2">
                            <FiLink />
                        </span>
                        <Link href={data.websiteUrl} className="text-blue-600 hover:underline">
                            {data.websiteUrl}
                        </Link>
                    </li>
                )}
            </ul>
        </div>
    );
};

export default UserCard;
