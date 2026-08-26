import { useAuth } from "../../context/AuthContext";

export default function AdminDashboard() {
    const { user, logout } = useAuth();

    return (
        <div className="container-fluid py-4">

            <div className="d-flex justify-content-between align-items-center mb-4">

                <div>
                    <h2 className="fw-bold mb-1">
                        Administration Dashboard
                    </h2>

                    <p className="text-muted mb-0">
                        Welcome, {user?.first_name}
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
                                Lecturers
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
                                Programmes
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
                                Courses
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