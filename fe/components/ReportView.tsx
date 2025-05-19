import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function ReportView() {
  const [stats, setStats] = useState({ golden_records: 0, duplicates: 0, low_certainty: 0 });
  const [shapImage, setShapImage] = useState('');

  useEffect(() => {
    const fetchStats = async () => {
      const res = await axios.get('http://localhost:8000/report/stats');
      setStats(res.data);
    };
    const fetchShap = async () => {
      const res = await axios.get('http://localhost:8000/report/shap', { responseType: 'blob' });
      const url = URL.createObjectURL(res.data);
      setShapImage(url);
    };
    fetchStats();
    fetchShap();
  }, []);

  const handleDownload = async () => {
    const res = await axios.get('http://localhost:8000/report', { responseType: 'blob' });
    const blob = new Blob([res.data], { type: res.headers['content-type'] });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'golden_record.xlsx';
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-xl shadow-md space-y-6">
      <h1 className="text-3xl font-bold text-gray-800 text-center">GoldenRecord</h1>
      <p className="text-center text-gray-600 -mt-4">Entity Matching System</p>

      <h2 className="text-xl font-semibold mt-6">Report</h2>

      <div className="grid grid-cols-3 gap-4 text-center text-lg font-medium">
        <div className="bg-gray-100 rounded p-4">
          <p>🧬 Golden Records</p>
          <p className="text-2xl text-pink-600 font-bold">{stats.golden_records}</p>
        </div>
        <div className="bg-gray-100 rounded p-4">
          <p>🔁 Duplicates</p>
          <p className="text-2xl text-pink-600 font-bold">{stats.duplicates}</p>
        </div>
        <div className="bg-gray-100 rounded p-4">
          <p>❓ Low Certainty</p>
          <p className="text-2xl text-pink-600 font-bold">{stats.low_certainty}</p>
        </div>
      </div>

      <h3 className="text-lg font-semibold mt-6">Feature Importance (SHAP)</h3>
      {shapImage && <img src={shapImage} alt="SHAP Beeswarm Plot" className="w-full max-h-[400px] object-contain" />}

      <div className="flex justify-center gap-4 mt-6">
        <button onClick={handleDownload} className="bg-pink-600 text-white px-6 py-2 rounded hover:bg-pink-700 transition">Export Report</button>
        <button onClick={() => window.location.href = '/'} className="bg-gray-300 text-gray-800 px-6 py-2 rounded hover:bg-gray-400 transition">Redo</button>
      </div>
    </div>
  );
}