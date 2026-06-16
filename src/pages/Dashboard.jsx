import { useEffect, useState } from "react";
import { getHistory } from "../services/api";

export default function Dashboard() {
  const [stats, setStats] = useState([
    { title: "Total Predictions", value: "0" },
    { title: "Churn Customers", value: "0" },
    { title: "Retained Customers", value: "0" },
    { title: "Model Accuracy", value: "93%" },
  ]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await getHistory();
        const data = res.data;

        const history = data.history || [];

        const total = history.length;
        const churn = history.filter((h) => h.prediction === "Churn").length;
        const retained = history.filter((h) => h.prediction === "Not Churn").length;

        setStats([
          { title: "Total Predictions", value: total },
          { title: "Churn Customers", value: churn },
          { title: "Retained Customers", value: retained },
          { title: "Model Accuracy", value: "93%" },
        ]);
      } catch (err) {
        console.log("Dashboard error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-2">Dashboard</h1>

      <p className="text-gray-400 mb-8">
        Customer churn insights at a glance.
      </p>

      {loading && (
        <p className="text-gray-400 mb-4">Loading live stats...</p>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        {stats.map((card) => (
          <div key={card.title} className="glass rounded-3xl p-6">
            <p className="text-gray-400 text-sm">{card.title}</p>
            <h2 className="text-4xl font-bold mt-3">{card.value}</h2>
          </div>
        ))}
      </div>

      <div className="glass rounded-3xl p-8 mt-8">
        <h2 className="text-2xl font-semibold mb-4">
          Welcome to ChurnSense AI
        </h2>

        <p className="text-gray-300">
          Use Single Prediction for individual customers and Bulk Prediction for CSV uploads.
          Analytics are now live and connected to backend history.
        </p>
      </div>
    </div>
  );
}