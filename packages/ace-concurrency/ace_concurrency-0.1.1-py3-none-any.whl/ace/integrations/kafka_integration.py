import asyncio
import time
from typing import Optional, Callable, Any, List
from dataclasses import dataclass
from ace.core.limiters import ACESemaphore
from ace.core.control import ACEController, AIMDConfig
from ace.core.signals import SignalCollector
from ace.core.logger import ACELogger


@dataclass
class KafkaMessage:
    """Simple message container"""
    topic: str
    partition: int
    offset: int
    key: Optional[str]
    value: Any


class MockKafkaConsumer:
    """Mock Kafka consumer for demonstration (replace with real kafka-python in production)"""
    
    def __init__(self, topics: List[str], group_id: str):
        self.topics = topics
        self.group_id = group_id
        self._paused = False
        self._message_counter = 0
    
    def poll(self, timeout_ms: int = 1000) -> List[KafkaMessage]:
        if self._paused:
            time.sleep(timeout_ms / 1000.0)
            return []
        
        messages = []
        for i in range(3):
            self._message_counter += 1
            messages.append(KafkaMessage(
                topic=self.topics[0],
                partition=0,
                offset=self._message_counter,
                key=f"key-{self._message_counter}",
                value=f"message-{self._message_counter}"
            ))
        
        time.sleep(timeout_ms / 1000.0)
        return messages
    
    def pause(self):
        self._paused = True
    
    def resume(self):
        self._paused = False
    
    def commit(self):
        pass
    
    def close(self):
        pass
    
    def get_lag(self) -> int:
        import random
        return random.randint(0, 100)


class ACEKafkaConsumerManager:
    """Manages Kafka consumer with adaptive concurrency and pause/resume"""
    
    def __init__(
        self,
        topics: List[str],
        group_id: str,
        message_handler: Callable[[KafkaMessage], Any],  # Your async function to process messages
        config: AIMDConfig,
        logger: Optional[ACELogger] = None,
        signal_collector: Optional[SignalCollector] = None,
        use_mock: bool = True  # Set False for real Kafka (requires kafka-python)
    ):
        self.topics = topics
        self.group_id = group_id
        self.message_handler = message_handler
        self.config = config
        self.logger = logger or ACELogger()
        self.signal_collector = signal_collector or SignalCollector()  # Monitors system health
        self.controller = ACEController(config, self.logger)  # AIMD decision engine
        
        if use_mock:
            self.consumer = MockKafkaConsumer(topics, group_id)  # Demo consumer
        else:
            raise NotImplementedError("Real Kafka consumer not implemented in this demo")
        
        self.semaphore = ACESemaphore(initial_limit=config.initial_limit, logger=self.logger)  # Controls message processing concurrency
        self._running = False
        self._consumer_task: Optional[asyncio.Task] = None  # Polls and processes messages
        self._control_task: Optional[asyncio.Task] = None  # AIMD control loop
        self._paused = False  # Pause consumer when overloaded
    
    async def _control_loop(self):
        """Runs every ~2s: monitor system + Kafka lag → adjust concurrency → pause/resume consumer"""
        self.logger.log_info("ACE Kafka consumer control loop started", {
            "topics": self.topics,
            "group_id": self.group_id,
            "initial_limit": self.config.initial_limit
        })
        
        while self._running:
            try:
                signals = await self.signal_collector.collect_all_async()  # Get system health
                lag = await asyncio.get_event_loop().run_in_executor(None, self.consumer.get_lag)  # Get consumer lag
                self.signal_collector.update_kafka_lag(lag)
                signals.kafka_lag = lag
                
                stats = self.semaphore.get_stats()
                new_limit = self.controller.adjust_limit(stats["limit"], stats["active"], signals)  # AIMD decision
                
                if new_limit != stats["limit"]:
                    await self.semaphore.set_limit(new_limit)  # Adjust message processing concurrency
                
                # Pause consumer if system near breaking point (95% CPU or too many waiting)
                should_pause = (
                    signals.cpu_percent > self.config.cpu_threshold * 0.95 or
                    stats["waiting"] > stats["limit"] * 2
                )
                
                if should_pause and not self._paused:
                    await asyncio.get_event_loop().run_in_executor(None, self.consumer.pause)
                    self._paused = True
                    self.logger.log_info("Kafka consumer paused", {
                        "reason": "System overloaded",
                        "cpu_percent": signals.cpu_percent,
                        "waiting_tasks": stats["waiting"]
                    })
                elif not should_pause and self._paused:
                    await asyncio.get_event_loop().run_in_executor(None, self.consumer.resume)
                    self._paused = False
                    self.logger.log_info("Kafka consumer resumed")
                
                await asyncio.sleep(self.config.adjustment_interval_seconds)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.log_error("kafka_control_loop_error", str(e))
                await asyncio.sleep(1)
    
    async def _consume_loop(self):
        self.logger.log_info("Kafka consumer loop started")
        
        while self._running:
            try:
                messages = await asyncio.get_event_loop().run_in_executor(None, self.consumer.poll, 1000)
                
                if messages:
                    tasks = [self._process_message(msg) for msg in messages]
                    await asyncio.gather(*tasks, return_exceptions=True)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.log_error("kafka_consume_loop_error", str(e))
                await asyncio.sleep(1)
    
    async def _process_message(self, message: KafkaMessage):
        """Process one message - waits if concurrency limit reached"""
        async with self.semaphore.acquire():  # Block if limit reached (backpressure)
            try:
                await self.message_handler(message)  # Call user's handler
            except Exception as e:
                self.logger.log_error("message_processing_error", str(e), {
                    "topic": message.topic,
                    "partition": message.partition,
                    "offset": message.offset
                })
    
    async def start(self):
        self._running = True
        self._consumer_task = asyncio.create_task(self._consume_loop())
        self._control_task = asyncio.create_task(self._control_loop())
    
    async def stop(self):
        self._running = False
        
        if self._consumer_task:
            self._consumer_task.cancel()
            try:
                await self._consumer_task
            except asyncio.CancelledError:
                pass
        
        if self._control_task:
            self._control_task.cancel()
            try:
                await self._control_task
            except asyncio.CancelledError:
                pass
        
        await asyncio.get_event_loop().run_in_executor(None, self.consumer.close)
    
    def get_stats(self) -> dict:
        return self.semaphore.get_stats()
