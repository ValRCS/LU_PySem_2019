import ffmpeg
from utils import Cmd, run

@Cmd("one")
def One():
    print("Converting input/1.mkv to output/1.mp4")
    # Open input/1.mkv
    in_file = ffmpeg.input("input/1.mkv")
    # Save it to output/1.mp4
    ffmpeg.output(in_file, "output/1.mp4").run(quiet=True)
    ffmpeg.output(in_file, "output/1.mp4").view()

@Cmd("two")
def Two():
    print("Splitting input/1.mkv into output/2_video.webm and output/2_audio.mp3")
    in_file = ffmpeg.input("input/1.mkv")
    # Save the video stream to output/2_video.mp4
    ffmpeg.output(in_file.video, "output/2_video.mp4").run(quiet=True)
    ffmpeg.output(in_file.video, "output/2_video.mp4").view()
    # Save the audio stream to output/2_audio.mp3
    ffmpeg.output(in_file.audio, "output/2_audio.mp3").run(quiet=True)
    ffmpeg.output(in_file.audio, "output/2_audio.mp3").view()

@Cmd("three")
def Three():
    print("Combining output/2_video.mp4 and output/2_audio.mp3 in output/3.mkv")
    in_video = ffmpeg.input("output/2_video.mp4")
    in_audio = ffmpeg.input("output/2_audio.mp3")
    # Save both streams to output/3.mkv
    ffmpeg.output(in_video, in_audio, "output/3.mkv").run(quiet=True)
    ffmpeg.output(in_video, in_audio, "output/3.mkv").view()

@Cmd("four")
def Four():
    print("Getting the 6th second of input/1.mkv as output/4.mkv")
    in_file = ffmpeg.input("input/1.mkv")

    # Trim the video from 5 to 6 seconds
    trimmed_video = in_file.video.trim(start=5, end=6)
    # Recalculate new timestamps for the video (or else they'll start at 5)
    trimmed_video = trimmed_video.setpts("PTS-STARTPTS")

    # Trim the audio from 5 to 6 seconds
    trimmed_audio = in_file.audio.filter_("atrim", start=5, end=6)
    # Recalculate new timestamps for the audio
    trimmed_audio = trimmed_audio.filter_("asetpts", "PTS-STARTPTS")
    
    # Save both trimmed streams to output/4.mkv
    ffmpeg.output(trimmed_video, trimmed_audio, "output/4.mkv").run(quiet=True)
    ffmpeg.output(trimmed_video, trimmed_audio, "output/4.mkv").view()

@Cmd("five")
def Five():
    print("Combining input/1.mkv and input/2.mkv into output/5.mkv")
    in_first = ffmpeg.input("input/1.mkv")
    in_second = ffmpeg.input("input/2.mkv")

    # Scale second video to have the same width as the first video
    in_second = in_second.filter_("scale", w="480", h="270")
    # Add 270px of padding at the bottom of the first video
    in_first = in_first.filter_("pad", width="480", height="360+270")

    # Overlay the second video at y=360 on top of the first video
    in_first = in_first.overlay(in_second, x=0, y=360, shortest=1)

    ffmpeg.output(in_first, "output/5.mkv").view()
    ffmpeg.output(in_first, "output/5.mkv").run(quiet=True)

@Cmd("six")
def Six():
    print("Greenscreening greenscreen/1-4.mkv onto input/2.mkv and saving it as output/6.mkv")
    background = ffmpeg.input("input/2.mkv")
    greenscreen1 = ffmpeg.input("greenscreen/1.mkv", itsoffset=9)
    greenscreen2 = ffmpeg.input("greenscreen/2.mkv", itsoffset=4.5)
    greenscreen3 = ffmpeg.input("greenscreen/3.mkv")
    greenscreen4 = ffmpeg.input("greenscreen/4.mkv", itsoffset=7)

    greenscreen1 = greenscreen1.filter_("scale", width="1280", height="720")
    greenscreen2 = greenscreen2.filter_("scale", width="1280", height="720")
    greenscreen3 = greenscreen3.filter_("scale", width="1280", height="720")
    greenscreen4 = greenscreen4.filter_("scale", width="1280", height="720")

    # Apply chroma key to turn green into transparency
    greenscreen1 = greenscreen1.filter_("chromakey", color="green", similarity=0.15, blend=0.05)
    greenscreen2 = greenscreen2.filter_("chromakey", color="green", similarity=0.15, blend=0.05)
    greenscreen3 = greenscreen3.filter_("chromakey", color="green", similarity=0.15, blend=0.05)
    greenscreen4 = greenscreen4.filter_("chromakey", color="green", similarity=0.15, blend=0.05)

    background = background.overlay(greenscreen3, eof_action="pass", shortest=1)
    background = background.overlay(greenscreen4, eof_action="pass", shortest=1)
    background = background.overlay(greenscreen2, eof_action="pass", shortest=1)
    background = background.overlay(greenscreen1, eof_action="pass", shortest=1)

    ffmpeg.output(background, "output/6.mkv").view()
    ffmpeg.output(background, "output/6.mkv").run(quiet=True)

