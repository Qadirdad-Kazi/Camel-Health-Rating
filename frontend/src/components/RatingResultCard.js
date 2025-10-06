import React from 'react';
import { Star, TrendingUp, Award, Target } from 'lucide-react';

const RatingResultCard = ({ rating, features, imageUrl }) => {
  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <Star key={i} className="w-6 h-6 rating-star fill-current" />
      );
    }

    if (hasHalfStar) {
      stars.push(
        <div key="half" className="relative">
          <Star className="w-6 h-6 rating-star-empty" />
          <div className="absolute inset-0 overflow-hidden w-1/2">
            <Star className="w-6 h-6 rating-star fill-current" />
          </div>
        </div>
      );
    }

    const emptyStars = 10 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(
        <Star key={`empty-${i}`} className="w-6 h-6 rating-star-empty" />
      );
    }

    return stars;
  };

  const getRatingColor = (rating) => {
    if (rating >= 8) return 'text-green-600';
    if (rating >= 6) return 'text-yellow-600';
    if (rating >= 4) return 'text-orange-600';
    return 'text-red-600';
  };

  const getRatingLabel = (rating) => {
    if (rating >= 9) return 'Exceptional';
    if (rating >= 8) return 'Excellent';
    if (rating >= 7) return 'Very Good';
    if (rating >= 6) return 'Good';
    if (rating >= 5) return 'Average';
    if (rating >= 4) return 'Below Average';
    return 'Poor';
  };

  const getFeatureBadgeClass = (value) => {
    const valueLower = value.toLowerCase();
    if (valueLower.includes('excellent') || valueLower.includes('very_high')) {
      return 'feature-badge excellent';
    }
    if (valueLower.includes('good') || valueLower.includes('high')) {
      return 'feature-badge good';
    }
    if (valueLower.includes('fair') || valueLower.includes('average')) {
      return 'feature-badge fair';
    }
    return 'feature-badge poor';
  };

  const getFeatureIcon = (feature) => {
    switch (feature) {
      case 'body_shape':
        return <Target className="w-4 h-4" />;
      case 'head_structure':
        return <Award className="w-4 h-4" />;
      case 'leg_condition':
        return <TrendingUp className="w-4 h-4" />;
      case 'coat_condition':
        return <Star className="w-4 h-4" />;
      case 'overall_fitness':
        return <TrendingUp className="w-4 h-4" />;
      default:
        return <Star className="w-4 h-4" />;
    }
  };

  const getFeatureLabel = (feature) => {
    const labels = {
      body_shape: 'Body Shape',
      head_structure: 'Head Structure',
      leg_condition: 'Leg Condition',
      coat_condition: 'Coat Condition',
      overall_fitness: 'Overall Fitness'
    };
    return labels[feature] || feature;
  };

  return (
    <div className="card p-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Camel Rating Results
        </h2>
        <p className="text-gray-600">
          AI-powered analysis of your camel image
        </p>
      </div>

      {/* Image Display */}
      {imageUrl && (
        <div className="mb-6">
          <img
            src={imageUrl}
            alt="Analyzed camel"
            className="w-full h-64 object-cover rounded-lg border border-gray-200"
          />
        </div>
      )}

      {/* Overall Rating */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center space-x-2 mb-2">
          <span className={`text-4xl font-bold ${getRatingColor(rating)}`}>
            {rating}/10
          </span>
          <span className="text-lg text-gray-600">
            {getRatingLabel(rating)}
          </span>
        </div>
        
        <div className="flex justify-center space-x-1 mb-4">
          {renderStars(rating)}
        </div>
        
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className={`h-3 rounded-full transition-all duration-1000 ${
              rating >= 8 ? 'bg-green-500' :
              rating >= 6 ? 'bg-yellow-500' :
              rating >= 4 ? 'bg-orange-500' : 'bg-red-500'
            }`}
            style={{ width: `${(rating / 10) * 100}%` }}
          ></div>
        </div>
      </div>

      {/* Feature Breakdown */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Feature Analysis
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(features).map(([feature, value]) => (
            <div
              key={feature}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center space-x-3">
                {getFeatureIcon(feature)}
                <span className="font-medium text-gray-700">
                  {getFeatureLabel(feature)}
                </span>
              </div>
              <span className={`feature-badge ${getFeatureBadgeClass(value)}`}>
                {value.replace('_', ' ')}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Additional Info */}
      <div className="mt-6 p-4 bg-camel-50 rounded-lg">
        <div className="flex items-start space-x-3">
          <div className="w-8 h-8 bg-camel-100 rounded-full flex items-center justify-center flex-shrink-0">
            <Award className="w-4 h-4 text-camel-600" />
          </div>
          <div>
            <h4 className="font-medium text-camel-800 mb-1">
              AI Analysis Complete
            </h4>
            <p className="text-sm text-camel-600">
              This rating is based on advanced machine learning analysis of your camel's 
              physical characteristics. The AI evaluates multiple factors to provide 
              a comprehensive assessment.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RatingResultCard;
