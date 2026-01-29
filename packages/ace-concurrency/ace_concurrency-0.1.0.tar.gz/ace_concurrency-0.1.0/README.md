# ACE: Adaptive Concurrency Engine

**Automatic concurrency management for Python applications using AIMD algorithm.**

ACE dynamically adjusts concurrency limits based on system health signals (CPU, memory, queue depth, event loop lag), ensuring optimal performance without overload.

## Key Features

- **AIMD Algorithm**: Proven congestion control mechanism from TCP
- **Multi-Signal Monitoring**: CPU, memory, queues, event loop lag, Kafka lag
- **Backpressure Support**: Tasks wait gracefully when limits reached
- **Structured Logging**: JSON-formatted decision logs for observability
- **Three Integrations**: Asyncio, thread pools, Kafka consumers
- **Safety-First**: Fail-open defaults, hard boundaries, cooldown periods

## Installation

```bash
pip install ace-concurrency
```

## Architecture

![ACE Architecture](docs/architecture.png)

```
ACE Application Layer
┌─────────────────────────────────────────────────────────────┐
│  AsyncIO Manager  │  ThreadPool Manager  │  Kafka Manager   │
├─────────────────────────────────────────────────────────────┤
│              ACE Controller (AIMD Logic)                     │
├─────────────────────────────────────────────────────────────┤
│  ACE Semaphore     │  Queue Management   │  Backpressure    │
├─────────────────────────────────────────────────────────────┤
│              Signal Collector (System Health)                │
│         CPU%, Memory%, Queue Depth, Event Loop Lag           │
└─────────────────────────────────────────────────────────────┘

Control Loop (~2s interval):
1. Collect Signals    → CPU, Memory, Queue Depth, Lag
2. Check Thresholds   → CPU > 80%? Memory > 85%?
3. AIMD Decision      → Increase (healthy) or Decrease (stressed)
4. Apply New Limit    → Update semaphore/pool limit
5. Log Decision       → Structured JSON with full context

Task Lifecycle:
Task Submitted → Try Acquire Slot → Slot Available? → Execute
                         ↓
                    No Slot (Wait)
                         ↓
                    Backpressure Applied
```

## Quick Start

```python
import asyncio
from ace.core.control import AIMDConfig
from ace.integrations.asyncio_integration import ACEAsyncioManager

async def work(item):
    pass  # Your async work

async def main():
    config = AIMDConfig(min_limit=5, max_limit=50, initial_limit=10)
    async with ACEAsyncioManager(config) as manager:
        tasks = [manager.submit(work, i) for i in range(100)]
        results = await asyncio.gather(*tasks)

asyncio.run(main())
```

## Configuration

```python
AIMDConfig(
    # Concurrency bounds
    min_limit=5,                  # Minimum concurrency
    max_limit=200,                # Maximum concurrency
    initial_limit=20,             # Starting limit
    increase_step=2,              # Add per cycle
    decrease_factor=0.5,          # Multiply when stressed

    # Thresholds for DECREASE
    cpu_threshold=80.0,           # Decrease if CPU > 80%
    memory_threshold=85.0,        # Decrease if memory > 85%
    queue_threshold=100,          # Decrease if queue > 100
    event_loop_lag_threshold_ms=50.0,  # Decrease if lag > 50ms

    # Thresholds for INCREASE
    cpu_increase_threshold=40.0,       # Aggressive increase if CPU < 40%
    memory_increase_threshold=50.0,    # Aggressive increase if memory < 50%

    # Control loop
    cooldown_seconds=5.0,         # Min time between adjustments
    adjustment_interval_seconds=2.0,  # How often to check
)
```

**Decision Logic:**

- **Decrease**: CPU > 80% OR memory > 85% OR queue > 100 OR lag > 50ms
- **Increase (normal)**: High utilization (>80%) + system healthy
- **Increase (aggressive)**: Resources available (CPU < 40% AND memory < 50%)
- **Hold**: Moderate utilization + system healthy

## Integrations

**Asyncio Tasks** — Manage concurrent async operations:

```python
from ace.integrations.asyncio_integration import ACEAsyncioManager
async with ACEAsyncioManager(config) as manager:
    result = await manager.submit(async_func, *args)
```

**Thread Pool** — Manage CPU-bound work:

```python
from ace.integrations.threadpool_integration import ACEThreadPoolManager
with ACEThreadPoolManager(config) as manager:
    future = manager.submit(cpu_func, *args)
```

**Kafka Consumer** — Adaptive message processing with pause/resume:

```python
from ace.integrations.kafka_integration import ACEKafkaConsumerManager
manager = ACEKafkaConsumerManager(
    topics=["events"],
    group_id="group",
    message_handler=handler,
    config=config
)
await manager.start()
```

## How It Works

**Control Loop (~2s interval):**

1. Collect system signals (CPU, memory, queues)
2. Check thresholds (stressed or healthy)
3. Apply AIMD: increase if healthy, decrease if stressed
4. Apply new limit to semaphore
5. Log decision with full context

**Task Lifecycle:**

1. Task submitted to manager
2. Attempts to acquire semaphore slot
3. If full → waits (backpressure)
4. If available → executes immediately
5. Releases slot on completion
6. Next waiting task proceeds

## Logging

All decisions logged as JSON for observability:

```json
{
  "timestamp": "2026-01-16T12:34:56",
  "event_type": "limit_adjustment",
  "concurrency": {
    "current_limit": 10,
    "new_limit": 12,
    "active_tasks": 9
  },
  "signals": { "cpu_percent": 45.2, "memory_percent": 62.1 },
  "decision": "increase",
  "reason": "System healthy and high utilization"
}
```

## Performance

- Signal collection: ~10-20ms per cycle
- Limit adjustment: ~1ms
- Semaphore overhead: ~0.1ms (similar to stdlib)

Benefits far exceed cost: prevents overload, improves stability, enables higher throughput.

## License

MIT License — See [LICENSE](LICENSE) file

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
