import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";

import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CourseDetail from "./pages/CourseDetail";
import StudentAssignments from "./pages/StudentAssignments";
import AssignmentDetail from "./pages/AssignmentDetail";


function App() {
    return (
        <BrowserRouter>

            <AuthProvider>

                <Routes>

                    <Route
                        path="/login"
                        element={<Login />}
                    />

                    <Route
                        path="/dashboard"
                        element={
                            <ProtectedRoute>
                                <Dashboard />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/"
                        element={
                            <Navigate
                                to="/dashboard"
                                replace
                            />
                        }
                    />
                    
                    <Route
                        path="/courses/:offeringId"
                        element={
                            <ProtectedRoute>
                                <CourseDetail />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/assignments"
                        element={
                            <ProtectedRoute>
                                <StudentAssignments />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/assignments/:assignmentId"
                        element={
                            <ProtectedRoute>
                                <AssignmentDetail />
                            </ProtectedRoute>
                        }
                    />

                </Routes>   



            </AuthProvider>

        </BrowserRouter>
    );
}

export default App;