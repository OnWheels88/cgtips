import mvexportutils
import os

def isSupported():
    try:
        status, (stdout, stderr) = mvexportutils.run(['ffmpeg'])
    except:
        return False
    return True

def ffmpeg_queryCodecs():
    video_codecs = {}
    audio_codecs = {}

    status, (stdout, stderr) = mvexportutils.run(['ffmpeg', '-formats'])
    lines = stdout.splitlines()
    try:
        codec_start = lines.find('Codecs:')
    except:
        # Probably failed due to a newer version of ffmpeg.
        status, (stdout, stderr) = mvexportutils.run(['ffmpeg', '-codecs'])
        lines = stdout.splitlines()
        codec_start = 0
    for line in lines[codec_start+1:]:
        if len(line) == 0:
            break

        space_index = line.rfind(' ')
        if space_index >= 0:
            codec_flags = line[1:space_index]
            # We may not have enough characters, in which
            # case we skip this.
            if len(codec_flags) > 3:
                if codec_flags[2] == 'V':
                    video_codecs[line[space_index+1:]] = codec_flags
                elif codec_flags[2] == 'A':
                    audio_codecs[line[space_index+1:]] = codec_flags
    return video_codecs, audio_codecs

def encode(kwargs):

    fps = 10
    max_colors=64
     #YOUR PATH for CACHE pallete
    CACHE_PALLETE = 'D:/_CACHE/palette.png'
    
    #presets
    if kwargs['videopreset'].find('high') >= 0:
        fps = kwargs['framerate']
        max_colors = 256
    if kwargs['videopreset'].find('medium') >= 0:
        fps = 15
        max_colors=64
    if kwargs['videopreset'].find('low') >= 0:
        fps = 10
        max_colors=32
    
    args = []
    args.append('ffmpeg')
    # Ensure that we don't prompt about overwriting output files.
    args.append('-y')
    args.extend(['-i', kwargs['imagefilesstringformat']])

    #prepearre palette for gif
    args_pallete=[]
    args_pallete.append('ffmpeg')
    args_pallete.append('-y')
    args_pallete.extend(['-i',  kwargs['imagefilesstringformat']])
    args_pallete.extend(['-vf','fps=%g ,scale=320:-1:flags=lanczos,palettegen=stats_mode=diff:max_colors=%s' %(fps, max_colors)])
    args_pallete.extend(['-y', CACHE_PALLETE])   
        
    args.extend(['-i',CACHE_PALLETE])
    args.extend(['-lavfi','fps=%g [x];[x][1:v] paletteuse' % fps])
    #print("%s",args_pallete)

    args.append(kwargs['outputfile'])
    #print("%s",args)
    return mvexportutils.run(args)
