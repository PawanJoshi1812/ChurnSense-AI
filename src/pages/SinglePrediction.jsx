import { useState } from "react";
import { predictChurn } from "../services/api";

export default function SinglePrediction() {
  const [form, setForm] = useState({
    tenure: "",
    monthlyCharges: "",
    totalCharges: "",
    supportTickets: "",
    contract: "Month-to-month",
    paymentDelay: "",
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);

    try {
      const payload = {
  features: [
    Number(form.tenure || 0),
    Number(form.monthlyCharges || 0),
    Number(form.totalCharges || 0),
    Number(0),
    form.contract === "Month-to-month" ? 0 :
    form.contract === "One year" ? 1 : 2,
    Number(0)
  ]
};

     const res = await predictChurn(payload);
      console.log("Single Prediction Response:", res.data);
      setResult(res.data);
    } catch (error) {
  console.log("FULL ERROR:", error.response?.data);
  console.log("STATUS:", error.response?.status);
  console.log("MESSAGE:", error.message);

  setResult({
    error: JSON.stringify(error.response?.data || error.message),
  });
} finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-2">
        Single Prediction
      </h1>

      <p className="text-gray-400 mb-8">
        Enter customer details to predict churn.
      </p>

      <div className="glass rounded-3xl p-8 max-w-4xl">

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          <div>
            <label className="text-sm">Tenure</label>
            <input
              type="number"
              name="tenure"
              value={form.tenure}
              onChange={handleChange}
              className="w-full bg-white/10 p-3 rounded-xl"
              placeholder="Months"
            />
          </div>

          <div>
            <label className="text-sm">Monthly Charges</label>
            <input
              type="number"
              name="monthlyCharges"
              value={form.monthlyCharges}
              onChange={handleChange}
              className="w-full bg-white/10 p-3 rounded-xl"
              placeholder="75.30"
            />
          </div>

          <div>
            <label className="text-sm">Total Charges</label>
            <input
              type="number"
              name="totalCharges"
              value={form.totalCharges}
              onChange={handleChange}
              className="w-full bg-white/10 p-3 rounded-xl"
              placeholder="570.45"
            />
          </div>

          <div>
            <label className="text-sm">Support Tickets</label>
            <input
              type="number"
              name="supportTickets"
              value={form.supportTickets}
              onChange={handleChange}
              className="w-full bg-white/10 p-3 rounded-xl"
              placeholder="2"
            />
          </div>

          <div>
            <label className="text-sm">Payment Delay</label>
            <input
              type="number"
              name="paymentDelay"
              value={form.paymentDelay}
              onChange={handleChange}
              className="w-full bg-white/10 p-3 rounded-xl"
              placeholder="3"
            />
          </div>

          <div>
            <label className="text-sm">Contract Type</label>
            <select
              name="contract"
              value={form.contract}
              onChange={handleChange}
              className="w-full bg-white/10 p-3 rounded-xl"
            >
              <option>Month-to-month</option>
              <option>One year</option>
              <option>Two year</option>
            </select>
          </div>

        </div>

        <button
          onClick={handlePredict}
          disabled={loading}
          className="mt-8 bg-indigo-600 hover:bg-indigo-700 px-8 py-3 rounded-xl font-semibold"
        >
          {loading ? "Predicting..." : "Predict Churn"}
        </button>

        <div className="glass rounded-2xl p-6 mt-8">
          <p className="text-gray-400">
            Prediction Result
          </p>

          {result ? (
            result.error ? (
              <h2 className="text-red-400 mt-2">
                {result.error}
              </h2>
            ) : (
              <div className="mt-4">
                <h2
                  className={`text-3xl font-bold ${
                    result.prediction === 1
                      ? "text-red-400"
                      : "text-green-400"
                  }`}
                >
                  {result.prediction === 1
                    ? "Churn"
                    : "Not Churn"}
                </h2>

                {result.churn_probability !== undefined && (
                  <p className="mt-2 text-gray-300">
                    Probability: {result.churn_probability}
                  </p>
                )}
              </div>
            )
          ) : (
            <h2 className="text-2xl mt-2">
              No prediction yet
            </h2>
          )}
        </div>

      </div>
    </div>
  );
}