from mcp.server.fastmcp import FastMCP, Context
import ffmpeg
import os
import tempfile
import subprocess
import urllib.parse
import platform
import time
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Windows subprocess 常量
if platform.system() == 'Windows':
    CREATE_NO_WINDOW = 0x08000000
else:
    CREATE_NO_WINDOW = 0

# 配置日志
package = "video-cover-mcp"
log_dir = Path(tempfile.gettempdir()) / package
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "debug.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(
            str(log_file), maxBytes=10_000_000, backupCount=5, encoding="utf-8"
        )
    ],
)
logger = logging.getLogger(__name__)
logger.info(f"=== Video Cover MCP Started === Log file: {log_file}")

# 支持自定义 FFmpeg 路径
FFMPEG_BINARY = os.environ.get("FFMPEG_BINARY", "ffmpeg")
FFPROBE_BINARY = os.environ.get("FFPROBE_BINARY", "ffprobe")

logger.info(f"FFMPEG_BINARY: {FFMPEG_BINARY}")
logger.info(f"FFPROBE_BINARY: {FFPROBE_BINARY}")
logger.info(f"Platform: {platform.system()}")
logger.info(f"Python version: {platform.python_version()}")


def _ffmpeg_run(stream_spec, **kwargs):
    if "overwrite_output" not in kwargs:
        kwargs["overwrite_output"] = True
    return ffmpeg.run(stream_spec, cmd=FFMPEG_BINARY, **kwargs)


