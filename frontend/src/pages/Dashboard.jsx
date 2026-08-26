import { Navigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

import StudentDashboard from "./student/StudentDashboard";
import LecturerDashboard from "./lecturer/LecturerDashboard";
import AdminDashboard from "./admin/AdminDashboard";
import StaffDashboard from "./staff/StaffDashboard";


export default function Dashboard() {
    const { user } = useAuth();

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    switch (user.role) {

        case "STUDENT":
            return <StudentDashboard />;

        case "LECTURER":
            return <LecturerDashboard />;

        case "ADMIN":
            return <AdminDashboard />;

        case "STAFF":
            return <StaffDashboard />;

        default:
            return (
                <div className="container py-5">
                    <div className="alert alert-danger">
                        Your account does not have a valid
                        university role.
                    </div>
                </div>
            );
    }
}