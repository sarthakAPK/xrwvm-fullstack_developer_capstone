import LoginPanel from "./components/Login/Login";
import RegisterPanel from "./components/Register/Register"; // Add this import
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<RegisterPanel />} /> {/* Add this line */}
    </Routes>
  );
}

export default App;
