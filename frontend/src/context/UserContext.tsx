import React, { createContext, useContext, useState, useEffect, type ReactNode } from "react";

// 1. Define your user type
type User = {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: 'MOTHER' | 'NURSE' | 'ADMIN'; // Uppercase
  clinic?: string | null;
};

// 2. Define what the context provides
// We now store 'user' and 'token' separately
type UserContextType = {
  user: User | null;
  token: string | null;
  login: (userData: User, authToken: string) => void; // Accepts two arguments
  logout: () => void;
};

// Create the context
const UserContext = createContext<UserContextType | undefined>(undefined);

// Provider component
export const UserProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true); // For checking auth on load

  // 3. THIS IS THE UPGRADE: Check for a saved user on initial app load
  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    const storedToken = localStorage.getItem("token");

    // If we have both, the user is logged in
    if (storedUser && storedToken) {
      setUser(JSON.parse(storedUser));
      setToken(storedToken);
    }
    setIsLoading(false); // Finished checking, app can now render
  }, []); // The empty [] array means this runs only once when the app starts

  // 4. Updated login function to match our API response
  const login = (userData: User, authToken: string) => {
    setUser(userData);
    setToken(authToken);
    localStorage.setItem("user", JSON.stringify(userData));
    localStorage.setItem("token", authToken); // Save token separately
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("user");
    localStorage.removeItem("token"); // Remove token
  };

  // 5. Don't show the app until we know if the user is logged in
  if (isLoading) {
    return <div>Loading...</div>; // Or a real loading spinner
  }

  return (
    <UserContext.Provider value={{ user, token, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};

// Hook for easy access (this stays the same)
export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) throw new Error("useUser must be used inside UserProvider");
  return context;
};