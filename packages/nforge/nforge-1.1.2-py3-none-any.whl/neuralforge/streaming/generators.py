"""
Async Generator Utilities for NeuralForge Streaming.

Provides utilities for working with async generators
in streaming contexts.
"""

import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Optional, TypeVar, Union

logger = logging.getLogger(__name__)

T = TypeVar('T')


async def async_generator_wrapper(
    sync_generator: Any,
    chunk_delay: float = 0.0
) -> AsyncIterator[Any]:
    """
    Wrap a synchronous generator as an async generator.
    
    Args:
        sync_generator: Synchronous generator or iterable
        chunk_delay: Optional delay between chunks (seconds)
    
    Yields:
        Items from the generator
    
    Example:
        ```python
        def sync_gen():
            for i in range(10):
                yield i
        
        async for item in async_generator_wrapper(sync_gen()):
            print(item)
        ```
    """
    loop = asyncio.get_event_loop()
    
    # Convert to iterator if needed
    if hasattr(sync_generator, '__iter__'):
        iterator = iter(sync_generator)
    else:
        iterator = sync_generator
    
    while True:
        try:
            # Run next() in executor to avoid blocking
            item = await loop.run_in_executor(None, next, iterator)
            yield item
            
            if chunk_delay > 0:
                await asyncio.sleep(chunk_delay)
        except StopIteration:
            break


async def chunk_generator(
    data: Union[str, bytes, list],
    chunk_size: int = 100
) -> AsyncIterator[Union[str, bytes, list]]:
    """
    Split data into chunks for streaming.
    
    Args:
        data: Data to chunk (string, bytes, or list)
        chunk_size: Size of each chunk
    
    Yields:
        Chunks of the data
    
    Example:
        ```python
        text = "Hello, this is a long text to stream..."
        async for chunk in chunk_generator(text, chunk_size=10):
            await send(chunk)
        ```
    """
    if isinstance(data, (str, bytes)):
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]
            await asyncio.sleep(0)  # Yield control
    elif isinstance(data, list):
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]
            await asyncio.sleep(0)
    else:
        yield data


async def timeout_generator(
    generator: AsyncIterator[T],
    timeout: float,
    default: Optional[T] = None
) -> AsyncIterator[T]:
    """
    Wrap a generator with per-item timeout.
    
    Args:
        generator: Async generator to wrap
        timeout: Timeout in seconds for each item
        default: Default value to yield on timeout (None to skip)
    
    Yields:
        Items from generator or default on timeout
    
    Example:
        ```python
        async def slow_gen():
            await asyncio.sleep(5)  # Slow item
            yield "item"
        
        # Will timeout after 1 second
        async for item in timeout_generator(slow_gen(), timeout=1.0):
            print(item)
        ```
    """
    try:
        async for item in generator:
            try:
                # Wrap yield in timeout
                yield item
            except asyncio.TimeoutError:
                if default is not None:
                    yield default
                logger.warning(f"Generator item timed out after {timeout}s")
    except asyncio.TimeoutError:
        logger.warning(f"Generator timed out after {timeout}s")


async def rate_limited_generator(
    generator: AsyncIterator[T],
    rate: float
) -> AsyncIterator[T]:
    """
    Rate limit a generator.
    
    Args:
        generator: Async generator to rate limit
        rate: Maximum items per second
    
    Yields:
        Items from generator at limited rate
    
    Example:
        ```python
        # Limit to 10 items per second
        async for item in rate_limited_generator(fast_gen(), rate=10):
            print(item)
        ```
    """
    interval = 1.0 / rate if rate > 0 else 0
    last_yield = 0.0
    
    async for item in generator:
        now = asyncio.get_event_loop().time()
        elapsed = now - last_yield
        
        if elapsed < interval:
            await asyncio.sleep(interval - elapsed)
        
        yield item
        last_yield = asyncio.get_event_loop().time()


