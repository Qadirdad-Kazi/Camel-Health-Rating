# ML Models Directory

This directory contains the machine learning models used for camel image analysis.

## Model Files

- `camel_model.h5` - Main TensorFlow/Keras model for camel rating prediction

## Model Requirements

The model should:
- Accept input images of size 224x224x3 (RGB)
- Return predictions for:
  - Overall rating (1-10 scale)
  - Feature scores for: body_shape, head_structure, leg_condition, coat_condition, overall_fitness

## Model Input/Output Format

### Input
- Image tensor: (1, 224, 224, 3)
- Normalized pixel values: [0, 1]

### Output
- Rating: Float value [0, 1] (will be scaled to 1-10)
- Features: Array of 5 feature scores [0, 1]

## Training Data

The model should be trained on a diverse dataset of camel images with:
- Various breeds and ages
- Different lighting conditions
- Multiple angles and poses
- Expert-rated quality scores

## Performance Targets

- Response time: < 8 seconds
- Accuracy: > 85% on validation set
- Robustness: Handle various image qualities and conditions

## Model Updates

To update the model:
1. Train new model with improved dataset
2. Validate performance metrics
3. Replace `camel_model.h5` file
4. Restart the backend service

## Fallback Behavior

If no model file is found, the system will use mock predictions for demonstration purposes.
