import Head from "next/head";
import { GoGist, GoRepo } from "react-icons/go";
import { FiUserPlus, FiUsers } from "react-icons/fi";
import { useEffect, useState } from "react";
import axios from "axios";
import { Field, Form, Formik } from "formik";
import Navbar from "../components/Navbar";
import Cards from "../components/Cards";
import UserCard from "../components/UserCard";
import PublicRepos from "../components/PublicRepos";

export default function Home() {

    const [username, setUsername] = useState("");
    const [data, setData] = useState({});
    const [error, setError] = useState(null);

    useEffect(() => {
        const storedUsername = sessionStorage.getItem("username");
        if (storedUsername !== null) {
            setUsername(storedUsername);
        }
    }, []);


    useEffect(() => {
        sessionStorage.setItem("username", username);
        axios
            .get("/api/getTopRepos", { params: { username } })
            .then((res) => {
                if (res.data.success) {
                    setData(res.data.user);
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }, [username]);

    const initialValues = {
        ghusername: "",
    };

    const handleSubmit = (values, onSubmitProps) => {
        onSubmitProps.setSubmitting(true);
        axios
            .get("/api/getTopRepos", { params: { username: values.ghusername } })
            .then((res) => {
                if (res.data.success) {
                    console.log(res.data);
                    setData(res.data.user);
                    setError(null);
                    setUsername(values.ghusername);
                } else {
                    setError(res.data.error.message);
                }
            })
            .catch((err) => {
                console.log(err);
            });
        onSubmitProps.resetForm();
        onSubmitProps.setSubmitting(false);
    };

    const detailsData = [
        {
            id: 1,
            icon: <GoRepo />,
            title: "Public Repos",
            value: data.repositories ? data.repositories.totalCount : 0,
            color: "pink",
        },
        {
            id: 2,
            icon: <FiUsers />,
            title: "Followers",
            value: data.followers ? data.followers.totalCount : 0,
            color: "green",
        },
        {
            id: 3,
            icon: <FiUserPlus />,
            title: "Following",
            value: data.following ? data.following.totalCount : 0,
            color: "purple",
        },
        {
            id: 4,
            icon: <GoGist />,
            title: "Gists",
            value: data.gists ? data.gists.totalCount : 0,
            color: "yellow",
        },
    ];

    return (
        <>
            <Head>
                <title>Open Source Sustainability</title>
            </Head>
            <Navbar />
            <main className="container mx-auto p-4">
                <div className="mb-8">
                    <div className="mb-4">
                        <Formik initialValues={initialValues} onSubmit={handleSubmit}>
                            <Form className="flex flex-col sm:flex-row space-x-2">
                                <div className="flex-grow">
                                    <Field
                                        type="text"
                                        className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500"
                                        id="ghusername"
                                        name="ghusername"
                                        placeholder={username ? username : "Enter GitHub username"}
                                        autoComplete="off"
                                    />
                                </div>
                                <div>
                                    <button
                                        type="submit"
                                        className="w-full sm:w-auto px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring focus:bg-blue-600"
                                    >
                                        Search
                                    </button>
                                </div>
                            </Form>
                        </Formik>
                    </div>
                    <p className="text-red-500">{error}</p>
                </div>

                <Cards detailsData={detailsData} />

                <div className="flex flex-col sm:flex-row space-y-4 sm:space-x-4">
                    <div className="flex-grow">
                        <UserCard data={data} username={username} />
                    </div>
                    <div className="flex-grow">
                        <PublicRepos data={data} />
                    </div>
                </div>
            </main>
        </>
    );
}
