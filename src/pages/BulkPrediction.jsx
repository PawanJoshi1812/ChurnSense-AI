import { useState } from "react";
import { bulkPredict } from "../services/api";

export default function BulkPrediction() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const res = await bulkPredict(file);
      console.log("API RESPONSE:", res.data);

      setResult(res.data);
    } catch (err) {
      console.log("ERROR:", err);
      setError(
        err?.response?.data?.message ||
        err?.message ||
        "Bulk prediction failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-2">
        Bulk Prediction
      </h1>

      <p className="text-gray-400 mb-8">
        Upload CSV file for batch churn prediction.
      </p>

      <div className="glass rounded-3xl p-8 max-w-5xl">

        {/* UPLOAD SECTION */}
        <div className="border border-white/20 rounded-2xl p-8 text-center">

          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            className="hidden"
            id="fileUpload"
          />

          <label
            htmlFor="fileUpload"
            className="cursor-pointer inline-block bg-indigo-600 hover:bg-indigo-700 px-6 py-3 rounded-xl font-semibold"
          >
            Choose CSV File
          </label>

          {file && (
            <p className="mt-4 text-gray-300">
              Selected File: <b>{file.name}</b>
            </p>
          )}
        </div>

        {/* BUTTON */}
        <button
          onClick={handleUpload}
          disabled={loading}
          className="mt-8 bg-indigo-600 hover:bg-indigo-700 px-8 py-3 rounded-xl font-semibold"
        >
          {loading ? "Processing..." : "Run Bulk Prediction"}
        </button>

        {/* ERROR */}
        {error && (
          <div className="mt-6 p-4 bg-red-500/20 text-red-300 rounded-xl">
            {error}
          </div>
        )}

        {/* RESULT TABLE */}
        {result?.sample_output && (
          <div className="mt-8 glass rounded-2xl p-6">
            <h2 className="text-xl font-semibold mb-4">
              Prediction Results
            </h2>

            <div className="overflow-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="text-gray-400 border-b border-white/10">
                    <th className="py-2">Customer</th>
                    <th className="py-2">Prediction</th>
                    <th className="py-2">Probability</th>
                  </tr>
                </thead>

                <tbody>
                  {result.sample_output.map((item, index) => (
                    <tr key={index} className="border-b border-white/10">
                      <td className="py-2">#{index + 1}</td>

                      <td className="py-2">
                        <span
                          className={
                            item.prediction === 1
                              ? "text-red-400 font-semibold"
                              : "text-green-400 font-semibold"
                          }
                        >
                          {item.prediction === 1
                            ? "Churn"
                            : "Not Churn"}
                        </span>
                      </td>

                      <td className="py-2 text-gray-300">
                        {item.churn_probability}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* RAW FALLBACK VIEW */}
        {result && !result.sample_output && (
          <pre className="mt-8 text-sm text-gray-300 overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}

      </div>
    </div>
  );
}