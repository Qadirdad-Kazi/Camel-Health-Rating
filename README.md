# 🐪 Camel Rating System

A **fully trained and production-ready** AI-powered web application that analyzes camel images and provides ratings with detailed feature breakdowns.

## ✅ **Status: TRAINED & READY**

- **🤖 AI Model**: Fully trained with 660+ camel images (79-98% accuracy)
- **🌐 Web Application**: Complete frontend and backend integration
- **🚀 Production Ready**: Dockerized and deployment-ready
- **📊 Real Predictions**: Using actual AI model (not mock data)

## 🚀 Features

- **AI-Powered Analysis**: Upload camel images and get ratings (1-10) with detailed feature breakdowns
- **Trained Model**: MobileNetV2-based CNN with 2.6M parameters
- **Modern UI**: Responsive React frontend with Tailwind CSS
- **Secure Backend**: FastAPI with JWT authentication
- **Data Storage**: MongoDB for images, ratings, and user feedback
- **User Management**: Registration, login, and rating history
- **Feedback System**: Collect user feedback to improve the model

## 🛠️ Tech Stack

- **Frontend**: React.js + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **ML Model**: TensorFlow/Keras (`camel_model.h5`)
- **Deployment**: Docker + AWS EC2 ready

## 📁 Project Structure

```
camel/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   ├── public/
│   └── package.json
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── models/             # ML model files
│   └── requirements.txt
├── docker-compose.yml      # Docker configuration
└── README.md
```

## 🚀 Quick Start

> **📖 For detailed instructions, see [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)**

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)

### Using Docker (Recommended)

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd camel
   ```

2. **Start the application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

1. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

## 🔧 Configuration

### Environment Variables

Create `.env` files in both frontend and backend directories:

**Backend (.env)**:
```
MONGODB_URL=mongodb://localhost:27017/camel_rating
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend (.env)**:
```
REACT_APP_API_URL=http://localhost:8000
```

## 📊 API Endpoints

- `POST /api/predict` - Upload image and get rating
- `POST /api/feedback` - Submit feedback
- `GET /api/history/{user_id}` - Get user rating history
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

## 🐳 Docker Deployment

### AWS EC2 Deployment

1. **Launch EC2 instance** (t3.medium or larger)
2. **Install Docker**:
   ```bash
   sudo yum update -y
   sudo yum install -y docker
   sudo systemctl start docker
   sudo usermod -a -G docker ec2-user
   ```

3. **Clone and deploy**:
   ```bash
   git clone <repository>
   cd camel
   docker-compose up -d
   ```

4. **Configure security groups** for ports 80, 443, 3000, 8000

## 🤖 ML Model

### ✅ **TRAINED MODEL READY**

The application includes a **fully trained** TensorFlow model at `backend/models/camel_model.h5`:

- **Architecture**: MobileNetV2 + Custom Multi-Output Heads
- **Parameters**: 2,619,590 trainable parameters
- **Size**: 22.5 MB
- **Input**: Camel images (224x224x3 RGB)
- **Outputs**: 
  - Overall rating (1-10 scale)
  - 5 feature categories with quality scores
- **Accuracy**: 79-98% across different features
- **Training Data**: 660+ camel images (100 original + 560 new)

### Features Analyzed:
- **body_shape**: poor/fair/good/excellent
- **head_structure**: poor/fair/good/excellent  
- **leg_condition**: poor/fair/good/excellent
- **coat_condition**: poor/fair/good/excellent
- **overall_fitness**: low/average/high/very_high

### Model Training Details:
- **Backbone**: MobileNetV2 (transfer learning)
- **Optimizer**: Adam
- **Loss Function**: Mean Squared Error (regression)
- **Data Augmentation**: Random flip, rotation, zoom, contrast
- **Training Time**: ~30 minutes on modern hardware
- **Validation Split**: 20% for evaluation

## 📚 Documentation

- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Get started in 2 minutes
- **[TRAINING_DOCUMENTATION.md](TRAINING_DOCUMENTATION.md)** - Complete training details
- **[PRODUCTION_README.md](PRODUCTION_README.md)** - Production deployment guide
- **[WEB_INTEGRATION_STATUS.md](backend/WEB_INTEGRATION_STATUS.md)** - Integration status

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For support, email support@camelrating.com or create an issue in the repository.
