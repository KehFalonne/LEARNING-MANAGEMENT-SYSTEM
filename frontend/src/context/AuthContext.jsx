import {
    createContext,
    useContext,
    useEffect,
    useState,
} from "react";

import api from "../api/axios";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const accessToken = localStorage.getItem("access_token");

    const fetchUser = async () => {
        try {
            const response = await api.get("/auth/me/", {
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                },
            });

            setUser(response.data);
        } catch (error) {
            console.error("Unable to fetch user:", error);

            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");

            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (accessToken) {
            fetchUser();
        } else {
            setLoading(false);
        }
    }, []);

    const login = async (username, password) => {
        const response = await api.post(
            "/auth/login/",
            {
                username,
                password,
            }
        );

        const { access, refresh } = response.data;

        localStorage.setItem("access_token", access);
        localStorage.setItem("refresh_token", refresh);

        const userResponse = await api.get("/auth/me/", {
            headers: {
                Authorization: `Bearer ${access}`,
            },
        });

        setUser(userResponse.data);

        return userResponse.data;
    };

    const logout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                loading,
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}