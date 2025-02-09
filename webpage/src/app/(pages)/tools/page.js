"use client";
import React, { useEffect, useState } from "react";
import { UserAuth } from "../../../context/AuthContext";
import Spinner from "../../../components/Spinner";
import InputFQ from "../../../components/Input";

export default function FastQCPage() {
    const { user } = UserAuth();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAuthentication = async () => {
            await new Promise((resolve) => setTimeout(resolve, 50));
            setLoading(false);
        };
        checkAuthentication();
    }, [user]);

    return (
        <div className=" bg-gray-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">FASTQ File Analyzer</h1>
                {loading ? (
                    <Spinner />
                ) : user ? (
                    <InputFQ />
                ) : (
                    <div className="p-4 bg-yellow-50 text-yellow-800 rounded-lg">
                        You must be logged in to access this tool.
                    </div>
                )}
            </div>
        </div>
    );
}