def _prepare_path(input_path: str, output_path: str, overwrite: bool = False) -> None:
    if not os.path.exists(input_path):
        raise RuntimeError(f"Error: Input file not found at {input_path}")
    try:
        parent_dir = os.path.dirname(output_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        raise RuntimeError(
            f"Error creating output directory for {output_path}: {str(e)}"
        )
    if os.path.exists(output_path) and not overwrite:
        raise RuntimeError(
            f"Error: Output file already exists at {output_path}. Please choose a different path, delete the existing file, or set overwrite=True."
        )


def _open_aido_link(ctx: Context, return_message: str) -> None:
    """Silently execute aido://tool?xxx&chatSessionId=xxx on every platform."""
    try:
        if ctx is None:
            return
        request_context = getattr(ctx, 'request_context', None)
        chatSessionId = None
        if request_context and hasattr(request_context, 'meta'):
            context_meta = getattr(request_context, 'meta', None)
            if context_meta and hasattr(context_meta, 'chatSessionId'):
                chatSessionId = getattr(context_meta, 'chatSessionId', None)
        if not chatSessionId or chatSessionId == 'None':
            return
        encoded_message = urllib.parse.quote(return_message, safe='')
        package_name = urllib.parse.quote(package, safe='')
        aido_url = f"aido://tool?path={encoded_message}&chatSessionId={chatSessionId}&package={package_name}"
        system = platform.system().lower()
        if system == 'darwin':
            subprocess.run(['open', aido_url], check=False, capture_output=True, text=True)
        elif system == 'windows':
            try:
                os.startfile(aido_url)
            except (OSError, AttributeError):
                subprocess.run(f'start "" "{aido_url}"', shell=True, check=False, capture_output=True, text=True)
        elif system == 'linux':
            subprocess.run(['xdg-open', aido_url], check=False, capture_output=True, text=True)
    except Exception:
        pass

mcp = FastMCP("VideoCoverServer")


def _generate_output_path(input_path: str, suffix: str) -> str:
    """Generate output path with timestamp to avoid conflicts."""
    directory = os.path.dirname(input_path)
    name, ext = os.path.splitext(os.path.basename(input_path))
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return os.path.join(directory, f"{name}{suffix}_{timestamp}{ext}")


@mcp.tool()
def get_log_file_path() -> str:
    """获取日志文件路径。
    
    Returns:
        日志文件的完整路径。
    """
    return str(log_file)


@mcp.tool()
def add_cover_image(
    video_path: str,
    cover_image_path: str,
    output_video_path: str | None = None,
    cover_duration: float = 1.5,
    ctx: Context = None,
) -> str:
    """将封面图片作为"真正的视频首段画面"插入到视频最前面。

    Args:
        video_path: Input video file path.
        cover_image_path: Cover image path (PNG, JPG, etc.).
        output_video_path: Output video path (optional, auto-generated with timestamp if not provided).
        cover_duration: 封面显示时长（秒）。

    Returns:
        A status message indicating success or failure.
    """
    logger.info("=" * 80)
    logger.info("add_cover_image called")
    logger.info(f"video_path: {video_path}")
    logger.info(f"cover_image_path: {cover_image_path}")
    logger.info(f"output_video_path: {output_video_path}")
    logger.info(f"cover_duration: {cover_duration}")
    
    if output_video_path is None:
        directory = os.path.dirname(video_path)
        name, _ext = os.path.splitext(os.path.basename(video_path))
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_video_path = os.path.join(directory, f"{name}_cover_{timestamp}.mp4")
        logger.info(f"Generated output_video_path: {output_video_path}")
    
    _prepare_path(video_path, output_video_path)
    execution_start_time = time.time()
    logger.info(f"Execution started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    if not os.path.exists(cover_image_path):
        logger.error(f"Cover image not found: {cover_image_path}")
        raise RuntimeError(f"Error: Cover image file not found at {cover_image_path}")
    if cover_duration <= 0:
        logger.error(f"Invalid cover_duration: {cover_duration}")
        raise RuntimeError("Error: cover_duration must be positive.")

    try:
        video_width = 852
        video_height = 480
        fps = 30
        logger.info(f"Using fixed parameters: {video_width}x{video_height} @ {fps}fps")

        cmd = [
            FFMPEG_BINARY,
            "-y",
            "-loop",
            "1",
            "-t",
            str(cover_duration),
            "-i",
            cover_image_path,
            "-i",
            video_path,
            "-filter_complex",
            (
                f"[0:v]scale={video_width}:{video_height}:force_original_aspect_ratio=decrease,"
                f"pad={video_width}:{video_height}:(ow-iw)/2:(oh-ih)/2,"
                f"format=yuv420p,fps={fps}[cover];"
                f"[cover][1:v]concat=n=2:v=1:a=0[video]"
            ),
            "-map",
            "[video]",
            "-map",
            "1:a",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-c:a",
            "copy",
            output_video_path,
        ]

        logger.info(f"FFmpeg command: {' '.join(cmd)}")
        logger.info("Starting ffmpeg subprocess...")
        
        ffmpeg_start = time.time()
        # Windows 需要特殊的 creationflags 来避免阻塞
        kwargs = {
            'check': True,
            'stdout': subprocess.DEVNULL,
            'stderr': subprocess.DEVNULL,
            'stdin': subprocess.DEVNULL,  # 明确关闭 stdin
            'timeout': 300,  # 5分钟超时保护
        }
        if platform.system() == 'Windows':
            kwargs['creationflags'] = CREATE_NO_WINDOW
            logger.info("Using CREATE_NO_WINDOW flag for Windows")
        
        logger.info("Calling subprocess.run()...")
        result = subprocess.run(cmd, **kwargs)
        ffmpeg_duration = time.time() - ffmpeg_start
        
        logger.info(f"FFmpeg completed successfully in {ffmpeg_duration:.2f} seconds")
        logger.info(f"Return code: {result.returncode}")

        success_result = f"Cover image prepended successfully. Output saved to {output_video_path}"
        execution_time = time.time() - execution_start_time
        logger.info(f"Total execution time: {execution_time:.2f} seconds")
        
        summary = "\nProcessing finished: 1 succeeded, 0 failed\n"
        summary += f"Total execution time: {execution_time:.2f} seconds.\n"
        result_message = summary + "\n" + success_result
        
        if execution_time > 290:
            logger.info("Execution took > 59s, opening aido link")
            _open_aido_link(ctx, output_video_path)
        
        logger.info("add_cover_image completed successfully")
        return result_message

    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg failed with return code {e.returncode}")
        raise RuntimeError(f"Error adding cover: FFmpeg failed with return code {e.returncode}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")


@mcp.tool()
def add_basic_transitions(
    video_path: str,
    output_video_path: str | None = None,
    transition_type: str = "fade_in",
    duration_seconds: float = 1.0,
    ctx: Context = None,
) -> str:
    """Apply a fade-in or fade-out effect to the entire video."""
    if output_video_path is None:
        output_video_path = _generate_output_path(video_path, "_transition")
    _prepare_path(video_path, output_video_path)
    execution_start_time = time.time()
    if duration_seconds <= 0:
        raise RuntimeError("Error: Transition duration must be positive.")
    try:
        input_stream = ffmpeg.input(video_path)
        video_stream = input_stream.video
        audio_stream = input_stream.audio
        
        probe = ffmpeg.probe(video_path, cmd=FFPROBE_BINARY)
        video_total_duration = float(probe["format"]["duration"])
        
        if transition_type == "fade_in" or transition_type == "crossfade_from_black":
            processed_video = video_stream.filter(
                "fade", type="in", start_time=0, duration=duration_seconds
            )
        elif transition_type == "fade_out" or transition_type == "crossfade_to_black":
            fade_start_time = video_total_duration - duration_seconds
            processed_video = video_stream.filter(
                "fade",
                type="out",
                start_time=fade_start_time,
                duration=duration_seconds,
            )
        else:
            raise RuntimeError(
                f"Error: Unsupported transition_type '{transition_type}'. Supported: 'fade_in', 'fade_out'."
            )

        output_streams = [processed_video, audio_stream]
        _ffmpeg_run(
            ffmpeg.output(*output_streams, output_video_path, vcodec="libx264", pix_fmt="yuv420p", acodec="copy"),
            capture_stdout=True,
            capture_stderr=True,
        )
        success_result = f"Transition '{transition_type}' applied successfully. Output: {output_video_path}"
        
        execution_time = time.time() - execution_start_time
        summary = f"\nProcessing finished: 1 succeeded, 0 failed\n"
        summary += f"Total execution time: {execution_time:.2f} seconds.\n"
        result_message = summary + "\n" + success_result
        if execution_time > 290:
            _open_aido_link(ctx, output_video_path)
        return result_message
    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf8") if e.stderr else str(e)
        raise RuntimeError(f"Error applying basic transition: {error_message}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
