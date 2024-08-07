



"""
Extract background images from a tar archive.

"""


__all__ = (
    'extract_backgrounds',
)


import os
import sys
import tarfile

import cv2
import numpy


def im_from_file(f):
    a = numpy.asarray(bytearray(f.read()), dtype=numpy.uint8)
    return cv2.imdecode(a, cv2.CV_LOAD_IMAGE_GRAYSCALE)


def extract_backgrounds(archive_name):
    """
    Extract backgrounds from provided tar archive.

    JPEGs from the archive are converted into grayscale, and cropped/resized to
    256x256, and saved in ./bgs/.

    :param archive_name:
        Name of the .tar file containing JPEGs of background images.

    """
    os.mkdir("bgs")

    t = tarfile.open(name=archive_name)

    def members():
        m = t.next()
        while m:
            yield m
            m = t.next()
    index = 0
    for m in members():
        if not m.name.endswith(".jpg"):
            continue
        f =  t.extractfile(m)
        try:
            im = im_from_file(f)
        finally:
            f.close()
        if im is None:
            continue
        
        if im.shape[0] > im.shape[1]:
            im = im[:im.shape[1], :]
        else:
            im = im[:, :im.shape[0]]
        if im.shape[0] > 256:
            im = cv2.resize(im, (256, 256))
        fname = "bgs/{:08}.jpg".format(index)
        print fname
        rc = cv2.imwrite(fname, im)
        if not rc:
            raise Exception("Failed to write file {}".format(fname))
        index += 1


if __name__ == "__main__":

    extract_backgrounds(sys.argv[1])

