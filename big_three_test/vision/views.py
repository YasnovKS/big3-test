from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseServerError
from django.views.generic import FormView

from vision.camera_vision import CameraConfig, DetectionConfig, VideoCatch
from vision.forms import CameraForm


class IndexView(FormView):
    template_name = 'index.html'
    form_class = CameraForm

    def post(
        self, request: HttpRequest, *args: str, **kwargs: Any
    ) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            camera_url = data.get('camera_url')
            camera_config = CameraConfig(camera_url=camera_url)
            detection_config = DetectionConfig(object_type='cars')
            video_stream = VideoCatch(
                camera_config=camera_config, detection=detection_config
            )
            stream_response = video_stream.process()
            if not stream_response:
                raise HttpResponseServerError(
                    'В процессе обработки запроса произошла ошибка.'
                )
            response = self.get(request, *args, **kwargs)
            response.context_data.update(
                {'file_url': stream_response}
            )
            return response
        return super().post(request, *args, **kwargs)
