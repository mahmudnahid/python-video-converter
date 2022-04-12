# @TODO: Multi threading support

def convert_video(in_file, convert_to, dest_dir=None):

    converted_files = []

    try:
        from converter import Converter
    except ImportError:
        print "The package 'converter' not found. Please install from: https://github.com/senko/python-video-converter"
        return

    import os

    src_path = in_file[:in_file.rfind('/')] + '/'
    if not dest_dir:
        dest_dir = src_path

    # set working directory to src_path
    if os.path.isdir(src_path):
        os.chdir(src_path)
        print('Changing directory to: {}'.format(src_path))
    else:
        print('Source directory "{}" doesn\'t exits'.format(src_path))
        return False

    # extract fileName from infile
    file_name = in_file[in_file.rfind('/') + 1:in_file.rfind('.')]
    file_extension = in_file[in_file.rfind('.'):]

    if not os.path.isfile(file_name+file_extension):
        print('Source file "{}" doesn\'t exits'.format(file_name+file_extension))
        return False

    # rename src file to lowercase
    if not file_name.islower():
        os.rename(file_name+file_extension, file_name.lower()+file_extension)
        file_name = file_name.lower()
        in_file = src_path+file_name+file_extension
        print('renaming file {} to {}'.format(file_name+file_extension, file_name.lower()+file_extension))

    c = Converter()

    video_info = c.probe(in_file)

    for output_format, output_qualities in convert_to.items():

        for output_quality in output_qualities:

            output_properties = get_properties(output_format, output_quality)
            if not output_properties:
                return False

            print(output_properties['options'])

            out_file = dest_dir + file_name + '_' + output_quality + output_properties['ext']
            # print(out_file)

            conv = c.convert(in_file, out_file, output_properties['options'])
            #add to the converted files list
            converted_files.append(out_file)

            try:
                for timecode in conv:
                    print "Converting (%f) ...\r" % timecode
            except Exception as e:
                print(e)
                continue


                # c.thumbnails(in_flie, [(5, '/tmp/shot.png', '320x240'), (10, '/tmp/shot2.png', None, 5)])
    return converted_files


def get_properties(vformat, vquality):

    supported_formats = ('webm', 'mp4', 'flv')
    supported_qualities = ('180p', '320p', '360p', '480p', '720p')

    if vformat not in supported_formats:
        print("Format specified '{}' is not a web standard. Please chose within {}".format(vformat, supported_formats))
        return False

    if vquality not in supported_qualities:
        print("Quality specified '{}' is not a web standard. Please chose within {}".format(vquality, supported_qualities))
        return False

    vproperties = dict()

    ######################
    # set format options #
    if vformat is 'webm':
        vproperties['ext'] = '.' + vformat
        vproperties['options'] = {
            'format': vformat,
            'audio': {'codec': 'vorbis'},
            'video': {'codec': 'vp8'},
            }
    elif vformat is 'mp4':
        vproperties['ext'] = '.' + vformat
        vproperties['options'] = {
            'format': vformat,
            'audio': {'codec': 'aac'},
            'video': {'codec': 'h264'},
            }
    elif vformat is 'flv':
        vproperties['ext'] = '.' + vformat
        vproperties['options'] = {
            'format': vformat,
            'audio': {'codec': 'mp3'},
            'video': {'codec': 'h263'},
            }

    ##########################
    # set quality parameters #
    if vquality is '180p':
        vproperties['options']['audio'].update({
            # One quarter the sampling rate of audio CDs;
            # used for lower-quality PCM, MPEG audio and for audio analysis of subwoofer bandpasses
            'samplerate': 11025,
            'channels': 2,
            'bitrate': 32,
            })
        vproperties['options']['video'].update({
            'bitrate': 150,
            'height': 180,
            })
    elif vquality is '320p':
        vproperties['options']['audio'].update({
            # One half the sampling rate of audio CDs; used for lower-quality PCM and MPEG audio and
            # for audio analysis of low frequency energy. Suitable for digitizing early 20th century audio formats
            'samplerate': 22050,
            'channels': 2,
            'bitrate': 64,
            })
        vproperties['options']['video'].update({
            'bitrate': 400,
            'height': 320,
            })
    elif vquality is '360p':
        vproperties['options']['audio'].update({
            # miniDV, digital camcorder, DVCAM, DAT, FM Radio
            'samplerate': 32000,
            'channels': 2,
            'bitrate': 64,
            })
        vproperties['options']['video'].update({
            'bitrate': 700,
            'height': 360,
            })
    elif vquality is '480p':
        vproperties['options']['audio'].update({
            # Audio CD, also most commonly used with MPEG-1 audio (VCD, SVCD, MP3).
            'samplerate': 44100,
            'channels': 2,
            'bitrate': 96,
            })
        vproperties['options']['video'].update({
            'bitrate': 1100,
            'height': 480,
            })
    elif vquality is '720p':
        vproperties['options']['audio'].update({
            # The standard audio sampling rate used by professional digital video equipment
            'samplerate': 48000,
            'channels': 2,
            'bitrate': 128,
            })
        vproperties['options']['video'].update({
            'bitrate': 2000,
            'height': 720,
            })

    # print(vproperties)
    return vproperties


#if __name__ == "__main__":
#    in_flie = '/home/nahid/Documents/video_test.mp4'
#
#    convert_to = {
#        'webm': ['180p', '320p', '360p', '480p', '720p'],
#        'mp4': ['180p', '320p', '360p', '480p', '720p']
#    }
#    #convert_to = {
#    #    'webm': ['180p']
#    #}
#
#    print convert_video(in_flie, convert_to)
