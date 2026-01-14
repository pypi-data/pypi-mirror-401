# NeuralForge Quick Start Guide

NeuralForge is an **AI-native ML API framework** designed to help ML engineers and developers deploy, manage, and monitor machine learning models with production-grade reliability and high-performance.

---

## 📋 Prerequisites

- Python 3.10 or higher
- pip package manager
- (Optional) Redis for caching and rate limiting

---

## 🚀 Installation

### From Source (Current)

```bash
# Clone the repository
git clone https://github.com/rockstream/neuralforge.git
cd neuralforge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e .

# Verify installation
python -c "import neuralforge; print(neuralforge.__version__)"
```

### From PyPI (Recommended)

```bash
pip install nforge

# With PyTorch support
pip install nforge[pytorch]

# Full installation
pip install nforge[all]
```

---

## 🎯 Your First Application (2 Minutes)

Create a file called `app.py`:

```python
from neuralforge import NeuralForge
from pydantic import BaseModel

# Initialize app
app = NeuralForge(title="My First API", version="1.0.0")

# Define request/response models
class PredictionInput(BaseModel):
    text: str

class PredictionOutput(BaseModel):
    sentiment: str
    confidence: float

# Create endpoint
@app.endpoint("/predict", methods=["POST"])
async def predict(data: PredictionInput) -> PredictionOutput:
    # Simple sentiment analysis
    sentiment = "positive" if "good" in data.text.lower() else "negative"
    confidence = 0.95 if "good" in data.text.lower() else 0.85
    
    return PredictionOutput(
        sentiment=sentiment,
        confidence=confidence
    )

# Run the app
if __name__ == "__main__":
    app.run(port=8000)
```

**Run it:**
```bash
python app.py
```

**Test it:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This is good!"}'
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.95
}
```

---

## 🛡️ Adding Authentication (3 Minutes)

Add API key authentication:

```python
from neuralforge import NeuralForge
from neuralforge.auth import AuthManager
from neuralforge.dependencies import Depends
from pydantic import BaseModel

app = NeuralForge(title="Secure ML API", version="1.0.0")

# Setup authentication
auth = AuthManager(app)

class PredictionInput(BaseModel):
    text: str

@app.endpoint("/predict", methods=["POST"])
async def predict(
    data: PredictionInput,
    api_key: str = Depends(auth.verify_api_key)  # Require API key
):
    sentiment = "positive" if "good" in data.text.lower() else "negative"
    return {"sentiment": sentiment}

# Create API key (run once)
@app.endpoint("/create-key", methods=["POST"])
async def create_key(user_id: str, db = Depends(auth.get_db_session)):
    result = await auth.create_api_key(
        db_session=db,
        user_id=user_id,
        name=f"{user_id}'s key",
        expires_days=365
    )
    return result  # Returns: {"key": "nf_...", "user_id": "...", ...}

if __name__ == "__main__":
    app.run(port=8000)
```

**Create an API key:**
```bash
curl -X POST "http://localhost:8000/create-key?user_id=user123"
```

**Use the API key:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "X-API-Key: nf_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is great!"}'
```

---

## 🎨 Adding Rate Limiting (2 Minutes)

Protect your endpoints with rate limiting:

```python
from neuralforge import NeuralForge
from neuralforge.decorators import rate_limit
from pydantic import BaseModel

app = NeuralForge(title="Rate Limited API", version="1.0.0")

class PredictionInput(BaseModel):
    text: str

# Limit to 10 requests per minute
@app.endpoint("/predict", methods=["POST"])
@rate_limit(requests=10, per="minute")
async def predict(data: PredictionInput):
    sentiment = "positive" if "good" in data.text.lower() else "negative"
    return {"sentiment": sentiment}

# Expensive operation: 5 requests per hour
@app.endpoint("/expensive", methods=["POST"])
@rate_limit(requests=5, per="hour")
async def expensive_operation():
    # Expensive ML inference
    return {"status": "done"}

if __name__ == "__main__":
    app.run(port=8000)
```

---

## 💾 Adding Database (4 Minutes)

Store predictions in a database:

```python
from neuralforge import NeuralForge
from neuralforge.dependencies import Depends, get_db_session
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime
from neuralforge.db.base import Base
from datetime import datetime

app = NeuralForge(title="ML API with DB", version="1.0.0")

# Define database model
class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=app.db.engine)

class PredictionInput(BaseModel):
    text: str

@app.endpoint("/predict", methods=["POST"])
async def predict(
    data: PredictionInput,
    db = Depends(get_db_session)  # Auto-commit/rollback
):
    # Make prediction
    sentiment = "positive" if "good" in data.text.lower() else "negative"
    confidence = 0.95 if sentiment == "positive" else 0.85
    
    # Save to database
    prediction = Prediction(
        text=data.text,
        sentiment=sentiment,
        confidence=confidence
    )
    db.add(prediction)
    # Auto-commit on success, auto-rollback on error!
    
    return {
        "id": prediction.id,
        "sentiment": sentiment,
        "confidence": confidence
    }

if __name__ == "__main__":
    app.run(port=8000)
```

