import React, { createContext, useContext, useState, type ReactNode } from "react";

// Define what a User looks like
type User = {
  id: number;
  username: string;
  email: string;
  role: 'mother' | 'nurse';
  clinic?: string | null;
  token: string;
};

// Define what the context will provide
type UserContextType = {
  user: User | null;
  login: (userData: User) => void;
  logout: () => void;
};

// Create the context
const UserContext = createContext<UserContextType | undefined>(undefined);

// Provider component to wrap the app
export const UserProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = (userData: User) => {
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};

// Hook for easy access
export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) throw new Error("useUser must be used inside UserProvider");
  return context;
};
