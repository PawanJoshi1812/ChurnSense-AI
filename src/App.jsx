import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import SinglePrediction from "./pages/SinglePrediction";
import BulkPrediction from "./pages/BulkPrediction";
import Sidebar from "./components/Sidebar";

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex">
        <Sidebar />

        <div className="flex-1">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/single" element={<SinglePrediction />} />
            <Route path="/bulk" element={<BulkPrediction />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}