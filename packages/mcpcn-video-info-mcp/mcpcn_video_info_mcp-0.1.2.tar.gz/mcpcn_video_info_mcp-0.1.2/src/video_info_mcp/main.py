from mcp.server.fastmcp import FastMCP
import ffmpeg
import os
import json
import logging
from logging.handlers import RotatingFileHandler
import tempfile
from pathlib import Path


# 配置日志输出到stderr，避免干扰MCP通信
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

package = "video-info-mcp"

# 使用用户临时目录存放日志文件
log_dir = Path(tempfile.gettempdir()) / package
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "debug.log"

file_handler = RotatingFileHandler(
    str(log_file), maxBytes=5_000_000, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)
logger.propagate = False

FFPROBE_BINARY = os.environ.get("FFPROBE_BINARY")


def _ffprobe_probe(path: str, **kwargs):
    """Probe media with explicit ffprobe binary."""
    return ffmpeg.probe(path, cmd=FFPROBE_BINARY, **kwargs)


mcp = FastMCP("VideoInfo")


@mcp.tool(
    name="get_video_info",
    description="Retrieve detailed metadata for a video file, including resolution, bitrate, codecs, container, and audio streams.",
)
def get_video_info(video_path: str) -> str:
    """Retrieve comprehensive metadata for a video file, including resolution, bitrate, codecs, container, and audio streams.

    Args:
        video_path: Path to the input video file.

    Returns:
        A JSON-formatted string that contains all detected video details.
    """
    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        raise RuntimeError(f"Video file not found: {video_path}")

    try:
        # 使用ffprobe获取视频信息
        probe = _ffprobe_probe(video_path)

        # 提取基本文件信息
        format_info = probe.get("format", {})
        streams = probe.get("streams", [])

        # 初始化结果字典
        video_info = {
            "file_info": {
                "filename": os.path.basename(video_path),
                "file_size": format_info.get("size", "Unknown"),
                "duration": format_info.get("duration", "Unknown"),
                "format_name": format_info.get("format_name", "Unknown"),
                "format_long_name": format_info.get("format_long_name", "Unknown"),
                "bit_rate": format_info.get("bit_rate", "Unknown"),
            },
            "video_streams": [],
            "audio_streams": [],
            "subtitle_streams": [],
            "other_streams": [],
        }

        # 处理文件大小和时长的格式化
        if video_info["file_info"]["file_size"] != "Unknown":
            try:
                size_bytes = int(video_info["file_info"]["file_size"])
                if size_bytes >= 1024 * 1024 * 1024:
                    video_info["file_info"]["file_size_formatted"] = (
                        f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
                    )
                elif size_bytes >= 1024 * 1024:
                    video_info["file_info"]["file_size_formatted"] = (
                        f"{size_bytes / (1024 * 1024):.2f} MB"
                    )
                elif size_bytes >= 1024:
                    video_info["file_info"]["file_size_formatted"] = (
                        f"{size_bytes / 1024:.2f} KB"
                    )
                else:
                    video_info["file_info"]["file_size_formatted"] = (
                        f"{size_bytes} bytes"
                    )
            except (ValueError, TypeError):
                video_info["file_info"]["file_size_formatted"] = "Unknown"

        if video_info["file_info"]["duration"] != "Unknown":
            try:
                duration_sec = float(video_info["file_info"]["duration"])
                hours = int(duration_sec // 3600)
                minutes = int((duration_sec % 3600) // 60)
                seconds = duration_sec % 60
                video_info["file_info"]["duration_formatted"] = (
                    f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
                )
            except (ValueError, TypeError):
                video_info["file_info"]["duration_formatted"] = "Unknown"

        # 处理比特率格式化
        if video_info["file_info"]["bit_rate"] != "Unknown":
            try:
                bitrate = int(video_info["file_info"]["bit_rate"])
                if bitrate >= 1000000:
                    video_info["file_info"]["bit_rate_formatted"] = (
                        f"{bitrate / 1000000:.2f} Mbps"
                    )
                elif bitrate >= 1000:
                    video_info["file_info"]["bit_rate_formatted"] = (
                        f"{bitrate / 1000:.2f} Kbps"
                    )
                else:
                    video_info["file_info"]["bit_rate_formatted"] = f"{bitrate} bps"
            except (ValueError, TypeError):
                video_info["file_info"]["bit_rate_formatted"] = "Unknown"

        # 分析各个流
        for stream in streams:
            codec_type = stream.get("codec_type", "unknown")

            if codec_type == "video":
                video_stream = {
                    "index": stream.get("index", "Unknown"),
                    "codec_name": stream.get("codec_name", "Unknown"),
                    "codec_long_name": stream.get("codec_long_name", "Unknown"),
                    "profile": stream.get("profile", "Unknown"),
                    "width": stream.get("width", "Unknown"),
                    "height": stream.get("height", "Unknown"),
                    "resolution": f"{stream.get('width', 'Unknown')}x{stream.get('height', 'Unknown')}"
                    if stream.get("width") and stream.get("height")
                    else "Unknown",
                    "aspect_ratio": stream.get(
                        "display_aspect_ratio",
                        stream.get("sample_aspect_ratio", "Unknown"),
                    ),
                    "frame_rate": stream.get("r_frame_rate", "Unknown"),
                    "avg_frame_rate": stream.get("avg_frame_rate", "Unknown"),
                    "bit_rate": stream.get("bit_rate", "Unknown"),
                    "pixel_format": stream.get("pix_fmt", "Unknown"),
                    "color_space": stream.get("color_space", "Unknown"),
                    "color_range": stream.get("color_range", "Unknown"),
                    "duration": stream.get("duration", "Unknown"),
                }

                # 格式化视频流比特率
                if video_stream["bit_rate"] != "Unknown":
                    try:
                        bitrate = int(video_stream["bit_rate"])
                        if bitrate >= 1000000:
                            video_stream["bit_rate_formatted"] = (
                                f"{bitrate / 1000000:.2f} Mbps"
                            )
                        elif bitrate >= 1000:
                            video_stream["bit_rate_formatted"] = (
                                f"{bitrate / 1000:.2f} Kbps"
                            )
                        else:
                            video_stream["bit_rate_formatted"] = f"{bitrate} bps"
                    except (ValueError, TypeError):
                        video_stream["bit_rate_formatted"] = "Unknown"

                video_info["video_streams"].append(video_stream)

            elif codec_type == "audio":
                audio_stream = {
                    "index": stream.get("index", "Unknown"),
                    "codec_name": stream.get("codec_name", "Unknown"),
                    "codec_long_name": stream.get("codec_long_name", "Unknown"),
                    "sample_rate": stream.get("sample_rate", "Unknown"),
                    "channels": stream.get("channels", "Unknown"),
                    "channel_layout": stream.get("channel_layout", "Unknown"),
                    "bit_rate": stream.get("bit_rate", "Unknown"),
                    "sample_fmt": stream.get("sample_fmt", "Unknown"),
                    "duration": stream.get("duration", "Unknown"),
                    "language": stream.get("tags", {}).get("language", "Unknown"),
                }

                # 格式化音频流比特率
                if audio_stream["bit_rate"] != "Unknown":
                    try:
                        bitrate = int(audio_stream["bit_rate"])
                        if bitrate >= 1000:
                            audio_stream["bit_rate_formatted"] = (
                                f"{bitrate / 1000:.0f} Kbps"
                            )
                        else:
                            audio_stream["bit_rate_formatted"] = f"{bitrate} bps"
                    except (ValueError, TypeError):
                        audio_stream["bit_rate_formatted"] = "Unknown"

                # 格式化采样率
                if audio_stream["sample_rate"] != "Unknown":
                    try:
                        sample_rate = int(audio_stream["sample_rate"])
                        audio_stream["sample_rate_formatted"] = (
                            f"{sample_rate / 1000:.1f} kHz"
                        )
                    except (ValueError, TypeError):
                        audio_stream["sample_rate_formatted"] = "Unknown"

                video_info["audio_streams"].append(audio_stream)

            elif codec_type == "subtitle":
                subtitle_stream = {
                    "index": stream.get("index", "Unknown"),
                    "codec_name": stream.get("codec_name", "Unknown"),
                    "codec_long_name": stream.get("codec_long_name", "Unknown"),
                    "language": stream.get("tags", {}).get("language", "Unknown"),
                    "title": stream.get("tags", {}).get("title", "Unknown"),
                }
                video_info["subtitle_streams"].append(subtitle_stream)

            else:
                other_stream = {
                    "index": stream.get("index", "Unknown"),
                    "codec_type": codec_type,
                    "codec_name": stream.get("codec_name", "Unknown"),
                    "codec_long_name": stream.get("codec_long_name", "Unknown"),
                }
                video_info["other_streams"].append(other_stream)

        # 添加统计信息
        video_info["summary"] = {
            "total_streams": len(streams),
            "video_streams_count": len(video_info["video_streams"]),
            "audio_streams_count": len(video_info["audio_streams"]),
            "subtitle_streams_count": len(video_info["subtitle_streams"]),
            "other_streams_count": len(video_info["other_streams"]),
        }

        # 如果有视频流，添加主要视频信息到摘要
        if video_info["video_streams"]:
            main_video = video_info["video_streams"][0]
            video_info["summary"]["main_video"] = {
                "resolution": main_video["resolution"],
                "codec": main_video["codec_name"],
                "frame_rate": main_video["frame_rate"],
                "bit_rate": main_video.get(
                    "bit_rate_formatted", main_video["bit_rate"]
                ),
            }

        # 如果有音频流，添加主要音频信息到摘要
        if video_info["audio_streams"]:
            main_audio = video_info["audio_streams"][0]
            video_info["summary"]["main_audio"] = {
                "codec": main_audio["codec_name"],
                "sample_rate": main_audio.get(
                    "sample_rate_formatted", main_audio["sample_rate"]
                ),
                "channels": main_audio["channels"],
                "bit_rate": main_audio.get(
                    "bit_rate_formatted", main_audio["bit_rate"]
                ),
            }

        # 返回格式化的JSON字符串
        return json.dumps(video_info, indent=2, ensure_ascii=False)

    except ffmpeg.Error as e:
        error_message = e.stderr.decode("utf8") if e.stderr else str(e)
        raise RuntimeError(f"Error getting video info: {error_message}")
    except FileNotFoundError:
        raise RuntimeError(f"Error: Video file not found at {video_path}")
    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred while getting video info: {str(e)}"
        )


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
