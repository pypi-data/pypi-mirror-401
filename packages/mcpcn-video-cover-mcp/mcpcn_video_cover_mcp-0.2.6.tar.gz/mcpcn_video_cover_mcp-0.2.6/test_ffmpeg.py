#!/usr/bin/env python3
"""
测试 ffmpeg 子进程调用
用法: python test_ffmpeg.py
"""
import subprocess
import platform
import time
import sys

# Windows subprocess 常量
if platform.system() == 'Windows':
    CREATE_NO_WINDOW = 0x08000000
else:
    CREATE_NO_WINDOW = 0

def test_ffmpeg():
    """测试 ffmpeg 命令执行"""
    
    # 配置参数
    FFMPEG_BINARY = r"C:\Users\zcj40\Desktop\gjjk\rapido\bin\ffmpeg\bin\ffmpeg.exe"
    cover_image_path = r"C:\Users\zcj40\Desktop\cdb8719198766edb172dcd1fe24320dc.png"
    video_path = r"C:\Users\zcj40\Desktop\97acd344c1c4f39facb2e5dfe2cd11c5.mp4"
    output_video_path = r"C:\Users\zcj40\Desktop\test_output1.mp4"
    cover_duration = 1.5
    video_width = 852
    video_height = 480
    fps = 30
    
    # 构建命令
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
    
    print("=" * 80)
    print("测试 FFmpeg 子进程调用")
    print("=" * 80)
    print(f"平台: {platform.system()}")
    print(f"Python 版本: {platform.python_version()}")
    print(f"\nFFmpeg 路径: {FFMPEG_BINARY}")
    print(f"封面图片: {cover_image_path}")
    print(f"输入视频: {video_path}")
    print(f"输出视频: {output_video_path}")
    print(f"\n完整命令:\n{' '.join(cmd)}")
    print("=" * 80)
    
    # 测试方法 1: 使用 DEVNULL + CREATE_NO_WINDOW
    print("\n[测试 1] 使用 DEVNULL + CREATE_NO_WINDOW")
    try:
        start_time = time.time()
        kwargs = {
            'check': True,
            'stdout': subprocess.DEVNULL,
            'stderr': subprocess.DEVNULL,
            'stdin': subprocess.DEVNULL,
        }
        if platform.system() == 'Windows':
            kwargs['creationflags'] = CREATE_NO_WINDOW
        
        print("开始执行...")
        result = subprocess.run(cmd, **kwargs)
        duration = time.time() - start_time
        print(f"✓ 成功! 耗时: {duration:.2f} 秒")
        print(f"返回码: {result.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"✗ 失败! 返回码: {e.returncode}")
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
    
    # 测试方法 2: 捕获输出（用于调试）
    print("\n[测试 2] 捕获输出（调试模式）")
    output_video_path_2 = r"C:\Users\zcj40\Desktop\test_output_2.mp4"
    cmd[-1] = output_video_path_2
    
    try:
        start_time = time.time()
        kwargs = {
            'check': True,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'stdin': subprocess.DEVNULL,
            'text': True,
        }
        if platform.system() == 'Windows':
            kwargs['creationflags'] = CREATE_NO_WINDOW
        
        print("开始执行...")
        result = subprocess.run(cmd, **kwargs)
        duration = time.time() - start_time
        print(f"✓ 成功! 耗时: {duration:.2f} 秒")
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"标准输出:\n{result.stdout[:500]}")
        if result.stderr:
            print(f"标准错误:\n{result.stderr[:500]}")
    except subprocess.CalledProcessError as e:
        print(f"✗ 失败! 返回码: {e.returncode}")
        if e.stderr:
            print(f"错误信息:\n{e.stderr[:500]}")
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    test_ffmpeg()
