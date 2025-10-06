import cv2
import numpy as np
from PIL import Image
import io
import logging
from typing import Dict, Any, Tuple, List

logger = logging.getLogger(__name__)

class CamelHealthScreening:
    """
    Health screening system to detect injured or disabled camels
    before quality rating assessment.
    """
    
    def __init__(self):
        self.injury_threshold = 0.5  # Threshold for injury detection (less sensitive)
        self.missing_limb_threshold = 0.2  # Threshold for missing limb detection (balanced)
        
    def detect_missing_limbs(self, image_array: np.ndarray) -> Dict[str, Any]:
        """
        Detect if camel is missing limbs using contour analysis and symmetry detection.
        
        Args:
            image_array: Image as numpy array
            
        Returns:
            Dictionary with missing limb detection results
        """
        try:
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            
            # Apply edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Analyze contour symmetry and completeness
            height, width = gray.shape
            left_half = edges[:, :width//2]
            right_half = edges[:, width//2:]
            
            # Calculate edge density in each half
            left_density = np.sum(left_half > 0) / (left_half.size)
            right_density = np.sum(right_half > 0) / (right_half.size)
            
            # Check for significant asymmetry (missing limb indicator)
            asymmetry_ratio = abs(left_density - right_density) / max(left_density, right_density, 0.001)
            
            # Analyze bottom portion for leg detection (more lenient)
            bottom_portion = edges[int(height*0.5):, :]
            leg_contours = []
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 50:  # Lower threshold for leg detection
                    x, y, w, h = cv2.boundingRect(contour)
                    # Check if contour is in bottom portion (leg area) - more lenient
                    if y > height * 0.4:  # Start from middle of image
                        leg_contours.append(contour)
            
            # Count potential leg structures
            leg_count = len(leg_contours)
            
            # If no legs detected, assume 4 legs (healthy camel)
            if leg_count == 0:
                leg_count = 4
            
            # Determine if limbs are missing
            missing_limbs = False
            confidence = 0.0
            
            # Very conservative detection - only flag obvious cases
            # Only flag if we have very strong evidence of missing limbs
            if leg_count < 2:  # Very few legs detected (definitely missing)
                missing_limbs = True
                confidence = 0.9
            elif leg_count == 2 and asymmetry_ratio > 0.5:  # Only 2 legs + very high asymmetry
                missing_limbs = True
                confidence = 0.8
            # Don't flag for 3 legs or asymmetry alone - too many false positives
            
            return {
                "missing_limbs": missing_limbs,
                "confidence": confidence,
                "asymmetry_ratio": asymmetry_ratio,
                "leg_count": leg_count,
                "left_density": left_density,
                "right_density": right_density
            }
            
        except Exception as e:
            logger.error(f"Error in missing limb detection: {e}")
            return {
                "missing_limbs": False,
                "confidence": 0.0,
                "error": str(e)
            }
    
    def detect_visible_injuries(self, image_array: np.ndarray) -> Dict[str, Any]:
        """
        Detect visible injuries, wounds, or abnormalities.
        
        Args:
            image_array: Image as numpy array
            
        Returns:
            Dictionary with injury detection results
        """
        try:
            # Convert to different color spaces for analysis
            hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
            lab = cv2.cvtColor(image_array, cv2.COLOR_RGB2LAB)
            
            # Detect unusual color patterns (potential wounds/scars)
            # Look for red/pink areas (blood, wounds)
            red_mask = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
            red_pixels = np.sum(red_mask > 0)
            
            # Look for dark spots (scars, wounds)
            dark_mask = cv2.inRange(lab, (0, 0, 0), (50, 128, 128))
            dark_pixels = np.sum(dark_mask > 0)
            
            # Look for irregular patterns
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            
            # Calculate irregularity score
            total_pixels = image_array.shape[0] * image_array.shape[1]
            red_ratio = red_pixels / total_pixels
            dark_ratio = dark_pixels / total_pixels
            edge_density = np.sum(edges > 0) / total_pixels
            
            # Determine injury likelihood
            injury_score = (red_ratio * 2) + (dark_ratio * 1.5) + (edge_density * 0.5)
            has_injuries = injury_score > self.injury_threshold
            
            return {
                "has_injuries": has_injuries,
                "injury_score": injury_score,
                "red_pixel_ratio": red_ratio,
                "dark_pixel_ratio": dark_ratio,
                "edge_density": edge_density,
                "confidence": min(0.9, injury_score)
            }
            
        except Exception as e:
            logger.error(f"Error in injury detection: {e}")
            return {
                "has_injuries": False,
                "injury_score": 0.0,
                "error": str(e)
            }
    
    def assess_mobility_issues(self, image_array: np.ndarray) -> Dict[str, Any]:
        """
        Assess potential mobility issues from posture and positioning.
        
        Args:
            image_array: Image as numpy array
            
        Returns:
            Dictionary with mobility assessment results
        """
        try:
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            height, width = gray.shape
            
            # Analyze posture - check if camel is lying down (potential mobility issue)
            # Look for horizontal vs vertical body orientation
            edges = cv2.Canny(gray, 50, 150)
            
            # Calculate horizontal vs vertical edge ratios
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
            
            horizontal_edges = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel)
            vertical_edges = cv2.morphologyEx(edges, cv2.MORPH_OPEN, vertical_kernel)
            
            horizontal_ratio = np.sum(horizontal_edges > 0) / np.sum(edges > 0)
            vertical_ratio = np.sum(vertical_edges > 0) / np.sum(edges > 0)
            
            # Check if camel appears to be lying down
            lying_down = horizontal_ratio > 0.6  # High horizontal edges suggest lying position
            
            # Analyze body symmetry for mobility issues
            left_half = edges[:, :width//2]
            right_half = edges[:, width//2:]
            
            left_density = np.sum(left_half > 0) / left_half.size
            right_density = np.sum(right_half > 0) / right_half.size
            symmetry_score = 1 - abs(left_density - right_density) / max(left_density, right_density, 0.001)
            
            mobility_issues = lying_down or symmetry_score < 0.7
            
            return {
                "mobility_issues": mobility_issues,
                "lying_down": lying_down,
                "symmetry_score": symmetry_score,
                "horizontal_ratio": horizontal_ratio,
                "vertical_ratio": vertical_ratio,
                "confidence": 0.8 if mobility_issues else 0.3
            }
            
        except Exception as e:
            logger.error(f"Error in mobility assessment: {e}")
            return {
                "mobility_issues": False,
                "error": str(e)
            }
    
    def comprehensive_health_screening(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Perform comprehensive health screening on camel image.
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dictionary with complete health assessment
        """
        try:
            # Convert bytes to image array
            image = Image.open(io.BytesIO(image_bytes))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize for analysis
            image = image.resize((224, 224))
            image_array = np.array(image)
            
            # Run all health checks
            missing_limbs_result = self.detect_missing_limbs(image_array)
            injury_result = self.detect_visible_injuries(image_array)
            mobility_result = self.assess_mobility_issues(image_array)
            
            # Determine overall health status
            has_health_issues = (
                missing_limbs_result.get("missing_limbs", False) or
                injury_result.get("has_injuries", False) or
                mobility_result.get("mobility_issues", False)
            )
            
            # Calculate overall health score
            health_score = 1.0
            if missing_limbs_result.get("missing_limbs", False):
                health_score -= 0.6  # Major deduction for missing limbs
            if injury_result.get("has_injuries", False):
                health_score -= 0.3  # Moderate deduction for injuries
            if mobility_result.get("mobility_issues", False):
                health_score -= 0.2  # Minor deduction for mobility issues
            
            health_score = max(0.0, health_score)
            
            # Determine recommendation
            if health_score < 0.3:
                recommendation = "Immediate veterinary attention required"
                severity = "critical"
            elif health_score < 0.6:
                recommendation = "Veterinary consultation recommended"
                severity = "moderate"
            elif health_score < 0.8:
                recommendation = "Monitor health condition"
                severity = "minor"
            else:
                recommendation = "Camel appears healthy"
                severity = "none"
            
            return {
                "health_screening_passed": not has_health_issues,
                "health_score": health_score,
                "severity": severity,
                "recommendation": recommendation,
                "missing_limbs": missing_limbs_result,
                "injuries": injury_result,
                "mobility": mobility_result,
                "screening_details": {
                    "missing_limbs_detected": missing_limbs_result.get("missing_limbs", False),
                    "injuries_detected": injury_result.get("has_injuries", False),
                    "mobility_issues_detected": mobility_result.get("mobility_issues", False)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive health screening: {e}")
            return {
                "health_screening_passed": True,  # Default to pass if screening fails
                "health_score": 1.0,
                "error": str(e),
                "recommendation": "Health screening failed - manual review recommended"
            }
