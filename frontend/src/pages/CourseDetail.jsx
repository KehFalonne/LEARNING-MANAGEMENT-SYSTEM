import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api, { MEDIA_URL } from "../api/axios";

import { useAuth } from "../context/AuthContext";


export default function CourseDetail() {

    const { offeringId } = useParams();

    const [course, setCourse] = useState(null);
    const [materials, setMaterials] = useState([]);

    const [loading, setLoading] = useState(true);
    const [materialsLoading, setMaterialsLoading] = useState(true);

    const [error, setError] = useState("");
    const [materialsError, setMaterialsError] = useState("");


   useEffect(() => {

    const fetchCourse = async () => {

        try {

            const token = localStorage.getItem(
                "access_token"
            );

            const response = await api.get(
                `/courses/student/${offeringId}/`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
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


    const fetchMaterials = async () => {

        try {

            const token = localStorage.getItem(
                "access_token"
            );

            const response = await api.get(
                `/courses/student/${offeringId}/materials/`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            setMaterials(response.data);

        } catch (error) {

            console.error(error);

            setMaterialsError(
                "Unable to load learning materials."
            );

        } finally {

            setMaterialsLoading(false);

        }
    };


    fetchCourse();
    fetchMaterials();

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
            {/* LEARNING MATERIALS */}

            <div className="card border-0 shadow-sm mb-4">

                <div className="card-body">

                    <div className="d-flex justify-content-between align-items-center mb-4">

                        <div>

                            <h4 className="fw-bold mb-1">

                                <i className="bi bi-file-earmark-text me-2"></i>

                                Learning Materials

                            </h4>

                            <p className="text-muted mb-0">

                                Lecture notes, presentations and
                                other course resources.

                            </p>

                        </div>


                        <span className="badge text-bg-primary">

                            {materials.length} Materials

                        </span>

                    </div>


                    {materialsLoading ? (

                        <div className="text-center py-4">

                            <div
                                className="spinner-border"
                                role="status"
                            >

                                <span className="visually-hidden">
                                    Loading...
                                </span>

                            </div>

                        </div>

                    ) : materialsError ? (

                        <div className="alert alert-danger">

                            {materialsError}

                        </div>

                    ) : materials.length === 0 ? (

                        <div className="text-center py-5">

                            <i className="bi bi-folder2-open fs-1 text-muted"></i>

                            <h5 className="mt-3">
                                No learning materials yet
                            </h5>

                            <p className="text-muted mb-0">

                                Your lecturer has not published
                                any materials for this course yet.

                            </p>

                        </div>

                    ) : (

                        <div className="row g-3">

                            {materials.map((material) => (

                                <div
                                    className="col-md-6"
                                    key={material.id}
                                >

                                    <div className="border rounded p-3 h-100">

                                        <div className="d-flex align-items-start">

                                            <div className="me-3">

                                                <i className="bi bi-file-earmark-text fs-2"></i>

                                            </div>


                                            <div className="flex-grow-1">

                                                <div className="d-flex justify-content-between">

                                                    <h6 className="fw-bold mb-1">

                                                        {material.title}

                                                    </h6>

                                                    {material.week && (

                                                        <span className="badge text-bg-light">

                                                            Week {material.week}

                                                        </span>

                                                    )}

                                                </div>


                                                <span className="badge text-bg-secondary mb-2">

                                                    {material.material_type_display}

                                                </span>


                                                {material.description && (

                                                    <p className="text-muted small mb-3">

                                                        {material.description}

                                                    </p>

                                                )}


                                                <div>

                                                    {material.file && (

                                                        <a
                                                            href={
                                                                material.file?.startsWith("http")
                                                                    ? material.file
                                                                    : `${MEDIA_URL}${material.file}`
                                                            }
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                            className="btn btn-sm btn-outline-primary me-2"
                                                        >

                                                            <i className="bi bi-eye me-1"></i>

                                                            View File

                                                        </a>

                                                    )}


                                                    {material.external_url && (

                                                        <a
                                                            href={material.external_url}
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                            className="btn btn-sm btn-outline-primary"
                                                        >

                                                            <i className="bi bi-box-arrow-up-right me-1"></i>

                                                            Open Link

                                                        </a>

                                                    )}

                                                </div>

                                            </div>

                                        </div>

                                    </div>

                                </div>

                            ))}

                        </div>

                    )}

                </div>

            </div>  


        </div>

    );
}