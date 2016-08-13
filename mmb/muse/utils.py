#------------------------------------------#
# Util functions come here
#------------------------------------------#

# function to check for the session
def check_for_session(request):
    is_band = request.session.get('is_band')
    band_id = None

    if is_band:
        try:
            band_id = int(request.session.get('id'))
        except:
            pass

    return is_band, band_id

