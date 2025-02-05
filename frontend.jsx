import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", selectedFile);
    
    try {
      const response = await axios.post("http://127.0.0.1:8000/detect/", formData, {
        responseType: "blob",
      });
      setProcessedImage(URL.createObjectURL(response.data));
    } catch (error) {
      console.error("Error uploading file:", error);
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">Gesture-Based Hand Drawing</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} className="mb-4" />
      <button
        onClick={handleUpload}
        className="px-4 py-2 bg-blue-500 text-white rounded"
        disabled={loading}
      >
        {loading ? "Processing..." : "Upload & Detect"}
      </button>
      {processedImage && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold">Processed Image:</h2>
          <img src={processedImage} alt="Processed" className="mt-2 rounded shadow" />
        </div>
      )}
    </div>
  );
}
