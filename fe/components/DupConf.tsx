import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { getPairs, sendFeedback } from '../lib/api';

export default function DupConf() {
  const [pairs, setPairs] = useState<any[]>([]);
  const [decisions, setDecisions] = useState<{ [key: string]: string }>({});
  const router = useRouter();

  useEffect(() => {
    const fetchPairs = async () => {
      try {
        const data = await getPairs();
        console.log("✅ API /predict result:", data);
        const suspicious = data?.suspicious_pairs || [];
        setPairs(suspicious);
        const defaultDecisions: { [key: string]: string } = {};
        suspicious.forEach((p: any) => {
          const key = `${p.id1}-${p.id2}`;
          defaultDecisions[key] = 'Undecided';
        });
        setDecisions(defaultDecisions);
      } catch (err) {
        console.error("❌ Failed to load suspicious_pairs", err);
      }
    };
    fetchPairs();
  }, []);

  const handleDecisionChange = (key: string, value: string) => {
    setDecisions(prev => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async () => {
    const feedbackList = Object.entries(decisions).map(([key, value]) => {
      const [id1, id2] = key.split('-').map(Number);
      return { id1, id2, decision: value };
    });
    await sendFeedback({ feedback: feedbackList });
    router.push('/report');
  };

  return (
    <div className="max-w-6xl mx-auto p-6 bg-white rounded-xl shadow-md space-y-6">
      <h1 className="text-3xl font-bold text-gray-800 text-center">GoldenRecord</h1>
      <p className="text-center text-gray-600 -mt-4">Entity Matching System</p>

      <h2 className="text-xl font-semibold mt-6">Duplicate Confirmation</h2>

      <table className="w-full table-auto border-collapse border border-gray-300 mt-4 text-sm">
        <thead className="bg-gray-100">
          <tr>
            <th className="border border-gray-300 px-2 py-1">No.</th>
            <th className="border border-gray-300 px-2 py-1">Pair</th>
            <th className="border border-gray-300 px-2 py-1">Entity 1</th>
            <th className="border border-gray-300 px-2 py-1">Entity 2</th>
            <th className="border border-gray-300 px-2 py-1">Decision</th>
          </tr>
        </thead>
        <tbody>
          {pairs.map((pair, idx) => {
            const key = `${pair.id1}-${pair.id2}`;
            return (
              <tr key={key} className="text-center">
                <td className="border border-gray-300 px-2 py-1">{idx + 1}</td>
                <td className="border border-gray-300 px-2 py-1 font-semibold">
                  {pair.name1} ↔ {pair.name2}
                </td>
                <td className="border border-gray-300 px-2 py-1 text-left">
                  <ul>
                    {Object.entries(pair.entity1).map(([k, v], i) => (
                      <li key={i}><strong>{k}:</strong> {v}</li>
                    ))}
                  </ul>
                </td>
                <td className="border border-gray-300 px-2 py-1 text-left">
                  <ul>
                    {Object.entries(pair.entity2).map(([k, v], i) => (
                      <li key={i}><strong>{k}:</strong> {v}</li>
                    ))}
                  </ul>
                </td>
                <td className="border border-gray-300 px-2 py-1">
                  <div className="flex flex-col gap-1 items-center">
                    {['Undecided', 'Yes', 'No'].map(opt => (
                      <label key={opt} className="text-sm">
                        <input
                          type="radio"
                          name={key}
                          value={opt}
                          checked={decisions[key] === opt}
                          onChange={() => handleDecisionChange(key, opt)}
                          className="mr-1"
                        />
                        {opt}
                      </label>
                    ))}
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      <div className="flex justify-center mt-6">
        <button
          onClick={handleSubmit}
          className="bg-pink-600 text-white px-6 py-2 rounded hover:bg-pink-700 transition"
        >
          Continue
        </button>
      </div>
    </div>
  );
}