import React from 'react';
import { Target, Award, TrendingUp, Star, Activity } from 'lucide-react';

const FeatureBreakdownCard = ({ features }) => {
  const getFeatureIcon = (feature) => {
    const icons = {
      body_shape: <Target className="w-5 h-5" />,
      head_structure: <Award className="w-5 h-5" />,
      leg_condition: <TrendingUp className="w-5 h-5" />,
      coat_condition: <Star className="w-5 h-5" />,
      overall_fitness: <Activity className="w-5 h-5" />
    };
    return icons[feature] || <Star className="w-5 h-5" />;
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

  const getFeatureDescription = (feature, value) => {
    const descriptions = {
      body_shape: {
        excellent: 'Perfect proportions with strong, well-developed musculature',
        good: 'Well-proportioned body with good muscle development',
        fair: 'Adequate body structure with room for improvement',
        poor: 'Body structure needs significant improvement'
      },
      head_structure: {
        excellent: 'Well-formed head with proper proportions and alert expression',
        good: 'Good head structure with clear features',
        fair: 'Average head structure with minor imperfections',
        poor: 'Head structure shows significant issues'
      },
      leg_condition: {
        excellent: 'Strong, straight legs with excellent bone structure',
        good: 'Good leg structure with minor imperfections',
        fair: 'Adequate leg condition with some concerns',
        poor: 'Leg condition requires attention'
      },
      coat_condition: {
        excellent: 'Lustrous, healthy coat with excellent texture',
        good: 'Good coat condition with healthy appearance',
        fair: 'Average coat condition with minor issues',
        poor: 'Coat condition needs improvement'
      },
      overall_fitness: {
        very_high: 'Exceptional physical condition and fitness level',
        high: 'High level of fitness and physical condition',
        average: 'Good overall fitness with room for improvement',
        low: 'Fitness level needs significant improvement'
      }
    };
    
    return descriptions[feature]?.[value] || 'No description available';
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

  const getFeatureScore = (value) => {
    const valueLower = value.toLowerCase();
    if (valueLower.includes('excellent') || valueLower.includes('very_high')) {
      return 4;
    }
    if (valueLower.includes('good') || valueLower.includes('high')) {
      return 3;
    }
    if (valueLower.includes('fair') || valueLower.includes('average')) {
      return 2;
    }
    return 1;
  };

  return (
    <div className="card p-6">
      <div className="mb-6">
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          Detailed Feature Analysis
        </h3>
        <p className="text-gray-600">
          Comprehensive breakdown of each evaluated characteristic
        </p>
      </div>

      <div className="space-y-6">
        {Object.entries(features).map(([feature, value]) => {
          const score = getFeatureScore(value);
          const maxScore = 4;
          
          return (
            <div key={feature} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-camel-100 rounded-lg flex items-center justify-center text-camel-600">
                    {getFeatureIcon(feature)}
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">
                      {getFeatureLabel(feature)}
                    </h4>
                    <span className={`feature-badge ${getFeatureBadgeClass(value)}`}>
                      {value.replace('_', ' ')}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-500">Score</div>
                  <div className="text-lg font-bold text-camel-600">
                    {score}/{maxScore}
                  </div>
                </div>
              </div>
              
              <p className="text-sm text-gray-600 mb-3">
                {getFeatureDescription(feature, value)}
              </p>
              
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all duration-1000 ${
                    score >= 4 ? 'bg-green-500' :
                    score >= 3 ? 'bg-blue-500' :
                    score >= 2 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${(score / maxScore) * 100}%` }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-medium text-gray-900 mb-2">How We Evaluate</h4>
        <p className="text-sm text-gray-600">
          Our AI model analyzes multiple visual characteristics of camels including 
          body proportions, structural integrity, coat quality, and overall physical 
          condition. Each feature is scored on a scale from 1-4, contributing to 
          the overall rating.
        </p>
      </div>
    </div>
  );
};

export default FeatureBreakdownCard;
