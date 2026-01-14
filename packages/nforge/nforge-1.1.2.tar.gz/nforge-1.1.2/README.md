<div align="center">

# 🚀 NeuralForge

### The AI-Native ML API Framework
Deploy ML models to production in minutes, not weeks.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/nforge.svg)](https://pypi.org/project/nforge/)
[![Downloads](https://img.shields.io/pypi/dm/nforge.svg)](https://pypi.org/project/nforge/)
[![CI](https://github.com/rockstream/neuralforge/workflows/CI/badge.svg)](https://github.com/rockstream/neuralforge/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-157%2B%20passing-brightgreen.svg)](tests/)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](CHANGELOG.md)

</div>

---

## 🎯 What is NeuralForge?

**NeuralForge is the modern Python framework for deploying ML models to production.**

Built specifically for ML Engineers and Data Scientists, NeuralForge provides everything you need to serve ML models at scale:

- ✅ **Model Registry** - Version and manage all your models
- ✅ **A/B Testing** - Safely roll out model improvements
- ✅ **Monitoring** - Track predictions and detect drift
- ✅ **Auto-scaling** - Handle traffic spikes automatically
- ✅ **Production-ready** - Security, logging, metrics built-in

### Why NeuralForge?

**FastAPI is great for general APIs. NeuralForge is built specifically for ML.**

| Feature | FastAPI | NeuralForge |
|---------|---------|-------------|
| **Model Versioning** | ❌ Manual | ✅ Built-in |
| **A/B Testing** | ❌ Manual | ✅ Built-in |
| **Drift Detection** | ❌ Manual | ✅ Built-in |
| **Batch Prediction** | ❌ Manual | ✅ Built-in |
| **GPU Management** | ❌ Manual | ✅ Built-in |
| **ML Monitoring** | ❌ Manual | ✅ Built-in |

---

## 🚀 Quick Start

### Installation

**Basic Installation:**
```bash
pip install nforge
```

**With ML Optimization (PyTorch):**
```bash
pip install nforge[pytorch]
```

**Full Installation:**
```bash
pip install nforge[all]
```

> **Note:** PyTorch is optional. The core framework works perfectly without it. PyTorch is only needed for model quantization and GPU acceleration features. See [docs/guides/OPTIONAL_DEPENDENCIES.md](docs/guides/OPTIONAL_DEPENDENCIES.md) for details.

### Your First ML API (5 minutes)

```python
from neuralforge import NeuralForge
from pydantic import BaseModel

# Create app
app = NeuralForge()

# Define input/output
class PredictionInput(BaseModel):
    text: str

class PredictionOutput(BaseModel):
    sentiment: str
    confidence: float

# Create endpoint
@app.post("/predict")
async def predict(data: PredictionInput) -> PredictionOutput:
    # Your ML model here
    sentiment = "positive" if "good" in data.text.lower() else "negative"
    
    return PredictionOutput(
        sentiment=sentiment,
        confidence=0.95
    )

# Run
if __name__ == "__main__":
    app.run(port=8000)
```

**Test it:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This is great!"}'
```

---

## 🎨 Key Features

### 1. **Model Registry & Versioning**

Manage multiple model versions with ease:

```python
from neuralforge.ml import ModelRegistry

registry = ModelRegistry()

# Register models
@registry.register(name="sentiment", version="1.0.0")
class SentimentModelV1:
    def predict(self, text: str):
        return {"sentiment": "positive", "confidence": 0.9}

@registry.register(name="sentiment", version="2.0.0")
class SentimentModelV2:
    def predict(self, text: str):
        # Improved model
        return {"sentiment": "positive", "confidence": 0.95}

# Load specific version
model = await registry.load("sentiment", version="1.0.0")
```

### 2. **Built-in A/B Testing**

Test model improvements safely:

```python
from neuralforge.ml import ABTest

# Create A/B test
ab_test = ABTest(
    name="sentiment-v2-test",
    variants={
        "control": {"version": "1.0.0", "traffic": 0.7},
        "treatment": {"version": "2.0.0", "traffic": 0.3}
    }
)

@app.post("/predict")
@ab_test.route()
async def predict(data: Input):
    # Automatically selects variant
    model = await ab_test.get_model()
    return model.predict(data)
```

### 3. **Prediction Monitoring**

Track model performance in production:

```python
from neuralforge.ml import PredictionMonitor

monitor = PredictionMonitor(
    model_name="sentiment",
    track_latency=True,
    alert_on_degradation=True
)

@app.post("/predict")
@monitor.track()
async def predict(data: Input):
    # Automatically logged and monitored
    return model.predict(data)
```

### 4. **Production Features Built-in**

Everything you need for production:

- ✅ **Authentication** - API keys, JWT, OAuth2
- ✅ **Rate Limiting** - Protect your API
- ✅ **CORS** - Cross-origin requests
- ✅ **Logging** - Structured logging with masking
- ✅ **Metrics** - Prometheus-compatible
- ✅ **Health Checks** - Liveness and readiness probes

---

## 📚 Examples

### Sentiment Analysis
```python
# See examples/ml_api/main.py
# Full working sentiment analysis API with:
# - User authentication
# - Prediction history
# - Analytics
# - Rate limiting
```

### Text Generation with Streaming
```python
from neuralforge import NeuralForge
from neuralforge.streaming import SSEResponse, TokenStreamBuilder

app = NeuralForge()

@app.stream("/generate")
async def generate(prompt: str):
    builder = TokenStreamBuilder()
    
    # Stream tokens as they're generated
    async for token in llm.generate(prompt):
        yield builder.add_token(token)
    
    yield builder.finish()
```

### gRPC Server
```python
from neuralforge.grpc import GRPCServer, GRPCServicer, grpc_method

# Enable gRPC alongside HTTP
grpc_server = app.enable_grpc(port=50051)

class InferenceService(GRPCServicer):
    @grpc_method(response_streaming=True)
    async def StreamPredict(self, request, context):
        async for token in model.generate(request.prompt):
            yield TokenResponse(token=token)

grpc_server.register_service(InferenceService)
```

### Benchmarking
```bash
# Run latency benchmarks
neuralforge benchmark run --scenario latency

# Compare against FastAPI/BentoML
neuralforge benchmark compare --against fastapi,bentoml

# Generate HTML report
neuralforge benchmark report --format html --output report.html
```

### OpenTelemetry Tracing
```python
from neuralforge.observability import TracingManager, configure_structured_logging

# Configure tracing
tracer = TracingManager(service_name="ml-api")
tracer.configure(exporter="otlp", endpoint="localhost:4317")

# Structured JSON logging
configure_structured_logging(
    service_name="ml-api",
    format_type="json"
)
```

---

## 🐳 Docker Deployment

### One-Command Deployment

```bash
# Copy environment template
cp env.template .env

# Start everything (API + PostgreSQL + Redis)
docker compose up -d

# Check health
curl http://localhost:8000/health
```

See [docs/deployment/DOCKER_QUICKSTART.md](docs/deployment/DOCKER_QUICKSTART.md) for details.

---

## 📚 Documentation

### **Quick Start**
- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Production Quickstart](docs/PRODUCTION_QUICKSTART.md)** - Production-ready setup

### **Core Documentation**
- **[Production Features](docs/PRODUCTION_FEATURES.md)** - All production features explained
- **[Core Functionalities](docs/CORE_FUNCTIONALITIES.md)** - Framework capabilities
- **[Code Structure](docs/CODE_STRUCTURE.md)** - Project organization
- **[Code Quality](docs/CODE_QUALITY.md)** - Quality standards and best practices

### **Deployment**
- **[Docker Deployment](docs/deployment/DOCKER_DEPLOYMENT.md)** - Complete Docker guide
- **[Docker Quickstart](docs/deployment/DOCKER_QUICKSTART.md)** - Quick Docker setup

### **Guides**
- **[Testing Examples](docs/guides/TESTING_EXAMPLES.md)** - Testing patterns
- **[Optional Dependencies](docs/guides/OPTIONAL_DEPENDENCIES.md)** - ML framework options

### **Contributing**
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute
- **[Changelog](CHANGELOG.md)** - Version history

**📖 [Complete Documentation Index](docs/README.md)**

---

## 🏗️ Architecture

```
NeuralForge
├── Core Framework
│   ├── Async Routing (FastAPI-like)
│   ├── Dependency Injection
│   ├── Database Integration (SQLAlchemy)
│   └── Middleware Stack
│
├── ML Features (v0.8+)
│   ├── Model Registry
│   ├── A/B Testing
│   ├── Prediction Monitoring
│   └── Drift Detection
│
└── Production Features
    ├── Authentication & Authorization
    ├── Rate Limiting
    ├── Logging & Metrics
    └── Docker Deployment
```

---

## 🧪 Development

### Setup

```bash
git clone https://github.com/rockstream/neuralforge.git
cd neuralforge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=neuralforge --cov-report=html

# Specific test
pytest tests/test_routing.py -v
```

**Current Status:** ✅ 117/117 tests passing

---

## 🗺️ Roadmap

### ✅ v0.5 (Current) - Core Framework
- [x] Async routing with validation
- [x] Dependency injection
- [x] Database integration (SQLAlchemy)
- [x] Middleware (CORS, Security, Logging, Rate Limiting)
- [x] Docker deployment
- [x] 117 tests passing

### 🔄 v0.8 (6 weeks) - ML Essentials
- [ ] Model Registry & Versioning
- [ ] A/B Testing Framework
- [ ] Prediction Monitoring
- [ ] 3+ ML Examples

### 🎯 v1.0 (12 weeks) - Production ML Framework
- [ ] Drift Detection
- [ ] Model Optimization
- [ ] GPU Support
- [ ] Auto-scaling
- [ ] Enterprise Features

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas we need help:**
- 🐛 Bug fixes
- 📝 Documentation
- 🎨 ML examples
- 🔌 ML tool integrations
- ⚡ Performance optimization

---

## 📊 Comparison

### NeuralForge vs FastAPI

**Use FastAPI when:**
- Building general-purpose APIs
- Need maximum flexibility
- Not ML-specific

**Use NeuralForge when:**
- Deploying ML models
- Need model versioning
- Want A/B testing built-in
- Need drift detection
- ML-specific features matter

### NeuralForge vs BentoML

**NeuralForge:**
- ✅ General-purpose + ML-specific
- ✅ FastAPI-like developer experience
- ✅ More flexible

**BentoML:**
- ✅ ML-only focus
- ✅ More opinionated
- ✅ Mature ecosystem

---

## 🚀 Enterprise Agent System

[![CI](https://github.com/rockstream/neuralforge/actions/workflows/ci.yml/badge.svg)](https://github.com/rockstream/neuralforge/actions/workflows/ci.yml)
[![Code Quality](https://github.com/rockstream/neuralforge/actions/workflows/code-quality.yml/badge.svg)](https://github.com/rockstream/neuralforge/actions/workflows/code-quality.yml)

Production-ready code quality and security analysis powered by NeuralForge Enterprise Agents.

### 🎯 Features
- **Automated Quality Checks**: Enterprise-grade code analysis on every PR
- **Security Scanning**: SAST, dependency scanning, and secret detection
- **CI/CD Integration**: GitHub Actions workflows with automated reporting
- **Metrics & Monitoring**: Prometheus-compatible metrics collection

### 📊 Current Status
- **Enterprise Coverage**: 75% (Code Quality + Security + Observability + Integration)
- **Test Coverage**: 71% ([View Report](.agent/test_enterprise_agent.py))
- **Security Scans**: Automated via [Security Agent v2](.agent/security_agent_v2.py)

### 📚 Documentation
- [Deployment Guide](.agent/DEPLOYMENT_GUIDE.md) - Production deployment instructions
- [Quick Reference](.agent/QUICK_REFERENCE.md) - Daily CLI commands
- [Enterprise Agent Docs](.agent/ENTERPRISE_AGENT_DOCS.md) - Technical documentation

### 🔧 Quick Start
```bash
# Run quality analysis
python .agent/cli.py analyze --quick

# Run security scan
python .agent/cli.py security

# View metrics
python .agent/cli.py metrics
```

**Note**: Replace `YOUR_USERNAME` in badge URLs with your GitHub username for live status badges.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Inspired by [FastAPI](https://fastapi.tiangolo.com/) - Amazing DX
- Inspired by [BentoML](https://www.bentoml.com/) - ML serving patterns
- Built with [Pydantic](https://pydantic.dev/), [SQLAlchemy](https://www.sqlalchemy.org/), and [Uvicorn](https://www.uvicorn.org/)

---

## 📞 Support

- **Documentation**: [Coming Soon]
- **GitHub Issues**: [Report bugs](https://github.com/rockstream/neuralforge/issues)
- **Discord**: [Join community](https://discord.gg/neuralforge) (Coming Soon)
- **Email**: support@neuralforge.dev

---

<div align="center">

**Built with ❤️ for ML Engineers**

[Get Started](#-quick-start) • [Documentation](#-documentation) • [Examples](#-examples)

</div>
