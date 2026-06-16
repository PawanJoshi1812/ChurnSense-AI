import axios from "axios";

const API = axios.create({
  baseURL: "https://churnsense-ai-i01u.onrender.com",
});

// SINGLE PREDICTION
export const predictChurn = (data) => {
  return API.post("/predict", data);
};

// BULK PREDICTION
export const bulkPredict = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return API.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

// HISTORY (NEW)
export const getHistory = () => {
  return API.get("/history");
};