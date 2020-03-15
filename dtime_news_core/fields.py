import os
import base64
from django.utils.translation import ugettext_lazy as _
from drf_extra_fields.fields import Base64FileField

class VideoBase64FileField(Base64FileField):
    ALLOWED_TYPES = ['mp4', 'flv', 'avi', 'wmv', 'rm', 'rmvb', 
                     'm4p ', 'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 
                     '3gp', 'flv']
    
    # def to_internal_value(self, base64_data):
    #     file_name = ''
    #     if ';base64,' in base64_data:
    #         file_name, base64_data = base64_data.split(';base64,')
    #     self.file_name =  file_name
    #     return Base64FileField.to_internal_value(self, base64_data)
    
    def get_file_extension(self, filename, decoded_file):
        if self.file_name:
            return os.path.splitext(self.file_name)[1][1:]
        return ''

