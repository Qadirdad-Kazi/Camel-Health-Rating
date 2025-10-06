import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { predictionAPI } from '../services/api';
import RatingResultCard from '../components/RatingResultCard';
import FeatureBreakdownCard from '../components/FeatureBreakdownCard';
import { ArrowLeft, Share2, MessageSquare, BarChart3 } from 'lucide-react';

const Results = () => {
  const { imageId } = useParams();
  const navigate = useNavigate();
  const [imageData, setImageData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchImageData = async () => {
      try {
        const data = await predictionAPI.getImageDetails(imageId);
        setImageData(data);
      } catch (error) {
        console.error('Error fetching image data:', error);
        setError('Failed to load image data');
        toast.error('Failed to load image data');
      } finally {
        setLoading(false);
      }
    };

    if (imageId) {
      fetchImageData();
    }
  }, [imageId]);

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Camel Rating Results',
          text: `Check out this camel rating: ${imageData.rating}/10!`,
          url: window.location.href,
        });
      } catch (error) {
        console.log('Error sharing:', error);
      }
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      toast.success('Link copied to clipboard!');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading results...</p>
        </div>
      </div>
    );
  }

  if (error || !imageData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <BarChart3 className="w-8 h-8 text-red-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Results Not Found
          </h2>
          <p className="text-gray-600 mb-6">
            The requested analysis results could not be found.
          </p>
          <Link to="/" className="btn-primary">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Link 
            to="/" 
            className="flex items-center space-x-2 text-gray-600 hover:text-camel-600 transition-colors duration-200"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Home</span>
          </Link>
          
          <div className="flex items-center space-x-3">
            <button
              onClick={handleShare}
              className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-camel-600 transition-colors duration-200"
            >
              <Share2 className="w-4 h-4" />
              <span>Share</span>
            </button>
            
            <Link
              to={`/feedback/${imageId}`}
              className="btn-outline flex items-center space-x-2"
            >
              <MessageSquare className="w-4 h-4" />
              <span>Give Feedback</span>
            </Link>
          </div>
        </div>

        {/* Results Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Main Results */}
          <div>
            <RatingResultCard
              rating={imageData.rating}
              features={imageData.features}
              imageUrl={`http://localhost:8000${imageData.image_url}`}
            />
          </div>

          {/* Detailed Analysis */}
          <div>
            <FeatureBreakdownCard features={imageData.features} />
          </div>
        </div>

        {/* Additional Actions */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card p-6 text-center">
            <div className="w-12 h-12 bg-camel-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <MessageSquare className="w-6 h-6 text-camel-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">
              Provide Feedback
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Help us improve by rating the accuracy of this analysis
            </p>
            <Link to={`/feedback/${imageId}`} className="btn-outline">
              Give Feedback
            </Link>
          </div>

          <div className="card p-6 text-center">
            <div className="w-12 h-12 bg-camel-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Share2 className="w-6 h-6 text-camel-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">
              Share Results
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Share this analysis with others
            </p>
            <button onClick={handleShare} className="btn-outline">
              Share
            </button>
          </div>

          <div className="card p-6 text-center">
            <div className="w-12 h-12 bg-camel-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <BarChart3 className="w-6 h-6 text-camel-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">
              Analyze Another
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Upload another camel image for analysis
            </p>
            <Link to="/" className="btn-primary">
              New Analysis
            </Link>
          </div>
        </div>

        {/* Analysis Info */}
        <div className="mt-8 card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Analysis Information
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Analysis ID:</span>
              <span className="ml-2 text-gray-600 font-mono">{imageData.id}</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Date:</span>
              <span className="ml-2 text-gray-600">
                {new Date(imageData.created_at).toLocaleDateString()}
              </span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Filename:</span>
              <span className="ml-2 text-gray-600">{imageData.filename}</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Overall Rating:</span>
              <span className="ml-2 text-gray-600">{imageData.rating}/10</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;
