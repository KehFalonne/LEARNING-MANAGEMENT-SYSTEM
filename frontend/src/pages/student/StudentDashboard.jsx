import { useEffect, useState } from "react";

import { useAuth } from "../../context/AuthContext";
import api from "../../api/axios";


export default function StudentDashboard() {

    const { user, logout } = useAuth();

    const [dashboard, setDashboard] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    useEffect(() => {

        const fetchDashboard = async () => {

            try {

                const token = localStorage.getItem(
                    "access_token"
                );

                const response = await api.get(
                    "/students/dashboard/",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );

                setDashboard(response.data);

            } catch (error) {

                console.error(error);

                setError(
                    "Unable to load your dashboard."
                );

            } finally {

                setLoading(false);

            }
        };


        fetchDashboard();

    }, []);


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

            </div>
        );
    }


    const student = dashboard?.student;
    const courses = dashboard?.courses || [];


    return (

        <div className="container-fluid py-4">

            {/* HEADER */}

            <div className="d-flex justify-content-between align-items-center mb-4">

                <div>

                    <h2 className="fw-bold mb-1">
                        Student Dashboard
                    </h2>

                    <p className="text-muted mb-0">
                        Welcome back, {student?.full_name}
                    </p>

                </div>


                <button
                    className="btn btn-outline-danger"
                    onClick={logout}
                >
                    Logout
                </button>

            </div>


            {/* STUDENT INFORMATION */}

            <div className="card border-0 shadow-sm mb-4">

                <div className="card-body">

                    <div className="row">

                        <div className="col-md-3">

                            <small className="text-muted">
                                Student ID
                            </small>

                            <div className="fw-semibold">
                                {student?.student_id}
                            </div>

                        </div>


                        <div className="col-md-3">

                            <small className="text-muted">
                                Programme
                            </small>

                            <div className="fw-semibold">
                                {student?.programme_name}
                            </div>

                        </div>


                        <div className="col-md-3">

                            <small className="text-muted">
                                Level
                            </small>

                            <div className="fw-semibold">
                                {student?.level_name}
                            </div>

                        </div>


                        <div className="col-md-3">

                            <small className="text-muted">
                                Status
                            </small>

                            <div className="fw-semibold">
                                {student?.status}
                            </div>

                        </div>

                    </div>

                </div>

            </div>


            {/* STATISTICS */}

            <div className="row g-4 mb-4">

                <div className="col-md-4">

                    <div className="card border-0 shadow-sm">

                        <div className="card-body">

                            <h6 className="text-muted">
                                Registered Courses
                            </h6>

                            <h2 className="fw-bold">
                                {courses.length}
                            </h2>

                        </div>

                    </div>

                </div>


                <div className="col-md-4">

                    <div className="card border-0 shadow-sm">

                        <div className="card-body">

                            <h6 className="text-muted">
                                Total Credit Units
                            </h6>

                            <h2 className="fw-bold">

                                {courses.reduce(
                                    (total, course) =>
                                        total +
                                        course.credit_units,
                                    0
                                )}

                            </h2>

                        </div>

                    </div>

                </div>


                <div className="col-md-4">

                    <div className="card border-0 shadow-sm">

                        <div className="card-body">

                            <h6 className="text-muted">
                                Academic Session
                            </h6>

                            <h2 className="fw-bold">

                                {courses[0]?.academic_session || "—"}

                            </h2>

                        </div>

                    </div>

                </div>

            </div>


            {/* COURSES */}

            <div className="card border-0 shadow-sm">

                <div className="card-body">

                    <div className="d-flex justify-content-between align-items-center mb-3">

                        <h4 className="fw-bold mb-0">
                            My Courses
                        </h4>

                        <span className="badge text-bg-primary">
                            {courses.length} Courses
                        </span>

                    </div>


                    {courses.length === 0 ? (

                        <div className="text-center py-5">

                            <h5>
                                No courses registered
                            </h5>

                            <p className="text-muted">
                                You currently have no active
                                course registrations.
                            </p>

                        </div>

                    ) : (

                        <div className="table-responsive">

                            <table className="table align-middle">

                                <thead>

                                    <tr>

                                        <th>
                                            Course Code
                                        </th>

                                        <th>
                                            Course Title
                                        </th>

                                        <th>
                                            Credits
                                        </th>

                                        <th>
                                            Semester
                                        </th>

                                        <th>
                                            Status
                                        </th>

                                    </tr>

                                </thead>


                                <tbody>

                                    {courses.map(
                                        (course) => (

                                            <tr
                                                key={
                                                    course.id
                                                }
                                            >

                                                <td className="fw-semibold">
                                                    {
                                                        course.course_code
                                                    }
                                                </td>

                                                <td>
                                                    {
                                                        course.course_title
                                                    }
                                                </td>

                                                <td>
                                                    {
                                                        course.credit_units
                                                    }
                                                </td>

                                                <td>
                                                    {
                                                        course.semester
                                                    }
                                                </td>

                                                <td>

                                                    <span className="badge text-bg-success">
                                                        {
                                                            course.status
                                                        }
                                                    </span>

                                                </td>

                                            </tr>

                                        )
                                    )}

                                </tbody>

                            </table>

                        </div>

                    )}

                </div>

            </div>

        </div>

    );
}