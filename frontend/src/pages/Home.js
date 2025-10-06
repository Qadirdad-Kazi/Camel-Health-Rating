import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../contexts/AuthContext';
import { predictionAPI } from '../services/api';
import ImageUploadCard from '../components/ImageUploadCard';
import { Camera, Zap, Shield, BarChart3 } from 'lucide-react';

const Home = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleImageSelect = (file) => {
    setSelectedFile(file);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      toast.error('Please select an image first');
      return;
    }

    setLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = isAuthenticated 
        ? await predictionAPI.predict(formData)
        : await predictionAPI.predictAnonymous(formData);

      const imageId = response.data.id;
      navigate(`/results/${imageId}`);
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error(error.response?.data?.detail || 'Failed to analyze image');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-camel-50 via-white to-desert-50">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              AI-Powered
              <span className="text-gradient block">Camel Rating System</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Upload a camel image and get instant AI-powered analysis with detailed ratings 
              and feature breakdowns. Our advanced machine learning model evaluates multiple 
              characteristics to provide comprehensive assessments.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
              <div className="flex items-center space-x-2 text-camel-600">
                <Zap className="w-5 h-5" />
                <span className="font-medium">Instant Analysis</span>
              </div>
              <div className="flex items-center space-x-2 text-camel-600">
                <Shield className="w-5 h-5" />
                <span className="font-medium">Secure & Private</span>
              </div>
              <div className="flex items-center space-x-2 text-camel-600">
                <BarChart3 className="w-5 h-5" />
                <span className="font-medium">Detailed Reports</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div>
            <ImageUploadCard 
              onImageSelect={handleImageSelect}
              loading={loading}
            />
            
            {selectedFile && (
              <div className="mt-6">
                <button
                  onClick={handleAnalyze}
                  disabled={loading}
                  className="w-full btn-primary text-lg py-3 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <div className="flex items-center justify-center space-x-2">
                      <div className="loading-spinner"></div>
                      <span>Analyzing...</span>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center space-x-2">
                      <Camera className="w-5 h-5" />
                      <span>Analyze Camel Image</span>
                    </div>
                  )}
                </button>
              </div>
            )}
          </div>

          {/* Features Section */}
          <div className="space-y-6">
            <div className="card p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                How It Works
              </h3>
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-camel-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-camel-600 font-bold text-sm">1</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Upload Image</h4>
                    <p className="text-sm text-gray-600">
                      Upload a clear photo of a camel (JPEG or PNG, max 10MB)
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-camel-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-camel-600 font-bold text-sm">2</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">AI Analysis</h4>
                    <p className="text-sm text-gray-600">
                      Our advanced ML model analyzes the image in seconds
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-camel-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-camel-600 font-bold text-sm">3</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Get Results</h4>
                    <p className="text-sm text-gray-600">
                      Receive detailed rating and feature breakdown
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="card p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                What We Analyze
              </h3>
              <div className="grid grid-cols-2 gap-3">
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="font-medium text-gray-900">Body Shape</div>
                  <div className="text-xs text-gray-600">Proportions & Structure</div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="font-medium text-gray-900">Head Structure</div>
                  <div className="text-xs text-gray-600">Facial Features</div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="font-medium text-gray-900">Leg Condition</div>
                  <div className="text-xs text-gray-600">Bone Structure</div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="font-medium text-gray-900">Coat Quality</div>
                  <div className="text-xs text-gray-600">Fur Condition</div>
                </div>
              </div>
            </div>

            {!isAuthenticated && (
              <div className="card p-6 bg-gradient-camel text-white">
                <h3 className="text-xl font-bold mb-2">
                  Get More Features
                </h3>
                <p className="text-camel-100 mb-4">
                  Sign up to save your analysis history and track your camel ratings over time.
                </p>
                <div className="flex space-x-3">
                  <a href="/register" className="btn-outline bg-white text-camel-600 hover:bg-gray-100">
                    Sign Up
                  </a>
                  <a href="/login" className="text-camel-100 hover:text-white">
                    Login
                  </a>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
