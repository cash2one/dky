
from zoo.configs.default import DefaultConfig
import os,time

def allowed_file(file_name):
    return '.' in file_name and \
            file_name.rsplit('.', 1)[1] in DefaultConfig.ALLOWED_EXTENSIONS



def upload_file(file, path):
    file.save(os.path.join(path, file.filename))


def delete_file(filename, path):
    file_path = os.path.join(path, filename)
    os.remove(file_path)
