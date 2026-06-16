export default function Dashboard() {
  const stats = [
    { label: "Total Customers", value: 1000 },
    { label: "Churned Customers", value: 320 },
    { label: "Retained Customers", value: 680 },
    { label: "Churn Rate", value: "32%" },
  ];

  return (
    <div className="min-h-screen p-6 text-white bg-black">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((item, index) => (
          <div
            key={index}
            className="p-4 bg-gray-900 rounded-xl shadow-lg"
          >
            <h2 className="text-gray-400">{item.label}</h2>
            <p className="text-2xl font-bold mt-2">{item.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}