async def buffered_generator(
    generator: AsyncIterator[T],
    buffer_size: int = 10
) -> AsyncIterator[T]:
    """
    Buffer items from a generator.
    
    Useful for slow consumers with fast producers.
    
    Args:
        generator: Async generator to buffer
        buffer_size: Maximum buffer size
    
    Yields:
        Items from buffer
    """
    buffer: asyncio.Queue = asyncio.Queue(maxsize=buffer_size)
    done = asyncio.Event()
    
    async def producer():
        try:
            async for item in generator:
                await buffer.put(item)
        finally:
            done.set()
    
    # Start producer task
    producer_task = asyncio.create_task(producer())
    
    try:
        while not (done.is_set() and buffer.empty()):
            try:
                item = await asyncio.wait_for(buffer.get(), timeout=0.1)
                yield item
            except asyncio.TimeoutError:
                continue
    finally:
        producer_task.cancel()
        try:
            await producer_task
        except asyncio.CancelledError:
            pass


async def merge_generators(
    *generators: AsyncIterator[T],
    ordered: bool = False
) -> AsyncIterator[T]:
    """
    Merge multiple async generators into one.
    
    Args:
        *generators: Async generators to merge
        ordered: If True, yield items in order; if False, yield as available
    
    Yields:
        Items from all generators
    
    Example:
        ```python
        async def gen1():
            yield "a"
            yield "b"
        
        async def gen2():
            yield 1
            yield 2
        
        async for item in merge_generators(gen1(), gen2()):
            print(item)  # Prints: a, b, 1, 2 (or interleaved if ordered=False)
        ```
    """
    if ordered:
        # Yield from each generator in order
        for gen in generators:
            async for item in gen:
                yield item
    else:
        # Yield items as they become available
        pending = set()
        gen_map = {}
        
        for i, gen in enumerate(generators):
            task = asyncio.create_task(gen.__anext__())
            pending.add(task)
            gen_map[task] = (i, gen)
        
        while pending:
            done, pending = await asyncio.wait(
                pending,
                return_when=asyncio.FIRST_COMPLETED
            )
            
            for task in done:
                try:
                    result = task.result()
                    yield result
                    
                    # Schedule next item from this generator
                    _, gen = gen_map.pop(task)
                    new_task = asyncio.create_task(gen.__anext__())
                    pending.add(new_task)
                    gen_map[new_task] = (_, gen)
                except StopAsyncIteration:
                    gen_map.pop(task, None)


async def filter_generator(
    generator: AsyncIterator[T],
    predicate: Callable[[T], bool]
) -> AsyncIterator[T]:
    """
    Filter items from a generator.
    
    Args:
        generator: Async generator to filter
        predicate: Function returning True for items to keep
    
    Yields:
        Items passing the predicate
    """
    async for item in generator:
        if predicate(item):
            yield item


async def map_generator(
    generator: AsyncIterator[T],
    transform: Callable[[T], Any]
) -> AsyncIterator[Any]:
    """
    Transform items from a generator.
    
    Args:
        generator: Async generator to transform
        transform: Function to apply to each item
    
    Yields:
        Transformed items
    """
    async for item in generator:
        if asyncio.iscoroutinefunction(transform):
            yield await transform(item)
        else:
            yield transform(item)


async def take_generator(
    generator: AsyncIterator[T],
    count: int
) -> AsyncIterator[T]:
    """
    Take only the first N items from a generator.
    
    Args:
        generator: Async generator
        count: Maximum number of items to yield
    
    Yields:
        Up to count items
    """
    taken = 0
    async for item in generator:
        if taken >= count:
            break
        yield item
        taken += 1


async def skip_generator(
    generator: AsyncIterator[T],
    count: int
) -> AsyncIterator[T]:
    """
    Skip the first N items from a generator.
    
    Args:
        generator: Async generator
        count: Number of items to skip
    
    Yields:
        Items after skipping
    """
    skipped = 0
    async for item in generator:
        if skipped < count:
            skipped += 1
            continue
        yield item
