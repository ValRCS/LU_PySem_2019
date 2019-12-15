import ffmpeg
import numpy as np
import os
import subprocess
from deepdream import DeepDream

# Based on https://github.com/kkroening/ffmpeg-python/blob/master/examples/tensorflow_stream.py
def start_ffmpeg_process1(in_filename):
    args = (
        ffmpeg
        .input(in_filename).filter_("scale", w="640", h="360") # Resize to 640x360 or else it will take forever
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .compile()
    )
    return subprocess.Popen(args, stdout=subprocess.PIPE)


def start_ffmpeg_process2(out_filename, width, height):
    args = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
        .output(out_filename, pix_fmt='yuv420p')
        .overwrite_output()
        .compile()
    )
    return subprocess.Popen(args, stdin=subprocess.PIPE)


def read_frame(process1, width, height):
    # Note: RGB24 == 3 bytes per pixel.
    frame_size = width * height * 3
    in_bytes = process1.stdout.read(frame_size)
    if len(in_bytes) == 0:
        frame = None
    else:
        assert len(in_bytes) == frame_size
        frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([height, width, 3])
        )
    return frame

def write_frame(process2, frame):
    process2.stdin.write(
        frame
        .astype(np.uint8)
        .tobytes()
    )

def Twelve():
    print("Deep dreaming input/stock.mkv to output/12.mkv")
    process_frame = DeepDream().process_frame
    width = 640
    height = 360
    process1 = start_ffmpeg_process1("input/stock.mkv")
    process2 = start_ffmpeg_process2("output/12.mkv", width, height)
    while True:
        in_frame = read_frame(process1, width, height)
        if in_frame is None:
            break

        out_frame = process_frame(in_frame)
        write_frame(process2, out_frame)

    process1.wait()

    process2.stdin.close()
    process2.wait()

Twelve()

