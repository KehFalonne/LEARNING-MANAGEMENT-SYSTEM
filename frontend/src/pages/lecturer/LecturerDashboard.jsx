import { useAuth } from "../../context/AuthContext";

export default function LecturerDashboard() {
    const { user, logout } = useAuth();

    return (
        <div className="container-fluid py-4">

            <div className="d-flex justify-content-between align-items-center mb-4">

                <div>
                    <h2 className="fw-bold mb-1">
                        Lecturer Dashboard
                    </h2>

                    <p className="text-muted mb-0">
                        Welcome back, {user?.first_name}
                    </p>
                </div>

                <button
                    className="btn btn-outline-danger"
                    onClick={logout}
                >
                    Logout
                </button>

            </div>

            <div className="row g-4">

                <div className="col-md-3">
                    <div className="card border-0 shadow-sm">
                        <div className="card-body">
                            <h6 className="text-muted">
                                My Courses
                            </h6>

                            <h2 className="fw-bold">
                                0
                            </h2>
                        </div>
                    </div>
                </div>

                <div className="col-md-3">
                    <div className="card border-0 shadow-sm">
                        <div className="card-body">
                            <h6 className="text-muted">
                                Students
                            </h6>

                            <h2 className="fw-bold">
                                0
                            </h2>
                        </div>
                    </div>
                </div>

                <div className="col-md-3">
                    <div className="card border-0 shadow-sm">
                        <div className="card-body">
                            <h6 className="text-muted">
                                Assignments
                            </h6>

                            <h2 className="fw-bold">
                                0
                            </h2>
                        </div>
                    </div>
                </div>

                <div className="col-md-3">
                    <div className="card border-0 shadow-sm">
                        <div className="card-body">
                            <h6 className="text-muted">
                                Pending Grading
                            </h6>

                            <h2 className="fw-bold">
                                0
                            </h2>
                        </div>
                    </div>
                </div>

            </div>

        </div>
    );
}