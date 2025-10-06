import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { feedbackAPI, predictionAPI } from '../services/api';
import FeedbackForm from '../components/FeedbackForm';
import { ArrowLeft, MessageSquare, ThumbsUp, ThumbsDown } from 'lucide-react';

const Feedback = () => {
  const { imageId } = useParams();
  const navigate = useNavigate();
  const [imageData, setImageData] = useState(null);
  const [feedbackStats, setFeedbackStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [imageResponse, statsResponse] = await Promise.all([
          predictionAPI.getImageDetails(imageId),
          feedbackAPI.getFeedbackStats(imageId)
        ]);
        
        setImageData(imageResponse);
        setFeedbackStats(statsResponse);
      } catch (error) {
        console.error('Error fetching data:', error);
        toast.error('Failed to load data');
        navigate('/');
      } finally {
        setLoading(false);
      }
    };

    if (imageId) {
      fetchData();
    }
  }, [imageId, navigate]);

  const handleSubmitFeedback = async (feedbackData) => {
    setSubmitting(true);
    
    try {
      await feedbackAPI.submitFeedback(feedbackData);
      toast.success('Thank you for your feedback!');
      
      // Refresh feedback stats
      const stats = await feedbackAPI.getFeedbackStats(imageId);
      setFeedbackStats(stats);
    } catch (error) {
      console.error('Error submitting feedback:', error);
      toast.error(error.response?.data?.detail || 'Failed to submit feedback');
      throw error;
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!imageData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Image Not Found
          </h2>
          <p className="text-gray-600 mb-6">
            The requested image could not be found.
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
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Link 
            to={`/results/${imageId}`} 
            className="flex items-center space-x-2 text-gray-600 hover:text-camel-600 transition-colors duration-200"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Results</span>
          </Link>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Image and Rating */}
          <div className="lg:col-span-1">
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Analysis Results
              </h3>
              
              <div className="mb-4">
                <img
                  src={`http://localhost:8000${imageData.image_url}`}
                  alt="Analyzed camel"
                  className="w-full h-48 object-cover rounded-lg border border-gray-200"
                />
              </div>
              
              <div className="text-center">
                <div className="text-3xl font-bold text-camel-600 mb-2">
                  {imageData.rating}/10
                </div>
                <div className="text-sm text-gray-600">
                  Overall Rating
                </div>
              </div>
              
              <div className="mt-4 space-y-2">
                {Object.entries(imageData.features).map(([feature, value]) => (
                  <div key={feature} className="flex justify-between text-sm">
                    <span className="text-gray-600 capitalize">
                      {feature.replace('_', ' ')}:
                    </span>
                    <span className="font-medium text-gray-900 capitalize">
                      {value.replace('_', ' ')}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Feedback Form */}
          <div className="lg:col-span-2">
            <FeedbackForm
              imageId={imageId}
              onSubmit={handleSubmitFeedback}
              loading={submitting}
            />
          </div>
        </div>

        {/* Community Feedback Stats */}
        {feedbackStats && feedbackStats.total_feedback > 0 && (
          <div className="mt-8 card p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Community Feedback
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900 mb-1">
                  {feedbackStats.total_feedback}
                </div>
                <div className="text-sm text-gray-600">Total Reviews</div>
              </div>
              
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600 mb-1">
                  {feedbackStats.accuracy_rate}%
                </div>
                <div className="text-sm text-gray-600">Accuracy Rate</div>
              </div>
              
              <div className="text-center">
                <div className="flex justify-center space-x-4">
                  <div className="flex items-center space-x-1">
                    <ThumbsUp className="w-4 h-4 text-green-600" />
                    <span className="text-sm font-medium text-gray-900">
                      {feedbackStats.accurate_feedback}
                    </span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <ThumbsDown className="w-4 h-4 text-red-600" />
                    <span className="text-sm font-medium text-gray-900">
                      {feedbackStats.inaccurate_feedback}
                    </span>
                  </div>
                </div>
                <div className="text-sm text-gray-600 mt-1">Accurate vs Inaccurate</div>
              </div>
            </div>
          </div>
        )}

        {/* Help Section */}
        <div className="mt-8 card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Why Your Feedback Matters
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Improve AI Accuracy</h4>
              <p className="text-sm text-gray-600">
                Your feedback helps us train our AI model to provide more accurate 
                ratings and better feature analysis.
              </p>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Help the Community</h4>
              <p className="text-sm text-gray-600">
                By providing feedback, you're helping other users get better 
                camel analysis results in the future.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Feedback;
