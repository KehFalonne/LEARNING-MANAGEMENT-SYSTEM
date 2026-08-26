import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import api from "../api/axios";
import { useAuth } from "../context/AuthContext";


export default function CourseDetail() {

    const { offeringId } = useParams();

    const { user } = useAuth();

    const [course, setCourse] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");


    useEffect(() => {

        const fetchCourse = async () => {

            try {

                const token =
                    localStorage.getItem(
                        "access_token"
                    );

                const response = await api.get(
                    `/courses/student/${offeringId}/`,
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`,
                        },
                    }
                );

                setCourse(response.data);

            } catch (error) {

                console.error(error);

                setError(
                    "Unable to load this course."
                );

            } finally {

                setLoading(false);

            }
        };


        fetchCourse();

    }, [offeringId]);


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


    if (error) {

        return (
            <div className="container py-5">

                <div className="alert alert-danger">
                    {error}
                </div>

                <Link
                    to="/dashboard"
                    className="btn btn-primary"
                >
                    Back to Dashboard
                </Link>

            </div>
        );
    }


    return (

        <div className="container-fluid py-4">

            {/* BACK */}

            <div className="mb-4">

                <Link
                    to="/dashboard"
                    className="text-decoration-none"
                >
                    ← Back to Dashboard
                </Link>

            </div>


            {/* COURSE HEADER */}

            <div className="card border-0 shadow-sm mb-4">

                <div className="card-body p-4">

                    <div className="d-flex justify-content-between align-items-start">

                        <div>

                            <span className="badge text-bg-primary mb-2">
                                {course.course_code}
                            </span>

                            <h1 className="fw-bold mb-2">
                                {course.course_title}
                            </h1>

                            <p className="text-muted mb-0">
                                {course.description ||
                                    "No course description available."
                                }
                            </p>

                        </div>


                        <span className="badge text-bg-success">
                            Active
                        </span>

                    </div>

                </div>

            </div>


            {/* COURSE INFORMATION */}

            <div className="row g-4 mb-4">

                <div className="col-md-3">

                    <div className="card border-0 shadow-sm h-100">

                        <div className="card-body">

                            <small className="text-muted">
                                Credit Units
                            </small>

                            <h4 className="fw-bold mt-2">
                                {course.credit_units}
                            </h4>

                        </div>

                    </div>

                </div>


                <div className="col-md-3">

                    <div className="card border-0 shadow-sm h-100">

                        <div className="card-body">

                            <small className="text-muted">
                                Course Type
                            </small>

                            <h4 className="fw-bold mt-2">
                                {course.course_type}
                            </h4>

                        </div>

                    </div>

                </div>


                <div className="col-md-3">

                    <div className="card border-0 shadow-sm h-100">

                        <div className="card-body">

                            <small className="text-muted">
                                Semester
                            </small>

                            <h4 className="fw-bold mt-2">
                                {course.semester}
                            </h4>

                        </div>

                    </div>

                </div>


                <div className="col-md-3">

                    <div className="card border-0 shadow-sm h-100">

                        <div className="card-body">

                            <small className="text-muted">
                                Academic Session
                            </small>

                            <h4 className="fw-bold mt-2">
                                {course.academic_session}
                            </h4>

                        </div>

                    </div>

                </div>

            </div>


            {/* LECTURERS */}

            <div className="card border-0 shadow-sm mb-4">

                <div className="card-body">

                    <h4 className="fw-bold mb-3">
                        Course Lecturer
                    </h4>

                    {course.lecturers?.length > 0 ? (

                        course.lecturers.map(
                            (lecturer) => (

                                <div
                                    key={lecturer.id}
                                    className="d-flex align-items-center border-bottom py-3"
                                >

                                    <div
                                        className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center me-3"
                                        style={{
                                            width: "48px",
                                            height: "48px",
                                        }}
                                    >
                                        <i className="bi bi-person"></i>
                                    </div>


                                    <div>

                                        <div className="fw-semibold">
                                            {
                                                lecturer.lecturer_name
                                            }
                                        </div>

                                        <small className="text-muted">
                                            Staff ID:{" "}
                                            {
                                                lecturer.staff_id
                                            }
                                        </small>

                                    </div>


                                    {lecturer.is_primary && (

                                        <span className="badge text-bg-primary ms-auto">
                                            Primary Lecturer
                                        </span>

                                    )}

                                </div>

                            )
                        )

                    ) : (

                        <p className="text-muted mb-0">
                            No lecturer assigned yet.
                        </p>

                    )}

                </div>

            </div>


            {/* LMS SECTIONS */}

            <div className="row g-4">

                <div className="col-md-4">

                    <div className="card border-0 shadow-sm h-100">

                        <div className="card-body">

                            <i className="bi bi-file-earmark-text fs-2"></i>

                            <h5 className="fw-bold mt-3">
                                Learning Materials
                            </h5>

                            <p className="text-muted">
                                Access lecture notes,
                                presentations and other
                                learning resources.
                            </p>

                            <button
                                className="btn btn-outline-primary"
                                disabled
                            >
                                Coming Soon
                            </button>

                        </div>

                    </div>

                </div>


                <div className="col-md-4">

                    <div className="card border-0 shadow-sm h-100">

                        <div className="card-body">

                            <i className="bi bi-clipboard-check fs-2"></i>

                            <h5 className="fw-bold mt-3">
                                Assignments
                            </h5>

                            <p className="text-muted">
                                View and submit your
                                course assignments.
                            </p>

                            <button
                                className="btn btn-outline-primary"
                                disabled
                            >
                                Coming Soon
                            </button>

                        </div>

                    </div>

                </div>


                <div className="col-md-4">

                    <div className="card border-0 shadow-sm h-100">

                        <div className="card-body">

                            <i className="bi bi-question-circle fs-2"></i>

                            <h5 className="fw-bold mt-3">
                                Quizzes
                            </h5>

                            <p className="text-muted">
                                Take online quizzes and
                                view your results.
                            </p>

                            <button
                                className="btn btn-outline-primary"
                                disabled
                            >
                                Coming Soon
                            </button>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    );
}