@Cmd("seven")
def Seven():
    print("Detecting edges of input/stock.mkv to output/ 7_bw 7_color .mkv")
    background = ffmpeg.input("input/stock.mkv")

    background1 = background.filter_("edgedetect")
    background2 = background.filter_("edgedetect", mode="colormix")

    ffmpeg.output(background1, "output/7_bw.mkv").view()
    ffmpeg.output(background2, "output/7_color.mkv").view()
    ffmpeg.output(background1, "output/7_bw.mkv").run(quiet=True)
    ffmpeg.output(background2, "output/7_color.mkv").run(quiet=True)

@Cmd("eight")
def Eight():
    print("Lagfun effect on input/stock.mkv to output/8.mkv")
    background = ffmpeg.input("input/stock.mkv")

    background = background.filter_("lagfun")

    ffmpeg.output(background, "output/8.mkv").view()
    ffmpeg.output(background, "output/8.mkv").run(quiet=True)

@Cmd("nine")
def Nine():
    print("Lagfun + random effect on input/stock.mkv to output/9.mkv")
    background = ffmpeg.input("input/stock.mkv")

    background = background.filter_("lagfun")
    background = background.filter_("random", frames=32)

    ffmpeg.output(background, "output/9.mkv").view()
    ffmpeg.output(background, "output/9.mkv").run(quiet=True)

@Cmd("ten")
def Ten():
    print("Scene to output/10.mkv")
    # Open the image and loop it
    background = ffmpeg.input("input/background.jpg", loop=1)
    # Crop height to be an even number, because h264 is unable to encode odd heights
    background = background.crop(x=0, y=0, width=1300, height=730)

    h1 = ffmpeg.input("input/h1.mp4")
    h1 = h1.crop(0, 180, 400, 180)
    h1 = h1.filter_("chromakey", color="#00aa00", similarity=0.15, blend=0.01)
    # Use the video loop filter to loop forever
    h1 = h1.filter_("loop", loop=-1, size=10000)
    h1 = h1.filter_("rotate", fillcolor="none", out_w="sqrt(in_w * in_w + in_h * in_h)", out_h="out_w", angle="sin(sin(t * 3.14159265 / 0.75) * 3.14159265 / 3)")

    h2 = ffmpeg.input("input/h2.mkv", itsoffset="5")
    h2 = h2.hflip()
    # Use expressions to calculate the height
    h2 = h2.filter_("scale", width="1300", height="out_w / in_w * in_h")
    h2 = h2.filter_("chromakey", color="green", similarity=0.15, blend=0.01)

    # Use expressions to dynamically calculate the x and y position
    background = background.overlay(h1, x="sin(t*3.141592/3)*40+30", y="sin(t*3.141592/3)*20+10", eof_action="pass")
    background = background.overlay(h2, x=0, y=0, eof_action="endall")

    ffmpeg.output(background, "output/10.mkv").view()
    ffmpeg.output(background, "output/10.mkv").run(quiet=True)

