import json
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.renderers import JSONRenderer


class StudentJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'student': data
        })


class StudentsJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'students': data
        })

class AttendanceRecordsRenderer(JSONRenderer): 

    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'attendance_records': data
        })

class CommentJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            return json.dumps({
                'comments': data,
            })
        return json.dumps({
            'comment': data
        })
