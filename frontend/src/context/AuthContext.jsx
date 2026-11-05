import React, { useState, useEffect, createContext } from "react";
import { setToken, getToken, removeToken } from "../api/token";
import { useUser } from "../hooks/useUser";

// 1. Crear el contexto
export const AuthContext = createContext({
  auth: undefined,
  login: () => null,
  logout: () => null,
});

// 2. Crear el provider
export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(undefined);
  const { getMe } = useUser();

  useEffect(() => {
    const token = getToken();
    if (!token) {
      setAuth(null);
    } else {
      login(token);
    }
  }, []);

  const login = async (token) => {
    try {
      setToken(token);
      const me = await getMe(token);
      setAuth({ token, me });
    } catch (error) {
      removeToken();
      setAuth(null);
    }
  };

  const logout = () => {
    if (auth) {
      setAuth(null);
      removeToken();
    }
  };

  const valueContext = {
    auth,
    login,
    logout,
  };

  if (auth === undefined) return null;

  return (
    <AuthContext.Provider value={valueContext}>{children}</AuthContext.Provider>
  );
}
