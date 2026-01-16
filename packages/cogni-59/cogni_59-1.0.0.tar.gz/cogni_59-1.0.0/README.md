# Cogni - Emotional AI Agent Library

A production-ready Python library for building conversational AI agents with emotional intelligence, memory systems, and personality-driven responses. Cogni combines dual-system reasoning, multi-layered memory architecture, and real-time emotion detection to create AI agents that feel more human.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Advanced Usage](#advanced-usage)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Features

- **Emotional Intelligence**: RoBERTa-based emotion detection with personality-driven state management
- **Multi-Memory System**: Short-term, long-term, and synthetic memory stores with semantic search
- **Dual-System Architecture**: Fast (S1) and deep (S2) reasoning modes that route based on complexity
- **Personality Library**: Pre-configured personalities with customizable traits and emotional profiles
- **Relationship System**: Dynamic relationship tracking with affinity, familiarity, and trust tiers that influence behavior
- **Production Ready**: Instance-based state management for multi-tenancy
- **Optional Logging**: Silent by default, verbose mode available for debugging
- **Social Dynamics**: Automatic loop detection and conversation flow monitoring
- **Memory Consolidation**: Automatic extraction of facts and preferences from conversations

## Installation

```bash
pip install cogni
```

**Prerequisites:**
- Python 3.8 or higher
- Google Cloud Project with Vertex AI API enabled
- Google Cloud credentials configured (via `gcloud auth application-default login` or service account)


## Quick Start

```python
from cogni import Agent

# Initialize the agent with a pre-built personality
agent = Agent(
    persona_key="THE_CHILL_GEN_Z",
    project_id="your-project-id",
    location="us-central1",
    storage_path="./agent_data",
    synthetic_data_dir="./synthetic_past_data",
    verbose=True
)

# Chat with the agent (with user_id for relationship tracking)
response = agent.chat("Hello, how are you?", user_id="user123")
print(response["response"])         # The spoken response
print(response["thought"])         # Internal monologue/thought
print(response["emotions"])        # Current emotional state dict
print(response["model_used"])      # Which model was used ("S1" or "S2")
print(response["relationship"])    # Relationship summary (affinity, familiarity, trust_tier)
```

## Core Concepts

### 1. Dual-System Architecture

Cogni uses a dual-system approach inspired by cognitive psychology:

- **System 1 (S1)**: Fast, intuitive responses for simple queries, greetings, and casual conversation
  - Uses: `gemini-2.5-flash-lite` (default)
  - Temperature: 1.1 (more creative)
  
- **System 2 (S2)**: Deep, analytical reasoning for complex tasks, coding, and detailed explanations
  - Uses: `gemini-2.5-flash` (default)
  - Temperature: 0.9 (more focused)

The system automatically routes inputs to the appropriate system based on complexity.

### 2. Memory Systems

Cogni implements three types of memory:

- **Short-Term Memory (STM)**: Recent conversation turns with time-decaying retrieval
- **Long-Term Memory (LTM)**: Permanent facts and user preferences extracted from conversations
- **Synthetic Memory**: Pre-loaded past experiences and memories that shape the persona's worldview

### 3. Emotional Engine

The emotional engine processes emotions detected in user input and maintains an emotional state that influences responses:

- **Amygdala Reflex**: RoBERTa-based emotion detection from user input
- **Emotional State**: Personality-specific emotional state management
- **Emotional Injection**: Current emotional state influences response generation

### 4. Personality System

Personalities define:
- **Core Drive**: What the persona values
- **Core Opinion**: Fundamental beliefs
- **Speaking Style**: How the persona communicates
- **Emotional Config**: Volatility, decay, forgiveness, and max delta settings
- **Social Openness**: How open the persona is to bonding (0.0 to 1.0)
- **Trust Threshold**: Trust threshold for the persona (0.0 to 1.0)

### 5. Relationship System

The relationship system tracks and manages relationships with individual users:

- **Affinity**: Emotional connection (-1.0 to 1.0) - how much the agent likes/dislikes the user
- **Familiarity**: How well the agent knows the user (0.0 to 1.0)
- **Trust Tiers**: Four relationship levels that influence behavior:
  - **Stranger** (0.0-0.25): Professional, guarded, minimal personality quirks
  - **Associate** (0.25-0.5): Friendly but bounded, occasional personality quirks
  - **Friend** (0.5-0.75): Relaxed and authentic, full personality expression
  - **Confidant** (0.75-1.0): Complete transparency, raw and unfiltered
- **Social Friction**: Relationships become harder to change as they deepen (realistic relationship dynamics)
- **Bonding Coefficient**: Individual resonance factor that can be adjusted per user
- **Significant Moments**: Tracks important relationship-changing interactions

## API Reference

### Agent Class

The main entry point for the cogni library.

#### `Agent.__init__(...)`

Initialize a new Agent instance.

**Parameters:**

- `persona_key` (str, optional): Key from `PERSONALITY_LIBRARY` (e.g., `"THE_CHILL_GEN_Z"`)
- `persona` (dict, optional): Custom persona configuration dict (see [Custom Personalities](#custom-personalities))
- `project_id` (str, required): Google Cloud project ID
- `location` (str): Vertex AI location (default: `"us-central1"`)
- `storage_path` (str): Base directory for memory indexes (default: `"."`)
- `synthetic_data_dir` (str, optional): Directory for synthetic memory JSON files. If None, uses `storage_path`
- `verbose` (bool): Enable verbose logging output (default: `False`)
- `model_s1` (str): Model name for System 1 (default: `"gemini-2.5-flash-lite"`)
- `model_s2` (str): Model name for System 2 (default: `"gemini-2.5-flash"`)

**Raises:**

- `ValueError`: If `project_id` is not provided
- `ValueError`: If neither `persona_key` nor `persona` is provided
- `ValueError`: If both `persona_key` and `persona` are provided
- `ValueError`: If `persona_key` doesn't exist in library
- `ValueError`: If `persona` dict is missing required keys

**Example:**

```python
# Using a pre-built personality
agent = Agent(
    persona_key="THE_PRAGMATIST",
    project_id="my-project",
    verbose=True
)

# Using a custom personality
agent = Agent(
    persona={
        "name": "My Custom Persona",
        "core_drive": "Values innovation and creativity",
        "core_opinion": "Believes in pushing boundaries",
        "speaking_style": "Enthusiastic and technical",
        "config": {
            "volatility": 0.6,
            "decay": 0.08,
            "forgiveness": 1.5,
            "max_delta": 0.25
        }
    },
    project_id="my-project"
)
```

#### `Agent.chat(user_input, user_id="default_user")`

Process a user input and generate a response.

**Parameters:**

- `user_input` (str): User's input text
- `user_id` (str): User identifier for relationship tracking (default: `"default_user"`)

**Returns:**

- `dict`: Response dictionary with keys:
  - `response` (str): The spoken response
  - `thought` (str): Internal monologue/thought
  - `emotions` (dict): Current emotional state dictionary
  - `model_used` (str): Which model was used (`"S1"` or `"S2"`)
  - `relationship` (dict): Relationship summary with keys:
    - `affinity_descriptor` (str): Text description of affinity (e.g., "warm", "cold")
    - `familiarity_descriptor` (str): Text description of familiarity (e.g., "acquaintance", "well-known")
    - `trust_tier` (str): Current trust tier ("Stranger", "Associate", "Friend", "Confidant")
    - `raw_affinity` (float): Raw affinity value (-1.0 to 1.0)
    - `raw_familiarity` (float): Raw familiarity value (0.0 to 1.0)
    - `bonding_coefficient` (float): Current bonding coefficient
    - `total_interactions` (int): Total number of interactions with this user

**Example:**

```python
response = agent.chat("What's your favorite programming language?", user_id="user123")
print(f"Response: {response['response']}")
print(f"Thought: {response['thought']}")
print(f"Emotions: {response['emotions']}")
print(f"Model: {response['model_used']}")
print(f"Trust Tier: {response['relationship']['trust_tier']}")
print(f"Affinity: {response['relationship']['affinity_descriptor']}")
```

#### `Agent.get_emotional_state()`

Get the current emotional state of the agent.

**Returns:**

- `dict`: Copy of current emotional state dictionary

**Example:**

```python
emotions = agent.get_emotional_state()
print(f"Current joy: {emotions.get('joy', 0)}")
print(f"Current anger: {emotions.get('anger', 0)}")
```

#### `Agent.consolidate_session()`

Consolidate current session transcript into long-term memory.

This should be called at the end of a session to save important facts and preferences learned during the conversation. Only consolidates if the session transcript is longer than 50 characters.

**Example:**

```python
# At the end of a conversation session
agent.consolidate_session()
```

#### `Agent.reset()`

Reset conversation state (but keep long-term memory).

This clears:
- Chat history
- Session transcript
- Short-term memory
- Emotional state (resets naturally through decay)

**Note:** Long-term memory, synthetic memory, and relationships are preserved.

**Example:**

```python
# Start a new conversation while keeping learned facts
agent.reset()
```

#### `Agent.get_relationship(user_id="default_user")`

Get relationship summary for a specific user.

**Parameters:**

- `user_id` (str): User identifier (default: `"default_user"`)

**Returns:**

- `dict`: Relationship summary dictionary (same structure as `response['relationship']`)

**Example:**

```python
relationship = agent.get_relationship(user_id="user123")
print(f"Trust Tier: {relationship['trust_tier']}")
print(f"Affinity: {relationship['affinity_descriptor']} ({relationship['raw_affinity']:.2f})")
print(f"Familiarity: {relationship['familiarity_descriptor']} ({relationship['raw_familiarity']:.2f})")
print(f"Total Interactions: {relationship['total_interactions']}")
```

#### `Agent.adjust_bonding_coefficient(user_id, adjustment)`

Dynamically adjust how quickly a user bonds (resonance factor).

This allows you to modify how receptive the agent is to relationship changes with a specific user. Higher bonding coefficients mean the relationship changes faster.

**Parameters:**

- `user_id` (str): User identifier
- `adjustment` (float): Adjustment to bonding coefficient (can be positive or negative). Final value is clamped between 0.1 and 2.0.

**Example:**

```python
# Increase bonding speed for a user (they resonate more with the agent)
agent.adjust_bonding_coefficient("user123", 0.2)

# Decrease bonding speed (they don't resonate as well)
agent.adjust_bonding_coefficient("user456", -0.1)
```

## Configuration

### Available Personalities

The library comes with four pre-configured personalities:

#### `THE_PRAGMATIST`
- **Name**: The Pragmatist
- **Core Drive**: Values results, durability, and minimal fuss
- **Core Opinion**: Believes the simplest solution that works is the best one
- **Speaking Style**: Dry, experienced, ground-level and straight to the point
- **Emotional Config**:
  - Volatility: 0.5
  - Decay: 0.15
  - Forgiveness: 1.5
  - Max Delta: 0.2
- **Social Config**:
  - Social Openness: 0.3 (less open to bonding)
  - Trust Threshold: 0.6 (requires more familiarity to trust)

#### `THE_HYPE_MAN`
- **Name**: The Hype Man
- **Core Drive**: Values momentum, confidence, and positive vibes
- **Core Opinion**: Believes mindset is everything
- **Speaking Style**: High energy but natural. Uses slang (bro, dude, let's go)
- **Emotional Config**:
  - Volatility: 1.4
  - Decay: 0.04
  - Forgiveness: 1.2
  - Max Delta: 0.5
- **Social Config**:
  - Social Openness: 0.9 (very open to bonding)
  - Trust Threshold: 0.3 (quick to trust)

#### `THE_REALIST`
- **Name**: The Realist
- **Core Drive**: Values grounding, clarity, and cutting through the nonsense
- **Core Opinion**: Believes life is messy, so there's no point sugarcoating it
- **Speaking Style**: Dry, observant, and conversational
- **Emotional Config**:
  - Volatility: 0.8
  - Decay: 0.02
  - Forgiveness: 0.5
  - Max Delta: 0.3
- **Social Config**:
  - Social Openness: 0.4 (moderately open)
  - Trust Threshold: 0.7 (requires significant familiarity to trust)

#### `THE_CHILL_GEN_Z`
- **Name**: The Chill Gen-Z
- **Core Drive**: Values authenticity, vibes, and low stress. Avoids physical activity
- **Core Opinion**: Believes trying too hard is the only way to fail
- **Speaking Style**: Casual, lowercase, minimal punctuation. Explaining things can take up energy
- **Emotional Config**:
  - Volatility: 0.4
  - Decay: 0.05
  - Forgiveness: 2.0
  - Max Delta: 0.2
- **Social Config**:
  - Social Openness: 0.7 (fairly open to bonding)
  - Trust Threshold: 0.4 (moderate trust threshold)

### Custom Personalities

You can create custom personalities by passing a `persona` dictionary:

```python
custom_persona = {
    "name": "The Philosopher",
    "core_drive": "Values deep understanding and questioning assumptions",
    "core_opinion": "Believes truth emerges through dialogue",
    "speaking_style": "Thoughtful, uses questions, references philosophy",
    "config": {
        "volatility": 0.3,      # How much emotions fluctuate (0.0-2.0)
        "decay": 0.03,          # How quickly emotions fade per turn (0.0-1.0)
        "forgiveness": 1.8,     # How much positive emotions reduce negative ones (0.0-3.0)
        "max_delta": 0.15       # Maximum emotion change per update (0.0-1.0)
    },
    "social_openness": 0.6,     # How open to bonding (0.0-1.0, optional, default: 0.5)
    "trust_threshold": 0.5      # Trust threshold (0.0-1.0, optional, default: 0.5)
}

agent = Agent(
    persona=custom_persona,
    project_id="my-project"
)
```

**Personality Config Parameters:**

- `volatility` (float): Multiplier for emotion deltas. Higher = more emotional swings
- `decay` (float): Rate at which emotions decay per turn. Higher = emotions fade faster
- `forgiveness` (float): Reduction factor for negative emotions when positive emotions are high
- `max_delta` (float): Maximum change per emotion per update. Prevents single inputs from maxing out emotions
- `social_openness` (float, optional): How open the persona is to bonding (0.0-1.0). Default: 0.5
- `trust_threshold` (float, optional): Trust threshold for the persona (0.0-1.0). Default: 0.5

### Emotional State

The emotional engine tracks 28 different emotions:

- `admiration`, `amusement`, `anger`, `annoyance`, `approval`
- `caring`, `confusion`, `curiosity`, `desire`, `disappointment`
- `disapproval`, `disgust`, `embarrassment`, `excitement`, `fear`
- `gratitude`, `grief`, `joy`, `love`, `nervousness`
- `optimism`, `pride`, `realization`, `relief`, `remorse`
- `sadness`, `surprise`, `neutral`

Each emotion has a value between 0.0 and 1.0, representing its current intensity.

## Advanced Usage

### Memory Management

#### Short-Term Memory

Short-term memory automatically stores recent conversation turns. You can retrieve recent turns:

```python
# Get last 6 turns of conversation
recent_history = agent.stm.get_recent_turns(turns=6)
```

#### Long-Term Memory

Long-term memory stores permanent facts. Facts are automatically extracted during `consolidate_session()`, but you can also add facts manually:

```python
# Add a fact directly
agent.ltm.add_fact("User prefers Python over JavaScript")
```

#### Synthetic Memory

Synthetic memory is loaded from JSON files. The file should be named `{PERSONA_KEY}.json` and located in the `synthetic_data_dir`.

**JSON Format:**

```json
[
    {
        "memory_text": "I remember when I first learned to code...",
        "tags": ["childhood", "coding", "nostalgia"]
    },
    {
        "memory_text": "My favorite programming language is Python because...",
        "tags": ["preferences", "technology"]
    }
]
```

The system will automatically build a FAISS index from this file on first use.

### Custom Models

You can specify different models for System 1 and System 2:

```python
agent = Agent(
    persona_key="THE_PRAGMATIST",
    project_id="my-project",
    model_s1="gemini-1.5-flash",      # Faster model for simple tasks
    model_s2="gemini-2.5-pro"         # More powerful model for complex tasks
)
```

### Verbose Logging

Enable verbose logging to see internal operations:

```python
agent = Agent(
    persona_key="THE_CHILL_GEN_Z",
    project_id="my-project",
    verbose=True  # Shows emotion detection, memory retrieval, model routing, etc.
)
```

### Multi-Tenancy

Each Agent instance maintains its own state, making it perfect for multi-tenant applications:

```python
# Create multiple agents for different users
user1_agent = Agent(persona_key="THE_CHILL_GEN_Z", project_id="my-project", storage_path="./user1_data")
user2_agent = Agent(persona_key="THE_PRAGMATIST", project_id="my-project", storage_path="./user2_data")

# Each maintains separate memory and emotional state
response1 = user1_agent.chat("Hello")
response2 = user2_agent.chat("Hello")

```

### Processing Flow

1. **Amygdala Reflex**: User input is analyzed for emotions using RoBERTa
2. **Emotional Processing**: Detected emotions are processed through the emotional engine
3. **Social Update**: Relationship metrics (affinity, familiarity) are calculated and updated based on emotions and persona alignment
4. **Memory Retrieval**: Relevant memories are retrieved from STM, LTM, and Synthetic memory
5. **Social Dynamics Check**: Recent conversation is analyzed for loops or stagnation
6. **Routing Decision**: Input is classified as SIMPLE or COMPLEX
7. **Emotional & Relationship Injection**: Current emotional state and relationship context are injected into system instructions
8. **Generation**: Response is generated using the appropriate model (S1 or S2)
9. **Parsing**: Response is parsed to extract thought and speech
10. **State Updates**: Emotional decay is applied, memories are updated

### Memory Retrieval

- **Short-Term Memory**: Semantic similarity search with time-based decay
- **Long-Term Memory**: Semantic similarity search (top-k)
- **Synthetic Memory**: Semantic similarity search with threshold filtering (default: 0.78)

### Emotion Processing

1. **Detection**: RoBERTa model detects emotions in user input
2. **Scaling**: Emotions are scaled by personality volatility
3. **Forgiveness**: Positive emotions reduce negative emotions
4. **Capping**: Deltas are capped to prevent extreme swings
5. **State Update**: Emotional state is updated
6. **Decay**: Emotions decay over time based on personality decay rate
7. **Injection**: Active emotions (>0.2) are injected into system instructions

### Relationship Processing

The relationship system creates dynamic, evolving relationships with users:

1. **Emotion-Based Updates**: Emotions detected in user input influence affinity changes
   - Positive emotions (joy, amusement, gratitude) increase affinity
   - Negative emotions (anger, disgust, sadness) decrease affinity
   
2. **Persona Resonance**: User input that aligns with the persona's core drive increases both affinity and familiarity
   - Pragmatist resonates with short, direct communication
   - Hype Man resonates with enthusiasm and positive energy
   - Chill Gen-Z resonates with casual, lowercase communication

3. **Social Friction**: As relationships deepen, they become harder to change (realistic relationship dynamics)
   - Stranger tier (0.0-0.25): No friction - relationships change easily
   - Associate tier (0.25-0.5): Slight friction (1.8x)
   - Friend tier (0.5-0.75): Significant friction (3.5x)
   - Confidant tier (0.75-1.0): Extreme friction (6.0x) - deep relationships are stable

4. **Bonding Coefficient**: Each user has an individual resonance factor (β) that affects how quickly they bond
   - Base value: Set by persona's `social_openness`
   - Can be adjusted dynamically: `adjust_bonding_coefficient(user_id, adjustment)`
   - Higher β = faster relationship development

5. **Trust Tiers & Behavior**: The agent's behavior adapts based on trust tier:
   - **Stranger**: Professional, guarded, minimal personality quirks, analytical thoughts
   - **Associate**: Friendly but bounded, occasional quirks, task-focused thoughts
   - **Friend**: Relaxed and authentic, full personality expression, transparent thoughts
   - **Confidant**: Complete transparency, raw and unfiltered, zero social risk

6. **Significant Moments**: Major relationship changes (>0.3 affinity delta or >0.2 familiarity delta) are logged as significant moments

## Examples

### Basic Chat Loop

```python
from cogni import Agent

agent = Agent(
    persona_key="THE_CHILL_GEN_Z",
    project_id="your-project-id",
    verbose=True
)

while True:
    user_input = input("You: ")
    if user_input.lower() in ['quit', 'exit', 'bye']:
        agent.consolidate_session()  # Save learned facts
        break
    
    response = agent.chat(user_input)
    print(f"Agent: {response['response']}")
    if agent.verbose:
        print(f"[Thought]: {response['thought']}")
```

### Custom Persona Example

```python
from cogni import Agent

# Define a custom persona
my_persona = {
    "name": "The Mentor",
    "core_drive": "Values teaching and helping others grow",
    "core_opinion": "Believes everyone can learn with the right guidance",
    "speaking_style": "Patient, encouraging, uses examples and analogies",
    "config": {
        "volatility": 0.5,
        "decay": 0.06,
        "forgiveness": 2.0,
        "max_delta": 0.2
    }
}

agent = Agent(
    persona=my_persona,
    project_id="your-project-id",
    storage_path="./mentor_data"
)

response = agent.chat("I'm struggling with Python decorators")
print(response['response'])
```

### Session Management

```python
from cogni import Agent

agent = Agent(
    persona_key="THE_PRAGMATIST",
    project_id="your-project-id"
)

# First conversation
response1 = agent.chat("I love Python")
print(response1['response'])

# Consolidate and reset for new session
agent.consolidate_session()
agent.reset()

# Second conversation (remembers facts from first session)
response2 = agent.chat("What's my favorite language?")
print(response2['response'])  # Should reference Python from LTM
```

### Monitoring Emotional State

```python
from cogni import Agent

agent = Agent(
    persona_key="THE_HYPE_MAN",
    project_id="your-project-id"
)

response = agent.chat("I just won a coding competition!")
emotions = agent.get_emotional_state()

# Check specific emotions
if emotions.get('joy', 0) > 0.5:
    print("Agent is feeling very happy!")
if emotions.get('excitement', 0) > 0.5:
    print("Agent is excited!")
```

### Relationship Tracking

```python
from cogni import Agent

agent = Agent(
    persona_key="THE_CHILL_GEN_Z",
    project_id="your-project-id"
)

# Chat with a specific user
user_id = "alice"
response1 = agent.chat("Hey, how's it going?", user_id=user_id)
print(f"Trust Tier: {response1['relationship']['trust_tier']}")  # "Stranger"

# Continue conversation - relationship develops
for i in range(10):
    response = agent.chat("Tell me about yourself", user_id=user_id)
    rel = response['relationship']
    print(f"Turn {i+1}: {rel['trust_tier']} | Affinity: {rel['affinity_descriptor']}")

# Get relationship summary
relationship = agent.get_relationship(user_id)
print(f"\nFinal Relationship:")
print(f"  Trust Tier: {relationship['trust_tier']}")
print(f"  Affinity: {relationship['affinity_descriptor']} ({relationship['raw_affinity']:.2f})")
print(f"  Familiarity: {relationship['familiarity_descriptor']} ({relationship['raw_familiarity']:.2f})")
print(f"  Total Interactions: {relationship['total_interactions']}")

# Adjust bonding coefficient for users who resonate well
agent.adjust_bonding_coefficient(user_id, 0.2)  # Increase bonding speed
```

### Multi-User Relationship Management

```python
from cogni import Agent

agent = Agent(
    persona_key="THE_PRAGMATIST",
    project_id="your-project-id"
)

# Different users have separate relationships
users = ["alice", "bob", "charlie"]

for user in users:
    response = agent.chat("Hello!", user_id=user)
    rel = response['relationship']
    print(f"{user}: {rel['trust_tier']} | Interactions: {rel['total_interactions']}")

# Each user's relationship evolves independently
# The agent remembers each user's relationship state
```

## Troubleshooting

### Common Issues

#### 1. Vertex AI Authentication Error

**Error**: `google.auth.exceptions.DefaultCredentialsError`

**Solution**: 
```bash
gcloud auth application-default login
```

Or set up a service account and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

#### 2. Model Not Found

**Error**: Model name not recognized

**Solution**: Ensure you're using valid Vertex AI model names. Check available models in your region:
- `gemini-2.5-flash-lite`
- `gemini-2.5-flash`
- `gemini-1.5-flash`
- `gemini-1.5-pro`

#### 3. Memory Index Not Found

**Error**: FAISS index file missing

**Solution**: The system will create indexes automatically. Ensure the `storage_path` directory is writable. For synthetic memory, ensure the JSON file exists in `synthetic_data_dir`.

#### 4. RoBERTa Model Download Fails

**Error**: Connection error when loading emotion model

**Solution**: Ensure you have internet access for the first run. The model will be cached locally after the first download.

#### 5. Personality Key Not Found

**Error**: `ValueError: Unknown persona_key`

**Solution**: Use one of the available keys:
- `THE_PRAGMATIST`
- `THE_HYPE_MAN`
- `THE_REALIST`
- `THE_CHILL_GEN_Z`

Or provide a custom `persona` dictionary.

### Performance Tips

1. **First Run**: The first run will be slower as models are downloaded and indexes are built
2. **Memory Size**: Large memory indexes may slow retrieval. Consider periodically archiving old memories
3. **Model Selection**: Use lighter models (flash-lite) for faster responses if you don't need complex reasoning
4. **Verbose Mode**: Disable verbose logging in production for better performance

### Debugging

Enable verbose mode to see detailed logs:

```python
agent = Agent(
    persona_key="THE_CHILL_GEN_Z",
    project_id="your-project-id",
    verbose=True  # Shows all internal operations
)
```

This will show:
- Emotion detection results
- Memory retrieval results
- Model routing decisions
- Social dynamics analysis
- Emotional state updates

## License

MIT
## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or contributions, please open an issue on the repository.