# Based on http://oioiiooixiii.blogspot.com/2019/04/ffmpeg-crt-screen-effect.html
def generateCRT(stream):
    # Reduce input to 25% PAL resolution
    stream = stream.filter_("scale", w=-2, h=144)
    # Crop to 4:3 aspect ratio at 25% PAL resolution
    stream = stream.filter_("crop", w=180,h=144)

    # Create RGB chromatic aberration
    streams = stream.filter_multi_output("split", 3)
    stream0 = streams[0].filter_("lutrgb", g="0", b="0").filter_("scale", w=188, h=144).filter_("crop", w=180, h=144)
    stream1 = streams[1].filter_("lutrgb", r="0", b="0").filter_("scale", w=184, h=144).filter_("crop", w=180, h=144)
    stream2 = streams[2].filter_("lutrgb", r="0", g="0").filter_("scale", w=180, h=144).filter_("crop", w=180, h=144)

    stream = ffmpeg.filter_([ffmpeg.filter_([stream0, stream2], "blend", all_mode="addition"), stream1], "blend", all_mode="addition").filter_("format", "gbrp")

    # Create YUV chromatic aberration
    streams = stream.filter_multi_output("split", 3)
    stream0 = streams[0].filter_("lutyuv", u="0", v="0").filter_("scale", w=192, h=144).filter_("crop", w=180, h=144)
    stream1 = streams[1].filter_("lutyuv", y="0", v="0").filter_("scale", w=188, h=144).filter_("crop", w=180, h=144)
    stream2 = streams[2].filter_("lutyuv", y="0", u="0").filter_("scale", w=180, h=144).filter_("crop", w=180, h=144)

    stream = ffmpeg.filter_([ffmpeg.filter_([stream0, stream2], "blend", all_mode="lighten"), stream1], "blend", all_mode="lighten")

    # Create edge contour effect
#    stream = stream.filter_("edgedetect", mode="colormix", high=0)

    # Add noise to each frame of input
    stream = stream.filter_("noise", c0s=8, allf="t")

    # Add interlaced fields effect to input
    streams = stream.filter_multi_output("split")
    stream0 = streams[0].filter_("format", "yuv420p").filter_("curves", preset="darker")
    stream = ffmpeg.filter_([stream0, streams[1]], "blend", all_expr="if(eq(0,mod(Y,2)),A,B)")

    # Re-scale input to full PAL resolution
    stream = stream.filter_("scale", w=720, h=576)

    fontfile = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"

    # Add magnetic damage effect to input [crt screen]
    magnetic_damage = ffmpeg.input("input/PAL.png", loop=1)
#    magnetic_damage = ffmpeg.input("nullsrc=s=720x576", f="lavfi")
    magnetic_damage = magnetic_damage.filter_("drawtext", fontfile=fontfile, text="@", x=600, y=30, fontsize=170, fontcolor="red@1.0")
    magnetic_damage = magnetic_damage.filter_("boxblur", 80)
    stream = ffmpeg.filter_([magnetic_damage, stream], "blend", all_mode="screen", shortest=1)

    tmppal = ffmpeg.input("input/PAL.png", loop=1)
#    tmppal = ffmpeg.input("nullsrc=s=720x576", f="lavfi")
    tmppal = tmppal.filter_("format", "gbrp")
    tmppal = tmppal.filter_multi_output("split")

    # Add reflections to input [crt screen]
    reflections = tmppal[0]
    reflections = reflections.filter_("drawtext", fontfile=fontfile, text="€", x=50, y=50, fontsize=150, fontcolor="white")
    reflections = reflections.filter_("drawtext", fontfile=fontfile, text="J", x=600, y=460, fontsize=120, fontcolor="white")
    reflections = reflections.filter_("boxblur", 25)
    stream = ffmpeg.filter_([reflections, stream], "blend", all_mode="screen", shortest=1)

    # Add more detailed highlight to input [crt screen]
    highlights = tmppal[1]
    highlights = highlights.filter_("drawtext", fontfile=fontfile, text="¡", x=80, y=60, fontsize=90, fontcolor="white")
    highlights = highlights.filter_("boxblur", 7)

    stream = ffmpeg.filter_([highlights, stream], "blend", all_mode="screen", shortest=1)

    # Curve input to mimic curve of crt screen
    stream = stream.filter_("vignette").filter_("format", "gbrp").filter_("lenscorrection", k1=0.2, k2=0.2)

    # Add bloom effect to input [crt screen]
    streams = stream.filter_multi_output("split")
    
    stream1 = streams[1].filter_("boxblur", 26)
    stream1 = stream1.filter_("format", "gbrp")

    stream = ffmpeg.filter_([stream1, streams[0]], "blend", all_mode="screen", shortest=1)

    return stream

@Cmd("eleven")
def Eleven():
    print("CRTifying input/stock.mkv to output/11.mkv")
    background = ffmpeg.input("input/stock.mkv")

    background_crt = generateCRT(background)

    ffmpeg.output(background_crt, "output/11.mkv").view()
    ffmpeg.output(background_crt, "output/11.mkv").run(quiet=True)

def main():
    run()

if __name__ == "__main__":
    main()

