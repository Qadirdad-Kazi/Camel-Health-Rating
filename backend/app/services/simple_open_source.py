import cv2
import numpy as np
from PIL import Image
import io
import logging
from typing import Dict, Any, List, Tuple
import requests
import json

logger = logging.getLogger(__name__)

class SimpleOpenSourceModels:
    """
    Lightweight open-source models for animal health assessment
    Using basic computer vision techniques without heavy dependencies
    """
    
    def __init__(self):
        self.animal_detection_confidence = 0.3
        self.health_assessment_threshold = 0.4
        
    def detect_animals_opencv(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Detect animals using OpenCV's built-in features
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dictionary with animal detection results
        """
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(image_bytes))
            image_array = np.array(image)
            
            # Convert to OpenCV format
            if len(image_array.shape) == 3:
                opencv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            else:
                opencv_image = image_array
            
            # Basic animal detection using contours and features
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Edge detection
            edges = cv2.Canny(blurred, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours by area and shape
            animal_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Minimum area for animal detection
                    # Check aspect ratio (animals are typically not too elongated)
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h if h > 0 else 0
                    if 0.3 < aspect_ratio < 3.0:  # Reasonable animal proportions
                        animal_contours.append({
                            "contour": contour,
                            "area": area,
                            "bbox": [x, y, w, h],
                            "aspect_ratio": aspect_ratio
                        })
            
            # Sort by area (largest first)
            animal_contours.sort(key=lambda x: x["area"], reverse=True)
            
            return {
                "animals_detected": len(animal_contours) > 0,
                "animal_count": len(animal_contours),
                "animals": animal_contours[:3],  # Top 3 largest
                "model": "OpenCV_Contours"
            }
            
        except Exception as e:
            logger.error(f"Error in OpenCV animal detection: {e}")
            return {"animals_detected": False, "error": str(e)}
    
    def assess_health_simple(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Simple health assessment using basic computer vision
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dictionary with health assessment results
        """
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(image_bytes))
            image_array = np.array(image)
            
            # Convert to OpenCV format
            if len(image_array.shape) == 3:
                opencv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            else:
                opencv_image = image_array
            
            health_issues = []
            health_score = 1.0
            
            # 1. Check for missing limbs using symmetry analysis
            symmetry_score = self._analyze_symmetry(opencv_image)
            if symmetry_score < 0.6:
                health_issues.append("Asymmetry detected - possible missing limb")
                health_score -= 0.3
            
            # 2. Check for injuries using color analysis
            injury_score = self._detect_injuries_simple(opencv_image)
            if injury_score < 0.7:
                health_issues.append("Potential injury or abnormality detected")
                health_score -= 0.2
            
            # 3. Check for mobility issues using posture analysis
            posture_score = self._analyze_posture(opencv_image)
            if posture_score < 0.6:
                health_issues.append("Abnormal posture detected")
                health_score -= 0.2
            
            # 4. Check for overall body condition
            body_condition = self._assess_body_condition(opencv_image)
            if body_condition < 0.5:
                health_issues.append("Poor body condition detected")
                health_score -= 0.3
            
            # Ensure health score is between 0 and 1
            health_score = max(0.0, min(1.0, health_score))
            
            # Determine severity
            if health_score > 0.8:
                severity = "none"
                recommendation = "Animal appears healthy"
            elif health_score > 0.6:
                severity = "minor"
                recommendation = "Minor issues detected, monitor closely"
            elif health_score > 0.3:
                severity = "moderate"
                recommendation = "Moderate health concerns, veterinary attention recommended"
            else:
                severity = "severe"
                recommendation = "Serious health issues detected, immediate veterinary attention required"
            
            return {
                "health_assessment": "completed",
                "health_score": health_score,
                "severity": severity,
                "recommendation": recommendation,
                "health_issues": health_issues,
                "symmetry_score": symmetry_score,
                "injury_score": injury_score,
                "posture_score": posture_score,
                "body_condition": body_condition,
                "confidence": 0.7,  # Moderate confidence for simple analysis
                "model": "Simple_OpenCV"
            }
            
        except Exception as e:
            logger.error(f"Error in simple health assessment: {e}")
            return {
                "health_assessment": "error",
                "health_score": 0.0,
                "error": str(e)
            }
    
    def _analyze_symmetry(self, image: np.ndarray) -> float:
        """Analyze image symmetry to detect missing limbs"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Get image dimensions
            height, width = gray.shape
            
            # Split image into left and right halves
            left_half = gray[:, :width//2]
            right_half = gray[:, width//2:]
            
            # Flip right half to compare with left
            right_half_flipped = cv2.flip(right_half, 1)
            
            # Resize to match dimensions
            min_width = min(left_half.shape[1], right_half_flipped.shape[1])
            left_half = left_half[:, :min_width]
            right_half_flipped = right_half_flipped[:, :min_width]
            
            # Calculate structural similarity
            diff = cv2.absdiff(left_half, right_half_flipped)
            mean_diff = np.mean(diff)
            
            # Convert to similarity score (0-1, higher is more symmetric)
            similarity = 1.0 - (mean_diff / 255.0)
            
            return max(0.0, min(1.0, similarity))
            
        except Exception as e:
            logger.error(f"Error in symmetry analysis: {e}")
            return 0.5  # Default moderate score
    
    def _detect_injuries_simple(self, image: np.ndarray) -> float:
        """Detect potential injuries using color and texture analysis"""
        try:
            # Convert to HSV for better color analysis
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Define color ranges for potential injury indicators
            # Red/brown areas that might indicate wounds
            lower_red1 = np.array([0, 50, 50])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 50, 50])
            upper_red2 = np.array([180, 255, 255])
            
            # Create masks for red areas
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            red_mask = cv2.bitwise_or(mask1, mask2)
            
            # Calculate percentage of red areas
            red_pixels = cv2.countNonZero(red_mask)
            total_pixels = image.shape[0] * image.shape[1]
            red_percentage = red_pixels / total_pixels
            
            # Convert to health score (lower red percentage = healthier)
            health_score = 1.0 - (red_percentage * 10)  # Scale factor for sensitivity
            return max(0.0, min(1.0, health_score))
            
        except Exception as e:
            logger.error(f"Error in injury detection: {e}")
            return 0.7  # Default moderate score
    
    def _analyze_posture(self, image: np.ndarray) -> float:
        """Analyze animal posture for mobility issues"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return 0.5  # No contours found, neutral score
            
            # Find the largest contour (likely the animal)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Analyze contour shape
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            if perimeter == 0:
                return 0.5
            
            # Calculate circularity (healthy animals tend to have more regular shapes)
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            # Analyze aspect ratio
            x, y, w, h = cv2.boundingRect(largest_contour)
            aspect_ratio = w / h if h > 0 else 1
            
            # Combine metrics for posture score
            # Higher circularity and reasonable aspect ratio = better posture
            posture_score = (circularity * 0.6) + (min(1.0, 1.0 / abs(aspect_ratio - 1.0)) * 0.4)
            
            return max(0.0, min(1.0, posture_score))
            
        except Exception as e:
            logger.error(f"Error in posture analysis: {e}")
            return 0.6  # Default moderate score
    
    def _assess_body_condition(self, image: np.ndarray) -> float:
        """Assess overall body condition using image analysis"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calculate image statistics
            mean_brightness = np.mean(gray)
            std_brightness = np.std(gray)
            
            # Analyze texture (healthy animals have more consistent texture)
            # Use Laplacian to measure image sharpness/texture
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            texture_variance = np.var(laplacian)
            
            # Combine metrics
            # Good body condition: moderate brightness, consistent texture
            brightness_score = 1.0 - abs(mean_brightness - 128) / 128  # Optimal around 128
            texture_score = min(1.0, texture_variance / 1000)  # Normalize texture variance
            
            body_condition = (brightness_score * 0.6) + (texture_score * 0.4)
            
            return max(0.0, min(1.0, body_condition))
            
        except Exception as e:
            logger.error(f"Error in body condition assessment: {e}")
            return 0.6  # Default moderate score
    
    def comprehensive_simple_analysis(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Run comprehensive analysis using simple open-source methods
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dictionary with comprehensive analysis results
        """
        try:
            logger.info("Running comprehensive simple open-source analysis...")
            
            # Run animal detection
            detection_result = self.detect_animals_opencv(image_bytes)
            
            # Run health assessment
            health_result = self.assess_health_simple(image_bytes)
            
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
                    overall_health = "detection_failed"
                    overall_score = 0.0
            else:
                overall_health = "no_animals_detected"
                overall_score = 0.0
            
            return {
                "simple_analysis": "completed",
                "overall_health": overall_health,
                "health_score": overall_score,
                "animals_detected": detection_result.get("animals_detected", False),
                "animal_count": detection_result.get("animal_count", 0),
                "health_assessment": health_result,
                "recommendation": health_result.get("recommendation", "Analysis completed"),
                "confidence": 0.6,  # Moderate confidence for simple methods
                "model": "Simple_OpenCV_Comprehensive"
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive simple analysis: {e}")
            return {
                "simple_analysis": "failed",
                "error": str(e)
            }
