import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Image as ImageIcon, AlertCircle, CheckCircle, X } from 'lucide-react';

const ImageUploadCard = ({ onImageSelect, loading = false }) => {
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    setError(null);
    
    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0];
      if (rejection.errors[0].code === 'file-too-large') {
        setError('File size must be less than 10MB');
      } else if (rejection.errors[0].code === 'file-invalid-type') {
        setError('Please upload a JPEG or PNG image');
      } else {
        setError('Invalid file type');
      }
      return;
    }

    const file = acceptedFiles[0];
    if (file) {
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
      };
      reader.readAsDataURL(file);
      
      onImageSelect(file);
    }
  }, [onImageSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: false
  });

  const clearPreview = () => {
    setPreview(null);
    setError(null);
  };

  return (
    <div className="card p-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Upload Camel Image
        </h2>
        <p className="text-gray-600">
          Upload a clear image of a camel to get an AI-powered rating and analysis
        </p>
      </div>

      {!preview ? (
        <div
          {...getRootProps()}
          className={`upload-area ${isDragActive ? 'dragover' : ''} ${
            loading ? 'pointer-events-none opacity-50' : 'cursor-pointer'
          }`}
        >
          <input {...getInputProps()} />
          <div className="flex flex-col items-center space-y-4">
            <div className="w-16 h-16 bg-camel-100 rounded-full flex items-center justify-center">
              {loading ? (
                <div className="loading-spinner"></div>
              ) : (
                <Upload className="w-8 h-8 text-camel-600" />
              )}
            </div>
            
            {isDragActive ? (
              <div>
                <p className="text-lg font-medium text-camel-600">
                  Drop the image here...
                </p>
              </div>
            ) : (
              <div>
                <p className="text-lg font-medium text-gray-700 mb-2">
                  Drag & drop your camel image here
                </p>
                <p className="text-sm text-gray-500">
                  or click to browse files
                </p>
              </div>
            )}
            
            <div className="text-xs text-gray-400">
              Supports JPEG, PNG • Max 10MB
            </div>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="relative">
            <img
              src={preview}
              alt="Preview"
              className="w-full h-64 object-cover rounded-lg border border-gray-200"
            />
            <button
              onClick={clearPreview}
              className="absolute top-2 right-2 bg-white rounded-full p-2 shadow-lg hover:bg-gray-50 transition-colors duration-200"
              disabled={loading}
            >
              <X className="w-4 h-4 text-gray-600" />
            </button>
          </div>
          
          <div className="flex items-center space-x-2 text-green-600">
            <CheckCircle className="w-5 h-5" />
            <span className="text-sm font-medium">Image ready for analysis</span>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 text-red-500" />
          <span className="text-sm text-red-700">{error}</span>
        </div>
      )}

      {loading && (
        <div className="mt-4 p-4 bg-camel-50 border border-camel-200 rounded-lg">
          <div className="flex items-center space-x-3">
            <div className="loading-spinner"></div>
            <div>
              <p className="text-sm font-medium text-camel-800">
                Analyzing your camel image...
              </p>
              <p className="text-xs text-camel-600">
                This may take a few seconds
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUploadCard;
