import os


def generate_upload_path(instance, filename):
    return os.path.join(instance._meta.model_name, filename)
