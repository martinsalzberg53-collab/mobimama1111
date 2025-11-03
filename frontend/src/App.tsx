import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import MotherDashboard from "./pages/MotherDashboard"
import NurseDashboard from "./pages/NurseDashboard"

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/motherdashboard" element={<MotherDashboard/>} />
        <Route path="/nursedashboard" element={<NurseDashboard/>} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
