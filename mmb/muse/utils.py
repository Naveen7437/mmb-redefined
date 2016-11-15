import json
from rest_framework.parsers import BaseParser, DataAndFiles
from django.conf import settings
from django.http.multipartparser import MultiPartParser as DjangoMultiPartParser, MultiPartParserError
from django.utils import six
from rest_framework.exceptions import ParseError

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


class MultiPartJSONParser(BaseParser):
    """
    multi-part form parser class
    """
    media_type = 'multipart/form-data'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as a multipart encoded form,
        and returns a DataAndFiles object.
        `.data` will be a `QueryDict` containing all the form parameters, and JSON decoded where available.
        `.files` will be a `QueryDict` containing all the form files.
        """
        parser_context = parser_context or {}
        request = parser_context['request']
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        meta = request.META.copy()
        meta['CONTENT_TYPE'] = media_type
        upload_handlers = request.upload_handlers

        try:
            parser = DjangoMultiPartParser(meta, stream, upload_handlers, encoding)
            data, files = parser.parse()
            for key in data:
                if data[key]:
                    try:
                        data[key] = json.loads(data[key])
                    except ValueError:
                        pass
            return DataAndFiles(data, files)
        except MultiPartParserError as exc:
            raise ParseError('Multipart form parse error - %s' % six.text_type(exc))
