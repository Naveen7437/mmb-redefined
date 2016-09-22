# import os
# from celery import task
#
# try:
#     from StringIO import StringIO
# except ImportError:
#     from io import BytesIO
#
# import PIL
# from PIL import Image
# from django.core.files.uploadedfile import SimpleUploadedFile
#
# @task
# def update_user_avatar(instance):
#     """
#
#     """
#     image_name = os.path.split(instance.avatar.name)[-1]
#
#     # don't need to save default image everytime so checking
#     # if image is default type then bypassing this method
#
#     # TODO: change this *******
#     if image_name != "default.png":
#         # open image using PIL
#         img = Image.open(instance.avatar.path)
#         img.resize((300, 450), PIL.Image.ANTIALIAS)
#
#
#         temp_handle = BytesIO()
#         img.save(temp_handle, 'png')
#         temp_handle.seek(0)
#
#         img_file = SimpleUploadedFile(image_name, temp_handle.read(),
#                                       content_type='image/png')
#
#         instance.avatar.save('{0}.png'.format(os.path.splitext(img_file.name)[0]), img_file)
#
