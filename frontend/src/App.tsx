import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LanguageProvider } from "./context/LanguageContext";
import Navbar from "./components/Navbar";
import OfflineBanner from "./components/OfflineBanner";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";

import MotherDashboard from "./pages/MotherDashboard";
import MotherProfile from "./pages/MotherProfile";
import MotherAppointments from "./pages/MotherAppointments";
import NurseDashboard from "./pages/NurseDashboard";
import NurseProfile from "./pages/NurseProfile";

import Chat from "./pages/Chat";
import SymptomTracker from "./pages/SymptomTracker";

function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/MotherDashboard" element={<MotherDashboard />} />
        <Route path="/motherprofile" element={<MotherProfile />} />
        <Route path="/motherappointments" element={<MotherAppointments />} />
        <Route path="/NurseDashboard" element={<NurseDashboard />} />
        <Route path="/nurse-profile" element={<NurseProfile />} />

        <Route path="/chat" element={<Chat />} />
        <Route path="/symptom-tracker" element={<SymptomTracker />} />
      </Routes>
        </BrowserRouter>
        <OfflineBanner />
    </LanguageProvider>
  );
}

export default App;
