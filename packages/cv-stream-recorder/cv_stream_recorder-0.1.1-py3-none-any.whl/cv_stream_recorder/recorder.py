import asyncio
import ffmpeg
import logging
import os
import time

from concurrent.futures import ThreadPoolExecutor
from .config import settings
from .helpers import check_url, check_folder_path, stop_process
from .utils.logging_config import setup_logging


# Set up logging configuration
logger = logging.getLogger(__name__)
setup_logging()


def stop_recording(pid: int) -> bool:
    """Stop the recording process with the given PID."""
    logger.info(f"stop_recording: Stopping process with PID {pid}")
    return stop_process(pid)


async def record_stream(url: str, folder_path: str, callback: callable = None):
    """Record a stream from URL into consecutive chunks and block until finished."""

    # Check the URL
    if not check_url(url):
        raise ValueError(f"Invalid URL: {url}")

    # Check the folder path
    if not check_folder_path(folder_path):
        raise ValueError(f"Invalid folder path: {folder_path}")

    # Start recording
    pid, task = await start_recording(url, folder_path, callback)
    
    # Wait for the recording task to finish
    await task
    return pid


async def start_recording(url: str, folder_path: str, callback: callable = None, segment_length: int = None, max_duration: int = None):
    """Start recording a stream from URL."""
    logger.info(f"record_stream: Recording stream from {url} into {folder_path}")

    # Use provided values or fall back to settings
    s_length = segment_length if segment_length is not None else settings.SEGMENT_LENGTH
    m_duration = max_duration if max_duration is not None else settings.MAX_DURATION
    logger.info(f"record_stream: Using segment length {s_length} (seconds)")

    filename_pattern = "chunk_%03d.mp4"
    filepath_pattern = os.path.join(folder_path, filename_pattern)

    logger.info(f"record_stream: Starting ffmpeg process")
    process = (
        ffmpeg
        .input(url)
        .output(
            filepath_pattern,
            codec="copy",
            f="segment",
            segment_time=s_length,
            reset_timestamps=1,
            max_duration=m_duration
        )
        .run_async()
    )
    pid = process.pid
    logger.info(f"record_stream: Process started with PID {pid}")

    # Check process and notify in a non-blocking task
    task = asyncio.create_task(check_process_and_notify(process, folder_path, callback))

    # Return PID and the task handle
    return pid, task


async def check_process_and_notify(process, folder_path: str, callback: callable = None):
    notified_chunks = set()
    current_index = 0
    current_chunk_size = 0

    try:
        while process.poll() is None:
            # If the NEXT chunk exists, the current one is definitely finished
            next_chunk = os.path.join(folder_path, f"chunk_{current_index + 1:03d}.mp4")
            current_chunk = os.path.join(folder_path, f"chunk_{current_index:03d}.mp4")
            if os.path.exists(next_chunk):
                if current_chunk not in notified_chunks and os.path.exists(current_chunk):
                    logger.info(f"record_stream: Next chunk {current_index + 1} exists, current chunk {current_index} finished")
                    if callback:
                        logger.info(f"record_stream: Notifying callback for chunk {current_index}")
                        with ThreadPoolExecutor(max_workers=2) as executor:
                            executor.submit(callback, current_chunk)

                    notified_chunks.add(current_chunk)
                    current_index += 1
                    current_chunk_size = os.path.getsize(next_chunk)

            else:
                # If the NEXT chunk does not exist, check if the current chunk size is the same as the previous size
                if os.path.exists(current_chunk):
                    size1 = os.path.getsize(current_chunk)
                    if size1 > 0 and size1 == current_chunk_size:
                        # Check twice: wait a bit and check again to be sure it's not still growing
                        await asyncio.sleep(0.5)
                        size2 = os.path.getsize(current_chunk)
                        if size1 == size2:
                            logger.info(f"record_stream: Chunk size does not change, chunk {current_index} finished")
                            if callback:
                                logger.info(f"record_stream: Notifying callback for chunk {current_index}")
                                with ThreadPoolExecutor(max_workers=2) as executor:
                                    executor.submit(callback, current_chunk)

                            notified_chunks.add(current_chunk)
                            current_index += 1
                    else:
                        current_chunk_size = size1

            await asyncio.sleep(0.5)
    except Exception as e:
        logger.error(f"record_stream: Error in monitoring task: {e}")
    finally:
        process.wait()
        logger.info(f"record_stream: ffmpeg process {process.pid} finished")
        
        """
        # After process finishes, notify about any remaining chunks
        # Scans the directory for all chunks to ensure none were missed
        logger.info(f"record_stream: Process finished, scanning the directory to notify about remaining chunks")
        for file in sorted(os.listdir(folder_path)):
            if file.startswith("chunk_") and file.endswith(".mp4"):
                full_path = os.path.join(folder_path, file)
                if full_path not in notified_chunks:
                    logger.info(f"record_stream: Found chunk {full_path} not notified, notifying callback")
                    if callback:
                        with ThreadPoolExecutor(max_workers=2) as executor:
                            executor.submit(callback, full_path)

                    notified_chunks.add(full_path)
        """


