from django import forms


class CameraForm(forms.Form):
    camera_url = forms.URLField(label='URL камеры', required=True)
