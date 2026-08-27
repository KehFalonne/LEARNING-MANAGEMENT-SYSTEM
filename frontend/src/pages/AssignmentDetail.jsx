import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import api from "../api/axios";


export default function AssignmentDetail() {

    const { assignmentId } = useParams();

    const [assignment, setAssignment] = useState(null);
    const [file, setFile] = useState(null);

    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");


    useEffect(() => {

        const fetchAssignment = async () => {

            try {

                const response = await api.get(
                    "/assignments/student/"
                );

                const foundAssignment =
                    response.data.find(
                        (item) =>
                            item.id === Number(assignmentId)
                    );

                if (!foundAssignment) {

                    setError(
                        "Assignment not found."
                    );

                    return;

                }

                setAssignment(foundAssignment);

            } catch (error) {

                console.error(error);

                setError(
                    "Unable to load assignment."
                );

            } finally {

                setLoading(false);

            }

        };

        fetchAssignment();

    }, [assignmentId]);


    const handleSubmit = async (event) => {

        event.preventDefault();

        if (!file) {

            setError(
                "Please select a file before submitting."
            );

            return;

        }

        try {

            setSubmitting(true);
            setError("");
            setSuccess("");

            const formData = new FormData();

            formData.append(
                "file",
                file
            );

            const response = await api.post(
                `/assignments/student/${assignmentId}/submit/`,
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );

            setSuccess(
                response.data.status === "LATE"
                    ? "Assignment submitted successfully, but it was submitted late."
                    : "Assignment submitted successfully."
            );

            setAssignment(
                (currentAssignment) => ({
                    ...currentAssignment,
                    submitted: true,
                    submission_status:
                        response.data.status,
                    marks:
                        response.data.marks,
                    feedback:
                        response.data.feedback,
                })
            );

            setFile(null);

        } catch (error) {

            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Unable to submit assignment."
            );

        } finally {

            setSubmitting(false);

        }

    };


    if (loading) {

        return (
            <div className="d-flex justify-content-center align-items-center vh-100">

                <div
                    className="spinner-border"
                    role="status"
                >
                    <span className="visually-hidden">
                        Loading...
                    </span>
                </div>

            </div>
        );

    }


    if (error && !assignment) {

        return (
            <div className="container py-5">

                <div className="alert alert-danger">
                    {error}
                </div>

                <Link
                    to="/assignments"
                    className="btn btn-outline-primary"
                >
                    Back to Assignments
                </Link>

            </div>
        );

    }


    return (

        <div className="container py-4">

            <Link
                to="/assignments"
                className="text-decoration-none"
            >
                ← Back to Assignments
            </Link>


            <div className="card border-0 shadow-sm mt-4">

                <div className="card-body p-4">

                    <div className="d-flex justify-content-between align-items-start mb-4">

                        <div>

                            <span className="badge text-bg-primary mb-2">

                                {assignment.course_code}

                            </span>

                            <h2 className="fw-bold">
                                {assignment.title}
                            </h2>

                            <p className="text-muted mb-0">
                                {assignment.course_title}
                            </p>

                        </div>


                        <span className="badge text-bg-secondary">

                            {assignment.submission_status ||
                                "Not Submitted"}

                        </span>

                    </div>


                    <hr />


                    <h5 className="fw-bold">
                        Instructions
                    </h5>

                    <p>
                        {assignment.instructions}
                    </p>


                    {assignment.attachment && (

                        <div className="mb-4">

                            <a
                                href={assignment.attachment}
                                target="_blank"
                                rel="noreferrer"
                                className="btn btn-outline-secondary"
                            >
                                <i className="bi bi-paperclip me-2"></i>

                                Download Assignment Attachment
                            </a>

                        </div>

                    )}


                    <div className="row mb-4">

                        <div className="col-md-6">

                            <strong>Total Marks:</strong>{" "}

                            {assignment.total_marks}

                        </div>


                        <div className="col-md-6">

                            <strong>Due Date:</strong>{" "}

                            {new Date(
                                assignment.due_date
                            ).toLocaleString()}

                        </div>

                    </div>


                    {/* GRADE AND FEEDBACK */}

                    {assignment.submitted &&
                        assignment.marks !== null && (

                        <div className="alert alert-success">

                            <h5 className="fw-bold">
                                Assignment Graded
                            </h5>

                            <p className="mb-1">

                                <strong>Marks:</strong>{" "}

                                {assignment.marks} /{" "}

                                {assignment.total_marks}

                            </p>

                            <p className="mb-0">

                                <strong>Feedback:</strong>{" "}

                                {assignment.feedback ||
                                    "No feedback provided."}

                            </p>

                        </div>

                    )}


                    {/* SUBMISSION FORM */}

                    <div className="border-top pt-4">

                        <h5 className="fw-bold">
                            {assignment.submitted
                                ? "Resubmit Assignment"
                                : "Submit Assignment"}
                        </h5>


                        {success && (

                            <div className="alert alert-success">
                                {success}
                            </div>

                        )}


                        {error && assignment && (

                            <div className="alert alert-danger">
                                {error}
                            </div>

                        )}


                        <form onSubmit={handleSubmit}>

                            <div className="mb-3">

                                <label
                                    className="form-label"
                                >
                                    Select File
                                </label>

                                <input
                                    type="file"
                                    className="form-control"
                                    accept=".pdf,.doc,.docx,.zip"
                                    onChange={(event) =>
                                        setFile(
                                            event.target.files[0]
                                        )
                                    }
                                />

                                <div className="form-text">
                                    Allowed files: PDF, DOC, DOCX, ZIP
                                </div>

                            </div>


                            <button
                                type="submit"
                                className="btn btn-primary"
                                disabled={submitting}
                            >

                                {submitting ? (
                                    <>
                                        <span
                                            className="spinner-border spinner-border-sm me-2"
                                        ></span>

                                        Submitting...
                                    </>
                                ) : (
                                    assignment.submitted
                                        ? "Resubmit Assignment"
                                        : "Submit Assignment"
                                )}

                            </button>

                        </form>

                    </div>

                </div>

            </div>

        </div>

    );

}