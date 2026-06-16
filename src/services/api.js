import axios from "axios";

const API = axios.create({
  baseURL: "https://churnsense-ai-i01u.onrender.com",
});

// Single Prediction
export const predictChurn = (data) => {
  return API.post("/predict", {
    features: [
      Number(data.tenure),
      Number(data.monthly_charges),
      Number(data.total_charges),
      Number(data.support_tickets),
      Number(data.contract_type),
      Number(data.payment_delay),
    ],
  });
};

// Bulk Prediction
export const bulkPredict = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return API.post("/upload", formData);
};

// Prediction History
export const getHistory = () => {
  return API.get("/history");
};

// Explain Prediction
export const explainPrediction = (data) => {
  return API.post("/explain", data);
};

export default API;