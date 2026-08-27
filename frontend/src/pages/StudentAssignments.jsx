import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api from "../api/axios";

export default function StudentAssignments() {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchAssignments = async () => {
      try {
        const response = await api.get("/assignments/student/");

        setAssignments(response.data);
    } catch (error) {
        console.error("ASSIGNMENT ERROR:", error);
        console.error("STATUS:", error.response?.status);
        console.error("DATA:", error.response?.data);

        setError(
            error.response?.data?.detail ||
            `Unable to load assignments. Status: ${
                error.response?.status || "Unknown"
            }`
        );
    }finally {
        setLoading(false);
      }
    };

    fetchAssignments();
  }, []);

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container py-5">
        <div className="alert alert-danger">{error}</div>
      </div>
    );
  }

  return (
    <div className="container-fluid py-4">
      {/* HEADER */}

      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold mb-1">My Assignments</h2>

          <p className="text-muted mb-0">
            View and submit your course assignments.
          </p>
        </div>

        <Link to="/dashboard" className="btn btn-outline-secondary">
          Back to Dashboard
        </Link>
      </div>

      {/* ASSIGNMENTS */}

      {assignments.length === 0 ? (
        <div className="card border-0 shadow-sm">
          <div className="card-body text-center py-5">
            <i className="bi bi-clipboard-check fs-1 text-muted"></i>

            <h4 className="mt-3">No Assignments Available</h4>

            <p className="text-muted mb-0">
              You currently have no published assignments.
            </p>
          </div>
        </div>
      ) : (
        <div className="row g-4">
          {assignments.map((assignment) => (
            <div className="col-md-6 col-xl-4" key={assignment.id}>
              <div className="card border-0 shadow-sm h-100">
                <div className="card-body d-flex flex-column">
                  <div className="d-flex justify-content-between mb-3">
                    <span className="badge text-bg-primary">
                      {assignment.course_code}
                    </span>

                    {assignment.submitted ? (
                      <span className="badge text-bg-success">
                        {assignment.submission_status}
                      </span>
                    ) : (
                      <span className="badge text-bg-warning">
                        Not Submitted
                      </span>
                    )}
                  </div>

                  <h5 className="fw-bold">{assignment.title}</h5>

                  <p className="text-muted small">{assignment.course_title}</p>

                  <p className="text-muted">{assignment.instructions}</p>

                  <div className="mt-auto">
                    <hr />

                    <small className="d-block mb-2">
                      <strong>Due:</strong>{" "}
                      {new Date(assignment.due_date).toLocaleString()}
                    </small>

                    <small className="d-block mb-3">
                      <strong>Marks:</strong> {assignment.total_marks}
                    </small>

                    <Link
                      to={`/assignments/${assignment.id}`}
                      className="btn btn-primary w-100"
                    >
                      View Assignment
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
