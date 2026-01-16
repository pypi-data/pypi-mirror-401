NECECV

NECECV is an advanced AI systems platform that combines:

Generative Language Models

Computer Vision Intelligence

Enterprise-grade Semantic Caching Infrastructure

NECECV is designed to act as a foundation layer for building high-performance AI agents, copilots, and automation systems.

Features
1. Generative Universe Engine

A hierarchical generative language model inspired by planetary systems, enabling layered semantic reasoning and structured text generation.

nececv.planet_generative_model

2. Computer Vision – PreEdge

A hybrid deep-learning + epsilon-learning edge detection system built on top of VGG16, Canny, and Sobel filtering.

Supports:

Object classification

Edge density estimation

Adaptive edge detection

Visualization

nececv.obj_det.PreEdge

3. Enterprise Semantic Cache

A RAM-bounded, vector-aware cache layer for LLMs, APIs, and AI agents.

Supports:

Semantic similarity matching

LRU eviction

FTPL (learning-based eviction)

Real RAM budgeting

nececv.semantic_cache


This allows NECECV to behave like real AI infrastructure used in production systems.

Installation
pip install nececv

1️⃣ Generative Universe (LLM)
from nececv.planet_generative_model import llm_genUniverse

model = llm_genUniverse()
print(model.generate("AI will change the world"))

2️⃣ Computer Vision (PreEdge)
from nececv import PreEdge

detector = PreEdge()

predictions = detector.detect_object_probability("image.jpg")
edges = detector.generate_edge_image("image.jpg", predictions, epsilon=0.1, iterations=10)

detector.display_results("image.jpg", predictions=predictions, edge_image="Canny")

3️⃣ Semantic Cache (LLM Infra)
import nececv

cache = nececv.LRUSemanticCache(max_ram_mb=512)

def llm(query):
    return "LLM response for: " + query

router = nececv.SemanticRouter(cache, llm)

embedding = embed("reset password")   # user-provided embedding
router.query("reset password", embedding)


The cache automatically:

Finds semantic matches

Reuses previous outputs

Evicts data when RAM limit is reached