---

## 🧪 Testing Your API (3 Minutes)

Write tests with the built-in test client:

```python
# test_app.py
import pytest
from neuralforge.testing import TestClient
from app import app

@pytest.mark.asyncio
async def test_predict():
    async with TestClient(app) as client:
        response = await client.post(
            "/predict",
            json={"text": "This is good!"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] == "positive"
        assert data["confidence"] > 0.9

@pytest.mark.asyncio
async def test_health():
    async with TestClient(app) as client:
        response = await client.get("/health")
        assert response.status_code == 200
```

**Run tests:**
```bash
pytest test_app.py -v
```

---

## 🐳 Docker Deployment (2 Minutes)

Deploy with Docker:

```bash
# Copy environment template
cp env.template .env

# Edit .env with your settings
# DATABASE_URL=postgresql://...
# REDIS_URL=redis://...
# SECRET_KEY=your-secret-key

# Start everything
docker-compose up -d

# Check health
curl http://localhost:8000/health
```

---

## 📚 Next Steps

### **Learn More:**
- **[Production Quickstart](docs/PRODUCTION_QUICKSTART.md)** - Complete production guide
- **[Production Features](docs/PRODUCTION_FEATURES.md)** - All features explained
- **[Code Quality Guide](docs/CODE_QUALITY.md)** - Quality standards and best practices
- **[Docker Deployment](docs/deployment/DOCKER_DEPLOYMENT.md)** - Complete Docker guide

### **Explore Examples:**
- Model Registry - Version your models
- A/B Testing - Test improvements safely
- Monitoring - Track predictions
- Drift Detection - Detect data drift

### **Production Features:**
- ✅ Global error handling
- ✅ Request/response logging
- ✅ Rate limiting (global + per-endpoint)
- ✅ CORS middleware
- ✅ Security headers
- ✅ Health checks
- ✅ Metrics collection
- ✅ Database integration
- ✅ Authentication & authorization
- ✅ Caching (Redis + memory)

---

## 💡 Tips

### **Environment Variables**
Create a `.env` file:
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-min-32-chars
LOG_LEVEL=INFO
```

### **Logging**
```python
from neuralforge.log_config import get_logger

logger = get_logger(__name__)

logger.info("Processing request")
logger.error("Error occurred", exc_info=True)
```

### **Validation**
```python
from neuralforge.validators import CommonValidators
from pydantic import BaseModel, validator

class Input(BaseModel):
    text: str
    email: str
    
    @validator('text')
    def validate_text(cls, v):
        return CommonValidators.validate_text_length(v, max_len=5000)
    
    @validator('email')
    def validate_email(cls, v):
        return CommonValidators.validate_email(v)
```

---

## 🎯 Common Patterns

### **Complete Production Endpoint**
```python
from neuralforge import NeuralForge
from neuralforge.auth import AuthManager
from neuralforge.decorators import rate_limit, cache
from neuralforge.dependencies import Depends, get_db_session
from pydantic import BaseModel

app = NeuralForge()
auth = AuthManager(app)

class Input(BaseModel):
    text: str

@app.endpoint("/predict", methods=["POST"])
@cache(ttl=300)  # Cache for 5 minutes
@rate_limit(requests=100, per="minute")  # Rate limit
async def predict(
    data: Input,
    db = Depends(get_db_session),  # Database
    api_key: str = Depends(auth.verify_api_key)  # Auth
):
    # Your ML logic here
    result = "positive"
    
    # Save to database
    db.add(Prediction(text=data.text, result=result))
    
    return {"result": result}
```

---

## 🆘 Troubleshooting

**Import errors?**
```bash
pip install -r requirements.txt
```

**Database errors?**
```bash
# Check DATABASE_URL in .env
# Create tables: python create_tables.py
```

**Port already in use?**
```bash
# Change port in .env or:
app.run(port=8001)
```

---

## 📞 Get Help

- **Documentation:** [docs/README.md](docs/README.md)
- **Issues:** [GitHub Issues](https://github.com/rockstream/neuralforge/issues)
- **Examples:** [examples/](examples/)

---

**🎉 You're ready to build production ML APIs with NeuralForge!**

**Next:** Check out the [Production Quickstart](docs/PRODUCTION_QUICKSTART.md) for advanced features!
