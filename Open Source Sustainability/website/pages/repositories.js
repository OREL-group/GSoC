import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import AllRepos from "../components/AllRepos";
import axios from "axios";

export default function Repos() {
    const [repos, setRepos] = useState({});

    // useEffect(() => {
    //     let username = sessionStorage.getItem("username");

    //     axios
    //         .get("/api/getAllRepos", { params: { username: username } })
    //         .then((res) => {
    //             // Update the state after fetching data
    //             setRepos(res.data);
    //             // console.log(res.data);
    //         })
    //         .catch((err) => {
    //             console.log(err);
    //         });
    // }, []);

    return (
        <>
            <Navbar />
            <AllRepos />
        </>
    );
}
