import React, { useState } from 'react';
import { ThumbsUp, ThumbsDown, MessageSquare, Send } from 'lucide-react';

const FeedbackForm = ({ imageId, onSubmit, loading = false }) => {
  const [isAccurate, setIsAccurate] = useState(null);
  const [comment, setComment] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (isAccurate === null) {
      return;
    }

    try {
      await onSubmit({
        image_id: imageId,
        is_accurate: isAccurate,
        comment: comment.trim() || null
      });
      setSubmitted(true);
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  if (submitted) {
    return (
      <div className="card p-6 text-center">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <ThumbsUp className="w-8 h-8 text-green-600" />
        </div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          Thank You for Your Feedback!
        </h3>
        <p className="text-gray-600">
          Your feedback helps us improve our AI model and provide better ratings.
        </p>
      </div>
    );
  }

  return (
    <div className="card p-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Rate This Analysis
        </h2>
        <p className="text-gray-600">
          Help us improve by providing feedback on the accuracy of this rating
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Accuracy Rating */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Was this rating accurate?
          </label>
          <div className="flex justify-center space-x-8">
            <button
              type="button"
              onClick={() => setIsAccurate(true)}
              className={`flex flex-col items-center space-y-2 p-4 rounded-lg border-2 transition-all duration-200 ${
                isAccurate === true
                  ? 'border-green-500 bg-green-50 text-green-700'
                  : 'border-gray-300 hover:border-green-400 hover:bg-green-50'
              }`}
            >
              <ThumbsUp className="w-8 h-8" />
              <span className="font-medium">Yes</span>
            </button>
            
            <button
              type="button"
              onClick={() => setIsAccurate(false)}
              className={`flex flex-col items-center space-y-2 p-4 rounded-lg border-2 transition-all duration-200 ${
                isAccurate === false
                  ? 'border-red-500 bg-red-50 text-red-700'
                  : 'border-gray-300 hover:border-red-400 hover:bg-red-50'
              }`}
            >
              <ThumbsDown className="w-8 h-8" />
              <span className="font-medium">No</span>
            </button>
          </div>
        </div>

        {/* Comment */}
        <div>
          <label htmlFor="comment" className="block text-sm font-medium text-gray-700 mb-2">
            Additional Comments (Optional)
          </label>
          <div className="relative">
            <MessageSquare className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
            <textarea
              id="comment"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              rows={4}
              className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-camel-500 focus:border-transparent resize-none"
              placeholder="Share any additional thoughts about the rating or suggestions for improvement..."
              maxLength={500}
            />
          </div>
          <div className="text-right text-xs text-gray-500 mt-1">
            {comment.length}/500 characters
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-center">
          <button
            type="submit"
            disabled={isAccurate === null || loading}
            className={`btn-primary flex items-center space-x-2 ${
              isAccurate === null || loading
                ? 'opacity-50 cursor-not-allowed'
                : ''
            }`}
          >
            {loading ? (
              <>
                <div className="loading-spinner"></div>
                <span>Submitting...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Submit Feedback</span>
              </>
            )}
          </button>
        </div>
      </form>

      {/* Help Text */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-medium text-gray-900 mb-2">Why Your Feedback Matters</h4>
        <p className="text-sm text-gray-600">
          Your feedback helps us continuously improve our AI model. By rating the accuracy 
          of our analysis, you're contributing to better camel evaluations for everyone.
        </p>
      </div>
    </div>
  );
};

export default FeedbackForm;
