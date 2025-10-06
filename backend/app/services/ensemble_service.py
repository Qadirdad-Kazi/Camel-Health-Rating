import logging
from typing import Dict, Any, List
import numpy as np

logger = logging.getLogger(__name__)

class EnsembleModelService:
    """
    Ensemble service that combines all available models for better accuracy
    """
    
    def __init__(self, ml_service):
        self.ml_service = ml_service
        self.model_weights = {
            'trained_tensorflow': 0.5,  # Increased weight for trained model
            'pretrained': 0.1,
            'simple_open_source': 0.2,
            'advanced_open_source': 0.2
        }
        self.health_weight = 0.4  # Weight for health screening results
    
    def ensemble_predict(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Run ensemble prediction using all available models
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dictionary with ensemble prediction results
        """
        try:
            logger.info("Running ensemble prediction with all available models...")
            
            # Collect predictions from all available models
            predictions = {}
            
            # 1. Trained TensorFlow model
            if self.ml_service.model is not None:
                try:
                    tf_result = self.ml_service._predict_with_trained_model(image_bytes)
                    predictions['trained_tensorflow'] = {
                        'rating': tf_result.get('rating', 0.0),
                        'confidence': tf_result.get('confidence', 0.0),
                        'model': 'trained_tensorflow',
                        'features': tf_result.get('features', {})
                    }
                    logger.info(f"✅ Trained TensorFlow model: {tf_result.get('rating', 0.0):.1f}/10")
                except Exception as e:
                    logger.warning(f"❌ Trained TensorFlow model failed: {e}")
            
            # 2. Pre-trained models
            if self.ml_service.pretrained_service and self.ml_service.pretrained_service.model_type:
                try:
                    pretrained_result = self.ml_service.pretrained_service.predict(image_bytes)
                    predictions['pretrained'] = {
                        'rating': pretrained_result.get('rating', 0.0),
                        'confidence': pretrained_result.get('confidence', 0.0),
                        'model': 'pretrained',
                        'features': pretrained_result.get('features', {})
                    }
                    logger.info(f"✅ Pre-trained model: {pretrained_result.get('rating', 0.0):.1f}/10")
                except Exception as e:
                    logger.warning(f"❌ Pre-trained model failed: {e}")
            
            # 3. Simple open-source models
            try:
                simple_result = self.ml_service._predict_with_simple_models(image_bytes)
                predictions['simple_open_source'] = {
                    'rating': simple_result.get('rating', 0.0),
                    'confidence': simple_result.get('confidence', 0.0),
                    'model': 'simple_open_source',
                    'features': simple_result.get('features', {}),
                    'health_screening': simple_result.get('health_screening', {})
                }
                logger.info(f"✅ Simple open-source model: {simple_result.get('rating', 0.0):.1f}/10")
            except Exception as e:
                logger.warning(f"❌ Simple open-source model failed: {e}")
            
            # 4. Advanced open-source models (if available)
            if hasattr(self.ml_service, 'advanced_models') and self.ml_service.advanced_models:
                try:
                    advanced_result = self.ml_service._predict_with_advanced_models(image_bytes)
                    predictions['advanced_open_source'] = {
                        'rating': advanced_result.get('rating', 0.0),
                        'confidence': advanced_result.get('confidence', 0.0),
                        'model': 'advanced_open_source',
                        'features': advanced_result.get('features', {}),
                        'health_screening': advanced_result.get('health_screening', {})
                    }
                    logger.info(f"✅ Advanced open-source model: {advanced_result.get('rating', 0.0):.1f}/10")
                except Exception as e:
                    logger.warning(f"❌ Advanced open-source model failed: {e}")
            
            # 5. Health screening
            health_result = None
            try:
                health_result = self.ml_service.health_screening.comprehensive_health_screening(image_bytes)
                logger.info(f"✅ Health screening: {health_result.get('health_screening_passed', True)}")
            except Exception as e:
                logger.warning(f"❌ Health screening failed: {e}")
            
            # Combine predictions using weighted ensemble
            ensemble_result = self._combine_predictions(predictions, health_result)
            
            return ensemble_result
            
        except Exception as e:
            logger.error(f"Ensemble prediction failed: {e}")
            # Fallback to simple open-source models
            return self.ml_service._predict_with_simple_models(image_bytes)
    
    def _combine_predictions(self, predictions: Dict[str, Any], health_result: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Combine predictions from all models using weighted ensemble
        
        Args:
            predictions: Dictionary of model predictions
            health_result: Health screening results
            
        Returns:
            Dictionary with ensemble results
        """
        try:
            if not predictions:
                raise ValueError("No predictions available for ensemble")
            
            # Calculate weighted average rating
            total_weight = 0.0
            weighted_rating = 0.0
            total_confidence = 0.0
            
            # Combine ratings
            for model_name, prediction in predictions.items():
                weight = self.model_weights.get(model_name, 0.1)
                rating = prediction.get('rating', 0.0)
                confidence = prediction.get('confidence', 0.0)
                
                weighted_rating += rating * weight
                total_weight += weight
                total_confidence += confidence * weight
            
            # Apply health screening penalty if health issues detected
            health_penalty = 0.0
            health_issues = []
            health_recommendation = "Analysis completed"
            
            # Only apply penalty for serious health issues (be more conservative)
            if health_result and not health_result.get('health_screening_passed', True):
                recommendation = health_result.get('recommendation', '')
                # Only apply penalty for very serious issues, not general health checks
                if 'severe' in recommendation.lower() or 'critical' in recommendation.lower():
                    health_penalty = 3.0  # Reduce rating by 3 points for serious health issues
                    health_issues.append(recommendation)
                    health_recommendation = recommendation
            
            # Check for health issues in open-source models (be more selective)
            for model_name, prediction in predictions.items():
                if 'health_screening' in prediction:
                    health_screening = prediction['health_screening']
                    if health_screening.get('issues_detected', False):
                        recommendation = health_screening.get('recommendation', '')
                        # Only apply penalty for serious issues, not minor monitoring
                        if 'severe' in recommendation.lower() or 'critical' in recommendation.lower() or 'immediate' in recommendation.lower():
                            health_penalty = max(health_penalty, 3.0)  # Apply penalty for serious issues
                            health_issues.append(recommendation)
                            health_recommendation = recommendation
            
            # Special case: If TensorFlow gives high rating but open-source models detect issues, apply penalty
            tf_rating = predictions.get('trained_tensorflow', {}).get('rating', 0.0)
            open_source_issues = False
            for model_name, prediction in predictions.items():
                if model_name != 'trained_tensorflow' and 'health_screening' in prediction:
                    if prediction['health_screening'].get('issues_detected', False):
                        open_source_issues = True
                        break
            
            if tf_rating > 5.0 and open_source_issues and health_penalty == 0.0:
                health_penalty = 2.0  # Apply moderate penalty for this case
                health_recommendation = "Health issues detected by computer vision analysis"
            
            # Apply health penalty
            final_rating = max(0.0, weighted_rating - health_penalty)
            
            # Normalize confidence
            final_confidence = total_confidence / total_weight if total_weight > 0 else 0.0
            
            # Determine which model to report as primary
            primary_model = max(predictions.keys(), key=lambda k: predictions[k].get('confidence', 0.0))
            
            # Combine features from all models
            combined_features = self._combine_features(predictions)
            
            # Generate ensemble message
            if health_penalty > 0:
                message = f"🏥 Ensemble analysis: Health issues detected (Rating reduced by {health_penalty:.1f} points)"
            else:
                message = f"🤖 Ensemble analysis: {final_rating:.1f}/10 from {len(predictions)} models"
            
            return {
                "rating": final_rating,
                "features": combined_features,
                "confidence": final_confidence,
                "model": f"ensemble_{primary_model}",
                "model_info": {
                    "type": "Ensemble Analysis",
                    "methods": [f"{name}_{pred.get('model', 'unknown')}" for name, pred in predictions.items()],
                    "confidence": "High",
                    "models_used": list(predictions.keys()),
                    "health_screening": "Applied" if health_penalty > 0 else "Passed"
                },
                "health_screening": {
                    "overall_health": "poor" if health_penalty > 0 else "good",
                    "health_score": 1.0 - (health_penalty / 10.0),
                    "recommendation": health_recommendation,
                    "issues_detected": len(health_issues) > 0,
                    "health_issues": health_issues
                },
                "message": message,
                "ensemble_details": {
                    "individual_predictions": predictions,
                    "health_result": health_result,
                    "health_penalty": health_penalty,
                    "final_rating": final_rating
                }
            }
            
        except Exception as e:
            logger.error(f"Error combining predictions: {e}")
            # Return the best individual prediction
            best_prediction = max(predictions.values(), key=lambda p: p.get('confidence', 0.0))
            return best_prediction
    
    def _combine_features(self, predictions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combine features from all models
        
        Args:
            predictions: Dictionary of model predictions
            
        Returns:
            Dictionary with combined features
        """
        try:
            combined_features = {}
            
            # Collect all unique feature keys
            all_features = set()
            for prediction in predictions.values():
                features = prediction.get('features', {})
                all_features.update(features.keys())
            
            # Combine features with voting
            for feature_key in all_features:
                feature_values = []
                for prediction in predictions.values():
                    features = prediction.get('features', {})
                    if feature_key in features:
                        feature_values.append(features[feature_key])
                
                if feature_values:
                    # Use the most common value or the first one
                    combined_features[feature_key] = feature_values[0]
            
            # Add ensemble indicator
            combined_features["Analysis Method"] = f"Ensemble of {len(predictions)} models"
            
            return combined_features
            
        except Exception as e:
            logger.error(f"Error combining features: {e}")
            return {"Analysis Method": "Ensemble analysis"}
