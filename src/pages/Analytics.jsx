import {
  Pie
} from "react-chartjs-2";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function Analytics() {
  // Dummy data (later can be replaced with backend stats)
  const data = {
    labels: ["Churn", "Not Churn"],
    datasets: [
      {
        label: "Customers",
        data: [35, 65],
        backgroundColor: ["#ef4444", "#22c55e"],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-2">
        Analytics Dashboard
      </h1>

      <p className="text-gray-400 mb-8">
        Visual insights of customer churn predictions.
      </p>

      <div className="glass rounded-3xl p-8 max-w-3xl">

        <h2 className="text-xl font-semibold mb-6">
          Churn Distribution
        </h2>

        <div className="w-full max-w-md mx-auto">
          <Pie data={data} />
        </div>

      </div>

      {/* Extra Info Card */}
      <div className="glass rounded-3xl p-6 mt-8">
        <h2 className="text-lg font-semibold mb-2">
          Insights
        </h2>

        <ul className="text-gray-400 space-y-2 list-disc ml-6">
          <li>Higher churn indicates customer dissatisfaction</li>
          <li>Contract type strongly affects churn rate</li>
          <li>Monthly charges correlate with churn probability</li>
        </ul>
      </div>

    </div>
  );
}