import { useAuth } from "../../context/AuthContext";

export default function StaffDashboard() {
    const { user, logout } = useAuth();

    return (
        <div className="container-fluid py-4">

            <div className="d-flex justify-content-between align-items-center mb-4">

                <div>
                    <h2 className="fw-bold mb-1">
                        Staff Dashboard
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

            <div className="card border-0 shadow-sm">
                <div className="card-body">
                    <h4>
                        University Administration
                    </h4>

                    <p className="text-muted mb-0">
                        Staff management tools will appear here.
                    </p>
                </div>
            </div>

        </div>
    );
}