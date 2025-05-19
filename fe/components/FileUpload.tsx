"use client";
import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import * as XLSX from 'xlsx';
import { useRouter } from 'next/router';
import axios from 'axios';

export default function FileUpload() {
  const [fileName, setFileName] = useState('');
  const [fileObj, setFileObj] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const [recordCount, setRecordCount] = useState(0);
  const [featureCount, setFeatureCount] = useState(0);
  const [columns, setColumns] = useState<string[]>([]);
  const [selectedId, setSelectedId] = useState('');
  const router = useRouter();

  const onDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setFileName(file.name);
      setFileObj(file);

      const reader = new FileReader();
      reader.onload = (e) => {
        const data = new Uint8Array(e.target?.result as ArrayBuffer);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(firstSheet, { header: 1 });
        const rows = jsonData as string[][];

        if (rows.length > 1) {
          setColumns(rows[0] as string[]);
          setRecordCount(rows.length - 1);
          setFeatureCount((rows[0] as string[]).length);
          setSelectedId((rows[0] as string[])[0]);
        }
      };
      reader.readAsArrayBuffer(file);
    }
  };

  const handleUpload = async () => {
    if (!fileObj || !selectedId) return;
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', fileObj);
      formData.append('identifier', selectedId);
      const res = await axios.post('http://localhost:8000/upload', formData);
      console.log("✅ Uploaded", res.data);
      setUploaded(true);
    } catch (err) {
      console.error("Upload error:", err);
    }
    setUploading(false);
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop, accept: { 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'] } });

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-md space-y-6">
      <h1 className="text-3xl font-bold text-gray-800 text-center">GoldenRecord</h1>
      <p className="text-center text-gray-600 -mt-4">Entity Matching System</p>

      <h2 className="text-xl font-semibold">File Uploading</h2>

      <div {...getRootProps()} className="border-2 border-dashed rounded-md p-6 text-center cursor-pointer hover:border-pink-400 transition-colors">
        <input {...getInputProps()} />
        <p className="text-gray-500">Drag & drop your .xlsx file here, or click to browse</p>
      </div>

      {fileName && !uploading && <p className="text-center text-sm text-gray-600 font-medium">{fileName}</p>}

      <div className="flex justify-center">
        <button
          onClick={handleUpload}
          className="bg-pink-500 text-white px-6 py-2 rounded hover:bg-pink-600 transition"
        >
          Upload
        </button>
      </div>

      {uploading && (
        <div className="w-full bg-gray-200 rounded h-2">
          <div className="w-full bg-pink-500 h-2 animate-pulse"></div>
        </div>
      )}

      {uploaded && (
        <p className="text-center text-green-600 font-semibold">
          ✅ {fileName} successfully uploaded!
        </p>
      )}

      {uploaded && (
        <div className="mt-4 space-y-2">
          <p className="text-gray-800">Total records: <span className="font-semibold">{recordCount}</span></p>
          <p className="text-gray-800">Total features: <span className="font-semibold">{featureCount}</span></p>

          <label className="block font-medium mt-2">Entity Identifier:</label>
          <select
            className="w-full border rounded px-3 py-2"
            value={selectedId}
            onChange={(e) => setSelectedId(e.target.value)}
          >
            {columns.map((col, idx) => (
              <option key={idx} value={col}>{col}</option>
            ))}
          </select>
        </div>
      )}

      {uploaded && (
        <div className="flex justify-center mt-6">
          <button
            onClick={() => router.push('/confirm')}
            className="bg-pink-600 text-white px-6 py-2 rounded hover:bg-pink-700 transition"
          >
            Continue
          </button>
        </div>
      )}
    </div>
  );
}