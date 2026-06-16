import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="w-64 min-h-screen bg-gray-900 text-white p-4">
      <h1 className="text-xl font-bold mb-6">ChurnSense AI</h1>

      <nav className="flex flex-col gap-4">
        <Link to="/" className="hover:text-blue-400">Dashboard</Link>
        <Link to="/single" className="hover:text-blue-400">Single Prediction</Link>
        <Link to="/bulk" className="hover:text-blue-400">Bulk Prediction</Link>
      </nav>
    </div>
  );
}