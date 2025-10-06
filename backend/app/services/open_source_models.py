import cv2
import numpy as np
from PIL import Image
import io
import logging
from typing import Dict, Any, List, Tuple
import requests
import json

logger = logging.getLogger(__name__)

class OpenSourceAnimalModels:
    """
    Integration of open-source models for animal health assessment
    """
    
    def __init__(self):
        self.yolo_model = None
        self.huggingface_models = {}
        self.animal_detection_confidence = 0.5
        self.health_assessment_threshold = 0.3
        
    def load_yolo_model(self):
        """Load YOLOv8 model for animal detection"""
        try:
            # Try to import ultralytics
            from ultralytics import YOLO
            
            # Load YOLOv8 model (general object detection)
            self.yolo_model = YOLO('yolov8n.pt')  # Nano version for speed
            logger.info("✅ YOLOv8 model loaded successfully")
            return True
            
        except ImportError:
            logger.warning("❌ ultralytics not installed. Install with: pip install ultralytics")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to load YOLOv8 model: {e}")
            return False
    
    def detect_animals_yolo(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Detect animals using YOLOv8 model
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dictionary with animal detection results
        """
        try:
            if not self.yolo_model:
                if not self.load_yolo_model():
                    return {"animals_detected": False, "error": "YOLO model not available"}
            
            # Convert bytes to image
            image = Image.open(io.BytesIO(image_bytes))
            image_array = np.array(image)
            
            # Run YOLO detection
            results = self.yolo_model(image_array)
            
            # Parse results
            animals_found = []
            animal_classes = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe']
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        
                        # Check if it's an animal class
                        if class_id < len(animal_classes) and confidence > self.animal_detection_confidence:
                            class_name = animal_classes[class_id]
                            if class_name in ['cow', 'horse', 'sheep', 'elephant', 'bear', 'zebra', 'giraffe']:
                                animals_found.append({
                                    "class": class_name,
                                    "confidence": confidence,
                                    "bbox": box.xyxy[0].tolist()
                                })
            
            return {
                "animals_detected": len(animals_found) > 0,
                "animal_count": len(animals_found),
                "animals": animals_found,
                "model": "YOLOv8"
            }
            
        except Exception as e:
            logger.error(f"Error in YOLO animal detection: {e}")
            return {"animals_detected": False, "error": str(e)}
    
    def assess_health_with_yolo(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Assess animal health using YOLO detection and basic heuristics
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dictionary with health assessment results
        """
        try:
            # First detect animals
            detection_result = self.detect_animals_yolo(image_bytes)
            
            if not detection_result.get("animals_detected", False):
                return {
                    "health_assessment": "no_animals_detected",
                    "health_score": 0.0,
                    "recommendation": "No animals detected in image",
                    "confidence": 0.0
                }
            
            # Basic health assessment based on detection
            animals = detection_result.get("animals", [])
            health_issues = []
            
            for animal in animals:
                confidence = animal.get("confidence", 0.0)
                class_name = animal.get("class", "")
                
                # Basic health heuristics
                if confidence < 0.7:
                    health_issues.append(f"Low detection confidence for {class_name}")
                
                # Check bounding box for potential issues
                bbox = animal.get("bbox", [])
                if len(bbox) == 4:
                    x1, y1, x2, y2 = bbox
                    width = x2 - x1
                    height = y2 - y1
                    
                    # Check for unusual proportions (potential injury)
                    aspect_ratio = width / height if height > 0 else 1
                    if aspect_ratio < 0.3 or aspect_ratio > 3.0:
                        health_issues.append(f"Unusual proportions detected for {class_name}")
            
            # Determine health status
            if health_issues:
                health_score = max(0.0, 1.0 - len(health_issues) * 0.2)
                recommendation = "Potential health issues detected"
                severity = "moderate" if len(health_issues) < 3 else "high"
            else:
                health_score = 0.8  # Good health
                recommendation = "Animal appears healthy"
                severity = "none"
            
            return {
                "health_assessment": "completed",
                "health_score": health_score,
                "severity": severity,
                "recommendation": recommendation,
                "health_issues": health_issues,
                "confidence": detection_result.get("animal_count", 0) * 0.2,
                "model": "YOLOv8_Health"
            }
            
        except Exception as e:
            logger.error(f"Error in YOLO health assessment: {e}")
            return {
                "health_assessment": "error",
                "health_score": 0.0,
                "error": str(e)
            }
    
    def load_huggingface_model(self, model_name: str = "microsoft/DialoGPT-medium"):
        """Load Hugging Face model for animal analysis"""
        try:
            from transformers import pipeline
            
            # Load a general image classification model
            self.huggingface_models[model_name] = pipeline(
                "image-classification",
                model="microsoft/resnet-50",
                device=-1  # CPU
            )
            logger.info(f"✅ Hugging Face model {model_name} loaded")
            return True
            
        except ImportError:
            logger.warning("❌ transformers not installed. Install with: pip install transformers")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to load Hugging Face model: {e}")
            return False
    
    def analyze_with_huggingface(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Analyze image using Hugging Face models
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dictionary with analysis results
        """
        try:
            if not self.huggingface_models:
                if not self.load_huggingface_model():
                    return {"analysis": "failed", "error": "Hugging Face model not available"}
            
            # Convert bytes to image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Run analysis with first available model
            model_name = list(self.huggingface_models.keys())[0]
            model = self.huggingface_models[model_name]
            
            results = model(image)
            
            # Parse results
            predictions = []
            for result in results:
                predictions.append({
                    "label": result.get("label", ""),
                    "score": result.get("score", 0.0)
                })
            
            return {
                "analysis": "completed",
                "predictions": predictions,
                "model": model_name,
                "top_prediction": predictions[0] if predictions else None
            }
            
        except Exception as e:
            logger.error(f"Error in Hugging Face analysis: {e}")
            return {"analysis": "failed", "error": str(e)}
    
    def comprehensive_open_source_analysis(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Run comprehensive analysis using multiple open-source models
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dictionary with comprehensive analysis results
        """
        try:
            logger.info("Running comprehensive open-source analysis...")
            
            # Run YOLO analysis
            yolo_result = self.assess_health_with_yolo(image_bytes)
            
            # Run Hugging Face analysis
            hf_result = self.analyze_with_huggingface(image_bytes)
            
            # Combine results
            combined_score = 0.0
            combined_confidence = 0.0
            recommendations = []
            
            # YOLO health assessment
            if yolo_result.get("health_assessment") == "completed":
                combined_score += yolo_result.get("health_score", 0.0) * 0.6
                combined_confidence += yolo_result.get("confidence", 0.0) * 0.6
                if yolo_result.get("recommendation"):
                    recommendations.append(f"YOLO: {yolo_result.get('recommendation')}")
            
            # Hugging Face analysis
            if hf_result.get("analysis") == "completed":
                top_pred = hf_result.get("top_prediction")
                if top_pred:
                    combined_score += top_pred.get("score", 0.0) * 0.4
                    combined_confidence += top_pred.get("score", 0.0) * 0.4
                    recommendations.append(f"HF: {top_pred.get('label', 'Unknown')}")
            
            # Determine overall health status
            if combined_score > 0.7:
                overall_health = "healthy"
                severity = "none"
            elif combined_score > 0.4:
                overall_health = "moderate"
                severity = "minor"
            else:
                overall_health = "poor"
                severity = "moderate"
            
            return {
                "open_source_analysis": "completed",
                "overall_health": overall_health,
                "health_score": combined_score,
                "confidence": combined_confidence,
                "severity": severity,
                "recommendations": recommendations,
                "yolo_results": yolo_result,
                "huggingface_results": hf_result,
                "models_used": ["YOLOv8", "HuggingFace"]
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive open-source analysis: {e}")
            return {
                "open_source_analysis": "failed",
                "error": str(e)
            }
