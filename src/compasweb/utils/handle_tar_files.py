import os
import shutil
import tarfile


def compress_files_into_tarball(filespath, tarfilepath):
    """
    Compress the contents of a directory into a tarball
    params:
    filespath: path to the directory to be compressed
    """
    # print('eman1')
    # print(f'filespath: {filespath}')
    # tarfilepath = os.path.join('/tmp/django', "output.tar.gz")
    # print(f'tarfilepath: {tarfilepath}')

    if os.path.exists(tarfilepath):
        return tarfilepath

    tf = tarfile.open(tarfilepath, mode="w:gz")
    size = tf.gettarinfo().size
    tf.add(filespath)
    tf.close()
    return size
