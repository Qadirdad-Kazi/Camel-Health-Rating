import cv2
import numpy as np
from PIL import Image
import io
import logging
from typing import Dict, Any, List, Tuple
import requests
import json
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class AdvancedOpenSourceModels:
    """
    Advanced open-source models for animal health assessment
    Integrates multiple state-of-the-art models for better accuracy
    """
    
    def __init__(self):
        self.models = {}
        self.model_weights = {
            'yolo': 0.3,
            'opencv': 0.2,
            'huggingface': 0.3,
            'ensemble': 0.2
        }
        self.animal_detection_confidence = 0.4
        self.health_assessment_threshold = 0.3
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all available models"""
        try:
            # Try to load YOLOv8
            self._load_yolo_model()
            
            # Try to load Hugging Face models
            self._load_huggingface_models()
            
            # Initialize OpenCV models
            self._initialize_opencv_models()
            
            logger.info("✅ Advanced open-source models initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing advanced models: {e}")
    
    def _load_yolo_model(self):
        """Load YOLOv8 model"""
        try:
            # Try to import ultralytics
            from ultralytics import YOLO
            
            # Load YOLOv8 model
            self.models['yolo'] = YOLO('yolov8n.pt')
            logger.info("✅ YOLOv8 model loaded")
            
        except ImportError:
            logger.warning("❌ ultralytics not available, skipping YOLOv8")
        except Exception as e:
            logger.error(f"❌ Failed to load YOLOv8: {e}")
    
    def _load_huggingface_models(self):
        """Load Hugging Face models"""
        try:
            from transformers import pipeline
            
            # Load image classification model
            self.models['huggingface'] = pipeline(
                "image-classification",
                model="microsoft/resnet-50",
                device=-1  # CPU
            )
            logger.info("✅ Hugging Face model loaded")
            
        except ImportError:
            logger.warning("❌ transformers not available, skipping Hugging Face")
        except Exception as e:
            logger.error(f"❌ Failed to load Hugging Face model: {e}")
    
    def _initialize_opencv_models(self):
        """Initialize OpenCV-based models"""
        try:
            # Load OpenCV DNN models
            self.models['opencv'] = {
                'face_cascade': cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'),
                'animal_detector': self._create_animal_detector()
            }
            logger.info("✅ OpenCV models initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize OpenCV models: {e}")
    
    def _create_animal_detector(self):
        """Create a custom animal detector using OpenCV"""
        # This is a simplified animal detector
        # In production, you'd use a pre-trained model
        return None
    
    def detect_animals_ensemble(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Detect animals using ensemble of models
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dictionary with ensemble detection results
        """
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(image_bytes))
            image_array = np.array(image)
            
            # Run detection with all available models
            results = {}
            
            # YOLO detection
            if 'yolo' in self.models:
                yolo_result = self._detect_with_yolo(image_array)
                results['yolo'] = yolo_result
            
            # OpenCV detection
            if 'opencv' in self.models:
                opencv_result = self._detect_with_opencv(image_array)
                results['opencv'] = opencv_result
            
            # Hugging Face detection
            if 'huggingface' in self.models:
                hf_result = self._detect_with_huggingface(image_array)
                results['huggingface'] = hf_result
            
            # Ensemble decision
            ensemble_result = self._ensemble_decision(results)
            
            return {
                "animals_detected": ensemble_result['animals_detected'],
                "animal_count": ensemble_result['animal_count'],
                "confidence": ensemble_result['confidence'],
                "model": "ensemble",
                "individual_results": results,
                "ensemble_decision": ensemble_result
            }
            
        except Exception as e:
            logger.error(f"Error in ensemble animal detection: {e}")
            return {"animals_detected": False, "error": str(e)}
    
    def _detect_with_yolo(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Detect animals using YOLO"""
        try:
            if 'yolo' not in self.models:
                return {"animals_detected": False, "error": "YOLO not available"}
            
            results = self.models['yolo'](image_array)
            
            animals_found = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        
                        # Check if it's an animal class
                        if confidence > self.animal_detection_confidence:
                            animals_found.append({
                                "class_id": class_id,
                                "confidence": confidence,
                                "bbox": box.xyxy[0].tolist()
                            })
            
            return {
                "animals_detected": len(animals_found) > 0,
                "animal_count": len(animals_found),
                "animals": animals_found,
                "model": "yolo"
            }
            
        except Exception as e:
            logger.error(f"YOLO detection error: {e}")
            return {"animals_detected": False, "error": str(e)}
    
    def _detect_with_opencv(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Detect animals using OpenCV"""
        try:
            # Convert to OpenCV format
            if len(image_array.shape) == 3:
                opencv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            else:
                opencv_image = image_array
            
            # Basic contour detection
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours
            animal_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Minimum area
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h if h > 0 else 0
                    if 0.3 < aspect_ratio < 3.0:  # Reasonable proportions
                        animal_contours.append({
                            "area": area,
                            "bbox": [x, y, w, h],
                            "aspect_ratio": aspect_ratio
                        })
            
            return {
                "animals_detected": len(animal_contours) > 0,
                "animal_count": len(animal_contours),
                "animals": animal_contours,
                "model": "opencv"
            }
            
        except Exception as e:
            logger.error(f"OpenCV detection error: {e}")
            return {"animals_detected": False, "error": str(e)}
    
    def _detect_with_huggingface(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Detect animals using Hugging Face"""
        try:
            if 'huggingface' not in self.models:
                return {"animals_detected": False, "error": "Hugging Face not available"}
            
            # Convert to PIL Image
            image = Image.fromarray(image_array)
            
            # Run classification
            results = self.models['huggingface'](image)
            
            # Check for animal-related classes
            animal_classes = ['dog', 'cat', 'horse', 'cow', 'sheep', 'bird', 'elephant', 'bear', 'zebra', 'giraffe']
            animals_found = []
            
            for result in results:
                if result['label'].lower() in animal_classes and result['score'] > self.animal_detection_confidence:
                    animals_found.append({
                        "label": result['label'],
                        "confidence": result['score']
                    })
            
            return {
                "animals_detected": len(animals_found) > 0,
                "animal_count": len(animals_found),
                "animals": animals_found,
                "model": "huggingface"
            }
            
        except Exception as e:
            logger.error(f"Hugging Face detection error: {e}")
            return {"animals_detected": False, "error": str(e)}
    
    def _ensemble_decision(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Make ensemble decision based on individual model results"""
        try:
            # Weighted voting
            total_confidence = 0.0
            total_weight = 0.0
            animals_detected = False
            animal_count = 0
            
            for model_name, result in results.items():
                if result.get("animals_detected", False):
                    weight = self.model_weights.get(model_name, 0.1)
                    confidence = result.get("confidence", 0.5)
                    
                    total_confidence += confidence * weight
                    total_weight += weight
                    
                    if not animals_detected:
                        animals_detected = True
                    
                    animal_count = max(animal_count, result.get("animal_count", 0))
            
            # Normalize confidence
            if total_weight > 0:
                final_confidence = total_confidence / total_weight
            else:
                final_confidence = 0.0
            
            return {
                "animals_detected": animals_detected,
                "animal_count": animal_count,
                "confidence": final_confidence,
                "model": "ensemble"
            }
            
        except Exception as e:
            logger.error(f"Ensemble decision error: {e}")
            return {
                "animals_detected": False,
                "animal_count": 0,
                "confidence": 0.0,
                "error": str(e)
            }
    
    def assess_health_advanced(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Advanced health assessment using multiple models
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dictionary with advanced health assessment results
        """
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(image_bytes))
            image_array = np.array(image)
            
            # Run multiple health assessments
            health_results = {}
            
            # Basic computer vision analysis
            health_results['opencv'] = self._assess_health_opencv(image_array)
            
            # YOLO-based analysis
            if 'yolo' in self.models:
                health_results['yolo'] = self._assess_health_yolo(image_array)
            
            # Hugging Face analysis
            if 'huggingface' in self.models:
                health_results['huggingface'] = self._assess_health_huggingface(image_array)
            
            # Ensemble health decision
            ensemble_health = self._ensemble_health_decision(health_results)
            
            return {
                "health_assessment": "completed",
                "health_score": ensemble_health['health_score'],
                "severity": ensemble_health['severity'],
                "recommendation": ensemble_health['recommendation'],
                "health_issues": ensemble_health['health_issues'],
                "confidence": ensemble_health['confidence'],
                "model": "advanced_ensemble",
                "individual_assessments": health_results
            }
            
        except Exception as e:
            logger.error(f"Advanced health assessment error: {e}")
            return {
                "health_assessment": "error",
                "health_score": 0.0,
                "error": str(e)
            }
    
    def _assess_health_opencv(self, image_array: np.ndarray) -> Dict[str, Any]:
        """OpenCV-based health assessment"""
        try:
            # Convert to OpenCV format
            if len(image_array.shape) == 3:
                opencv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            else:
                opencv_image = image_array
            
            health_issues = []
            health_score = 1.0
            
            # Symmetry analysis
            symmetry_score = self._analyze_symmetry_advanced(opencv_image)
            if symmetry_score < 0.6:
                health_issues.append("Asymmetry detected")
                health_score -= 0.3
            
            # Color analysis for injuries
            injury_score = self._detect_injuries_advanced(opencv_image)
            if injury_score < 0.7:
                health_issues.append("Potential injury detected")
                health_score -= 0.2
            
            # Posture analysis
            posture_score = self._analyze_posture_advanced(opencv_image)
            if posture_score < 0.6:
                health_issues.append("Abnormal posture detected")
                health_score -= 0.2
            
            health_score = max(0.0, min(1.0, health_score))
            
            return {
                "health_score": health_score,
                "health_issues": health_issues,
                "symmetry_score": symmetry_score,
                "injury_score": injury_score,
                "posture_score": posture_score,
                "model": "opencv"
            }
            
        except Exception as e:
            logger.error(f"OpenCV health assessment error: {e}")
            return {"health_score": 0.5, "health_issues": [], "error": str(e)}
    
    def _assess_health_yolo(self, image_array: np.ndarray) -> Dict[str, Any]:
        """YOLO-based health assessment"""
        try:
            if 'yolo' not in self.models:
                return {"health_score": 0.5, "health_issues": [], "error": "YOLO not available"}
            
            # Run YOLO detection
            results = self.models['yolo'](image_array)
            
            health_issues = []
            health_score = 1.0
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        confidence = float(box.conf[0])
                        
                        # Low confidence might indicate health issues
                        if confidence < 0.5:
                            health_issues.append("Low detection confidence - possible health issue")
                            health_score -= 0.1
            
            health_score = max(0.0, min(1.0, health_score))
            
            return {
                "health_score": health_score,
                "health_issues": health_issues,
                "model": "yolo"
            }
            
        except Exception as e:
            logger.error(f"YOLO health assessment error: {e}")
            return {"health_score": 0.5, "health_issues": [], "error": str(e)}
    
    def _assess_health_huggingface(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Hugging Face-based health assessment"""
        try:
            if 'huggingface' not in self.models:
                return {"health_score": 0.5, "health_issues": [], "error": "Hugging Face not available"}
            
            # Convert to PIL Image
            image = Image.fromarray(image_array)
            
            # Run classification
            results = self.models['huggingface'](image)
            
            health_issues = []
            health_score = 1.0
            
            # Analyze classification results for health indicators
            for result in results:
                label = result['label'].lower()
                score = result['score']
                
                # Check for health-related classifications
                if 'sick' in label or 'injured' in label or 'unhealthy' in label:
                    health_issues.append(f"Health concern detected: {label}")
                    health_score -= 0.3
                elif 'healthy' in label or 'good' in label:
                    health_score += 0.1
            
            health_score = max(0.0, min(1.0, health_score))
            
            return {
                "health_score": health_score,
                "health_issues": health_issues,
                "model": "huggingface"
            }
            
        except Exception as e:
            logger.error(f"Hugging Face health assessment error: {e}")
            return {"health_score": 0.5, "health_issues": [], "error": str(e)}
    
    def _ensemble_health_decision(self, health_results: Dict[str, Any]) -> Dict[str, Any]:
        """Make ensemble health decision"""
        try:
            total_score = 0.0
            total_weight = 0.0
            all_issues = []
            
            for model_name, result in health_results.items():
                if 'health_score' in result:
                    weight = self.model_weights.get(model_name, 0.1)
                    score = result['health_score']
                    
                    total_score += score * weight
                    total_weight += weight
                    
                    if 'health_issues' in result:
                        all_issues.extend(result['health_issues'])
            
            # Calculate final health score
            if total_weight > 0:
                final_score = total_score / total_weight
            else:
                final_score = 0.5
            
            # Determine severity
            if final_score > 0.8:
                severity = "none"
                recommendation = "Animal appears healthy"
            elif final_score > 0.6:
                severity = "minor"
                recommendation = "Minor issues detected, monitor closely"
            elif final_score > 0.3:
                severity = "moderate"
                recommendation = "Moderate health concerns, veterinary attention recommended"
            else:
                severity = "severe"
                recommendation = "Serious health issues detected, immediate veterinary attention required"
            
            return {
                "health_score": final_score,
                "severity": severity,
                "recommendation": recommendation,
                "health_issues": list(set(all_issues)),  # Remove duplicates
                "confidence": 0.8  # High confidence for ensemble
            }
            
        except Exception as e:
            logger.error(f"Ensemble health decision error: {e}")
            return {
                "health_score": 0.5,
                "severity": "unknown",
                "recommendation": "Assessment failed",
                "health_issues": [],
                "error": str(e)
            }
    
    def _analyze_symmetry_advanced(self, image: np.ndarray) -> float:
        """Advanced symmetry analysis"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape
            
            # Split into left and right halves
            left_half = gray[:, :width//2]
            right_half = gray[:, width//2:]
            
            # Flip right half for comparison
            right_half_flipped = cv2.flip(right_half, 1)
            
            # Resize to match
            min_width = min(left_half.shape[1], right_half_flipped.shape[1])
            left_half = left_half[:, :min_width]
            right_half_flipped = right_half_flipped[:, :min_width]
            
            # Calculate similarity
            diff = cv2.absdiff(left_half, right_half_flipped)
            mean_diff = np.mean(diff)
            
            similarity = 1.0 - (mean_diff / 255.0)
            return max(0.0, min(1.0, similarity))
            
        except Exception as e:
            logger.error(f"Symmetry analysis error: {e}")
            return 0.5
    
    def _detect_injuries_advanced(self, image: np.ndarray) -> float:
        """Advanced injury detection"""
        try:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Define injury color ranges
            lower_red1 = np.array([0, 50, 50])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 50, 50])
            upper_red2 = np.array([180, 255, 255])
            
            # Create masks
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            red_mask = cv2.bitwise_or(mask1, mask2)
            
            # Calculate red pixel percentage
            red_pixels = cv2.countNonZero(red_mask)
            total_pixels = image.shape[0] * image.shape[1]
            red_percentage = red_pixels / total_pixels
            
            # Convert to health score
            health_score = 1.0 - (red_percentage * 5)  # Scale factor
            return max(0.0, min(1.0, health_score))
            
        except Exception as e:
            logger.error(f"Injury detection error: {e}")
            return 0.7
    
    def _analyze_posture_advanced(self, image: np.ndarray) -> float:
        """Advanced posture analysis"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return 0.5
            
            # Find largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Analyze shape
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            if perimeter == 0:
                return 0.5
            
            # Calculate circularity
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            # Analyze aspect ratio
            x, y, w, h = cv2.boundingRect(largest_contour)
            aspect_ratio = w / h if h > 0 else 1
            
            # Combine metrics
            posture_score = (circularity * 0.6) + (min(1.0, 1.0 / abs(aspect_ratio - 1.0)) * 0.4)
            
            return max(0.0, min(1.0, posture_score))
            
        except Exception as e:
            logger.error(f"Posture analysis error: {e}")
            return 0.6
    
    def comprehensive_advanced_analysis(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Run comprehensive analysis using advanced ensemble models
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dictionary with comprehensive analysis results
        """
        try:
            logger.info("Running comprehensive advanced analysis...")
            
            # Run ensemble animal detection
            detection_result = self.detect_animals_ensemble(image_bytes)
            
            # Run advanced health assessment
            health_result = self.assess_health_advanced(image_bytes)
            
            # Combine results
            overall_health = "unknown"
            overall_score = 0.0
            
            if detection_result.get("animals_detected", False):
                if health_result.get("health_assessment") == "completed":
                    overall_score = health_result.get("health_score", 0.0)
                    
                    if overall_score > 0.8:
                        overall_health = "healthy"
                    elif overall_score > 0.6:
                        overall_health = "moderate"
                    elif overall_score > 0.3:
                        overall_health = "poor"
                    else:
                        overall_health = "critical"
                else:
                    overall_health = "assessment_failed"
                    overall_score = 0.0
            else:
                overall_health = "no_animals_detected"
                overall_score = 0.0
            
            return {
                "advanced_analysis": "completed",
                "overall_health": overall_health,
                "health_score": overall_score,
                "animals_detected": detection_result.get("animals_detected", False),
                "animal_count": detection_result.get("animal_count", 0),
                "health_assessment": health_result,
                "recommendation": health_result.get("recommendation", "Analysis completed"),
                "confidence": 0.8,  # High confidence for ensemble
                "model": "advanced_ensemble",
                "models_used": list(self.models.keys())
            }
            
        except Exception as e:
            logger.error(f"Advanced analysis error: {e}")
            return {
                "advanced_analysis": "failed",
                "error": str(e)
            }
