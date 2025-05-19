import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';

export default function FileUpload() {
  const [fileName, setFileName] = useState('');
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);

  const onDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFileName(acceptedFiles[0].name);
      setUploading(true);
      setTimeout(() => {
        setUploading(false);
        setUploaded(true);
      }, 1500);
    }
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div className="p-6 max-w-xl mx-auto space-y-4 bg-white rounded-xl shadow-md">
      <h2 className="text-xl font-bold">File Upload</h2>
      <div {...getRootProps()} className="border-dashed border-2 p-6 rounded-md text-center cursor-pointer">
        <input {...getInputProps()} />
        <p>Drag & drop your file here, or click to browse</p>
      </div>
      {fileName && <p className="text-gray-600 font-semibold">{fileName}</p>}
      <button
        onClick={() => setUploading(true)}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Upload
      </button>
      {uploading && <div className="w-full bg-gray-200 h-2 rounded"><div className="w-full bg-blue-500 h-2 animate-pulse"></div></div>}
      {uploaded && <p className="text-green-600 font-medium">✅ {fileName} successfully uploaded!</p>}
      <div className="mt-4">
        <p>Total records: 275</p>
        <p>Total features: 15</p>
        <label className="block mt-2">Entity Identifier:</label>
        <select className="border px-2 py-1 rounded w-full">
          <option>First Name</option>
          <option>Last Name</option>
          <option>ID Number</option>
        </select>
      </div>
      <button className="mt-4 w-full bg-green-600 text-white py-2 rounded hover:bg-green-700">Continue</button>
    </div>
  );
}
