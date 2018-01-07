import os
from shutil import copy2
from datetime import datetime
from PIL import Image


def get_date_from_exif(path):
    EXIFdate = Image.open(path)._getexif()[36867]
    return datetime.strptime(EXIFdate, "%Y:%m:%d %H:%M:%S")

def get_date_from_OS(path):
    stat = os.stat(pathname + "/" + filename)
    return datetime.fromtimestamp(stat.st_mtime)

def move_to_folder(path, filename, day, delete=True):
    if not os.path.isdir(path + "/Day - " + str(day)):
        os.mkdir(path + "/Day - " + str(day))

    copy2(path + "/" + filename, path + "/Day - " + str(day))
    if delete:
        os.remove(path + "/" + filename)

if __name__ == '__main__':
    #pathname = raw_input("Please enter the path with the files in it\n")
    #pathname = "M:/test"
    pathname = "M:/StudyAbroadPictures"
    sDate = datetime(2017, 9, 9)

    if os.path.isdir(pathname):

        numImg = 0
        numMov = 0

        for filename in os.listdir(pathname):
            if filename.endswith(".jpg"):
                numImg += 1
            elif filename.endswith(".mp4"):
                numMov += 1

        print  "dir has %i images and %i videos" % (numImg, numMov)

        raw = raw_input("press enter to continue, enter q to quit\n")
        if raw == "q":
            quit()

        for filename in os.listdir(pathname):
            if filename.endswith(".jpg"):
                try:
                   date = get_date_from_exif(pathname + "/" + filename)
                except KeyError:
                    date = get_date_from_OS(pathname + "/" + filename)
                    print "File %s has no date EXIF data, using stat.st_mtime" % (filename)
                delta = date - sDate
                print "IMG %s @%s,  day %i " % (filename, str(date), delta.days)
                move_to_folder(pathname, filename, delta.days)
            elif filename.endswith(".mp4"):
                date = get_date_from_OS(pathname + "/" + filename)
                delta = date - sDate
                print "MOV %s @%s, day %i" % (filename, str(date), delta.days)
                move_to_folder(pathname, filename, delta.days)
    else:
       print "This is not a directory. Quiting"