from mutagen.mp3 import MP3

# function to check for the session
def check_for_session(request):
    """

    :param request:
    :return:
    """
    is_band = request.session.get('is_band')
    band_id = None

    if is_band:
        try:
            band_id = int(request.session.get('id'))
        except:
            pass

    return is_band, band_id


def get_song_duration(song_path):
    """
    function to return song duration minutes
    """
    audio = MP3(song_path)
    duration = audio.info.length

    min, sec = divmod(duration, 60)

    return "%d:%.02d"%(min, sec)


