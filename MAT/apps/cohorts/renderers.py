import json

from rest_framework.renderers import JSONRenderer


class CohortJSONRenderer(JSONRenderer):
    """A renderer for a single cohort details

    Args:
        JSONRenderer (class): The base JSON render

    Returns:
        JSON: The json data that is formated according to this renderer.
    """
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'cohort': data
        })


class CohortsJSONRenderer(JSONRenderer):
    """A renderer for a list of cohorts

    Args:
        JSONRenderer (class): The base JSON render

    Returns:
        JSON: The json data that is formated according to this renderer.
    """
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'cohorts': data
        })
