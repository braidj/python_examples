# Finds duplicates of certain files between 2 different sources
import datetime
import hashlib
import os
import re
import shutil
import sys
import time

from PIL import Image

# archive_folder = "C:\\Users\\Jason\\Desktop\\Duplicates" # default, can be overriden
# archive_folder = "D:\\Duplicates" # Dell

archive_folder = "C:\\Users\\Jason\\Desktop\\Duplicates"  # laptop

filter_by = ['.DOCX', '.DOC', '.XSL', '.XLSX', '.PDF', '.JPG', '.PNG', '.EML', '.JPG', '.BMP', '.MP4', '.MP3', '.MOV',
             '.AVI']
photos = ['.JPG', '.JPEG', '.BMP', '.PNG']

redundant_files = ['.ini', '.db']
# redundant_folder = user selection


def is_dated_folder(src_fld, debug=0):
    # ------------------------------------------------------------------------------------------
    # Date: 20150504
    # Updated: 20160306
    # Author: braidj@gmail.com
    # Purpose: Checks if folder is in format of mmMMMYYYY, or YYYY
    # Input: current or source folder
    # Output: True / False
    # -------------------------------------------------------------------------------------------

    nos_validation_errors = 0

    if debug:
        print(("CALLED: is_dated_folder(%s,%s)" % (src_fld, debug)))

    # matching on mmMMMMYYYY
    match = re.search(r'(\d{2})(\w{3})(\d{4})', src_fld)

    try:

        result = match.groups(0)  # Have match, process further

        if debug:
            print(("month digit=[%s]month code=[%s]year=[%s]" % (
                match.group(1), match.group(2), match.group(3))))

        if check_month_nos(match.group(1), debug) == False:
            nos_validation_errors = + 1

        if check_month_chars(match.group(2), debug) == False:
            nos_validation_errors = + 1

        if nos_validation_errors == 0:
            if debug:
                print("%s is correctly named" % src_fld)
            return True
        else:
            if debug:
                print("%s is INCORRECTLY named" % src_fld)
            return False
    except:

        # No match
        if debug:
            print("%s does not match the required pattern for a dated folder" % src_fld)
        return False


def is_year_folder(src_fld, debug=0):
    # ------------------------------------------------------------------------------------------
    # Date: 20160306
    # Author: braidj@gmail.com
    # Purpose: Checks if folder name is a valid year
    # Output: True / False
    # -------------------------------------------------------------------------------------------

    if debug:
        print("CALLED: is_year_folder(%s,%s)" % (src_fld, debug))

    match = re.search(r'(\d{4})', src_fld)  # Matching on a 4 digit year folder

    try:
        result = match.string
        if debug:
            print("%s is correctly named" % src_fld)
        return True

    except:

        # No match
        if debug:
            print("%s does not match the required pattern for a year folder" % src_fld)
        return False


def check_month_chars(month_cd, debug=0):
    # ------------------------------------------------------------------------------------------
    # Date: 20160306
    # Author: braidj@gmail.com
    # Purpose: Checks if month charachters are in allowable range
    # Output: True / False
    # -------------------------------------------------------------------------------------------

    valid_codes = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                   'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    if debug:
        print("CALLED: check_month_chars(%s,%s)" % (month_cd, debug))
        print("Checking month code %s" % month_cd)

    if month_cd in valid_codes:
        if debug:
            print("%s is valid month code" % month_cd)
        return True
    else:
        if debug:
            print("%s is not a valid month code, expect %s" %
                  (month_cd, valid_codes))
        return False


def check_month_nos(month_nos, debug=0):
    # ------------------------------------------------------------------------------------------
    # Date: 20160306
    # Author: braidj@gmail.com
    # Purpose: Checks if month digits are in allowable range
    # Output: True / False
    # -------------------------------------------------------------------------------------------

    valid_digits = ['01', '02', '03', '04', '05',
                    '06', '07', '08', '09', '10', '11', '12']

    if debug:
        print("CALLED: check_month_nos(%s,%s)" % (month_nos, debug))
        print("Checking month nos %s" % month_nos)

    if month_nos in valid_digits:
        if debug:
            print("%s is valid month digit" % month_nos)
        return True
    else:
        if debug:
            print("%s is not a valid month digit, expect %s" %
                  (month_nos, valid_digits))
        return False


def has_valid_parent(src_fld, debug=0):
    # ------------------------------------------------------------------------------------------
    # Date: 20160308
    # Author: braidj@gmail.com
    # Purpose: Checks if folder has a valid parent folder name, by checking the next folder up
    # Input: current or source folder. Valid parent is defined as either matching a dated
    # folder pattern or a year folder pattern.
    # Output: True / False
    # -------------------------------------------------------------------------------------------

    # TODO Add check it see if there is no parent folder

    if debug:
        print("CALLED: has_valid_parent(%s,%s)" % (src_fld, debug))
    parent_fld = get_folder_level(src_fld)
    is_valid = True
    success_msg = "%s has a valid named parent folder(%s)" % (
        src_fld, parent_fld)
    failure_msg = "%s does NOT have a valid named parent folder(%s)" % (
        src_fld, parent_fld)

    if is_dated_folder(parent_fld, debug) == True:
        if debug:
            print(success_msg)
        return True
    else:
        is_valid = False

    if is_year_folder(parent_fld, debug) == True:
        if debug:
            print(success_msg)
        return True
    else:
        is_valid = False

    if debug:
        print(failure_msg)
    return is_valid  # only get here if fail both above


def get_folder_level(path, level=2, debug=0):
    # ------------------------------------------------------------------------------------------
    # Date: 20150509
    # Author: braidj@gmail.com
    # Purpose: Extracts a folder name from a path, based on level. Defaults to level 2
    # which is the parent, e.g. c:/cat/kitten would return cat
    # Input: string path
    # Output: folder name
    # -------------------------------------------------------------------------------------------

    if debug:
        print("CALLED: get_folder_level(%s,%s,%s" % (path, level, debug))

    folders = path.split("\\")
    i = len(folders) - level  # extract by level desired
    result = folders[i]
    return result


def main():
    # Refactoring to use as a media tidy up script
    sample_target = r"\\Seagate-407BC6\Public\Photos\2000"
    #sample_target =r"\\DELL\Photos\2000"
    print("in progress")
    total_files = 0
    total_folders = 0

    print("Going to stop here")
    sys.exit(0)

    for top, folder, files in os.walk(sample_target):

        print("Folder %s contains %d files" % (top, len(files)))
        total_folders += 1
        total_files += len(files)

        for file in files:
            current_file = "%s%s%s" % (top, os.path.sep, file)
            print("image created : %s" %
                  time.ctime(os.path.getctime(current_file)))
            # print "Checking %s" %(current_file)

            filename, file_extension = os.path.splitext(file)
            # print "\t", filename, file_extension
            if file_extension in ('.ini', '.db'):
                file_to_delete = "%s%s%s" % (top, os.path.sep, file)
                print(file_to_delete)

                try:
                    os.remove(file_to_delete)

                except Exception as e:
                    s = str(e)
                    print("FAILED", s)

                else:
                    print(file_to_delete, "removed !")

    print("Completed for %d files in %d folders" %
          (total_files, total_folders))
    sys.exit(0)


def migrate_to_parent(child_fld, parent_fld, top):
    # ------------------------------------------------------------------------------------------
    # Date: 20150512
    # Author: braidj@gmail.com
    # Purpose: Move or merge an entire folder to a suitable parent
    # Input: tbc
    # Output: tbc
    # -------------------------------------------------------------------------------------------

    # Logic steps
    year_tag = str(parent_fld[-4:])
    print("migrating %s to be under %s\%s\%s\%s" %
          (child_fld, top, year_tag, parent_fld, child_fld))


def move_folder(source_fld):
    # ------------------------------------------------------------------------------------------
    # Date: 20150506
    # Author: braidj@gmail.com
    # Purpose: Move or merge an entire folder to a suitable parent
    # Input: tbc
    # Output: tbc
    # -------------------------------------------------------------------------------------------
    print("in progress")


def folder_sort_by_name(source_fld):
    # ------------------------------------------------------------------------------------------
    # Date: 20150428
    # Author: braidj@gmail.com
    # Purpose: Check folder name and move into appropriate parent year folder
    # Input: base folder, current folder being analysed
    # Output: Success / Failure
    # -------------------------------------------------------------------------------------------

    print("Function called on %s" % source_fld)

    for top, folders, files in os.walk(source_fld):

        print("got here 1")
        if len(folders) > 0:
            print("processing %d folder(s) under %s" % (len(folders), top))

        for fld in folders:

            if is_dated_folder(fld) == False:
                # is parent folder name valid ?
                full_path = os.path.join(top, fld)

                if has_valid_parent(full_path) == False:
                    print(fld)
                    new_parent = suggest_folder_name(full_path)
                    print("-Suggested parent name: %s" % new_parent)
                    migrate_to_parent(fld, new_parent, top)
                    print(top)
            else:
                print(fld, "ok")

            # year_portion = fld[-4:]
            # log(fld, False)
            #
            # try:
            # 	int(year_portion)
            # 	parent = os.path.join(base_fld, year_portion)
            # 	if (os.path.isdir(parent)) == False:
            # 		print "Will have to create %s" % parent
            # 		os.makedirs(parent)
            # 	else:
            # 		child = os.path.join(top, fld)
            #
            # 		#if (os.path.isdir(child)) == False:
            # 		print "move %s to %s" % (child, parent)
            # 		shutil.move(child, parent)
            #
            # except:
                # custom named folder, have to analyse contents
                #something = 1
            #suggest_folder_name(os.path.join(top, fld),base_fld)

            # Create year folder if required

            # Move folder and files


def suggest_folder_name(source_fld):
    # ------------------------------------------------------------------------------------------
    # Date: 20150501
    # Author: braidj@gmail.com
    # Purpose: Check date taken of all files to work out which folder it should move to
    # Input: source folder
    # Output: returns a suggested mmMMMYYYY date tag for folder contents
    # -------------------------------------------------------------------------------------------

    content_range = {}

    for top, folders, files in os.walk(source_fld):

        print("-Analysing %d images for their date taken" % len(files))

        for f in files:
            full_f = os.path.join(source_fld, f)
            date_tag = get_date_taken(full_f)

            try:
                content_range[date_tag] = content_range[date_tag] + 1
            except:
                content_range[date_tag] = 1

        if len(content_range) == 1:  # if all files have same data taken tag
            k = list(content_range.keys())

            if k[0] == "skip":  # unable to get date from any img file
                print("-Unable to decide folder name")
                return "CHECK_%s" % get_folder_level(top, 1)
            else:
                return k[0]
        else:
            return suggest_name_by_file(content_range)


def suggest_name_by_file(dict_tags):
    # ------------------------------------------------------------------------------------------
    # Date: 20150512
    # Author: braidj@gmail.com
    # Purpose: Suggests folder name by the date taken counts
    # Input: dictionary of date taken tags
    # Output: string, format MMMMMYYYY, examples 01JAN2015, 02FEB2015
    # -------------------------------------------------------------------------------------------
    print("SUGGEST NAME BY FILES")

    # Logic
    # Pick most used tag by count, unless skip
    # If more than one, randomly pick one, unless skip,
    # n.b. order indexes are added to dict is random

    max_count = 0
    suggested_tag = 'not_set'

    for key in dict_tags:
        print(key, dict_tags[key])

        if key != 'skip':
            if int(dict_tags[key]) > max_count:
                max_count = int(dict_tags[key])
                suggested_tag = key

    return suggested_tag


def get_date_taken(path, debug=0):
    # ------------------------------------------------------------------------------------------
    # Date: 20150426
    # Author: braidj@gmail.com
    # Purpose: Using time taken of image file returns folder name file should be stored under.
    # Input: file name
    # Output: string, format MMMMMYYYY, examples 01JAN2015, 02FEB2015
    # -------------------------------------------------------------------------------------------
    try:
        result = Image.open(path)._getexif()[36867]
    except:
        # log("",False)
        # log("Error: can not get date taken from image, skipping; most likely a scanned image")
        return "skip"

    try:
        fld_name = datetime.datetime.strptime(
            result, "%Y:%m:%d %H:%M:%S").strftime("%m%b%Y")
    except:
        log("Error: can not convert date taken TS")
        sys.exit(1)

    if debug > 0:
        print(result)
        print(fld_name)

    return fld_name


def process_files(target):
    # -------------------------------------------------------------------------------------------------------------------
    # Date: 20150426
    # Author: braidj@gmail.com
    # Purpose: Walks through all files of interest.
    # Input: Parent folder to walk through
    # Output:tbc
    # -------------------------------------------------------------------------------------------------------------------

    for top, folder, files in os.walk(target):
        # if len(files) > 0:
        if top == target:
            # print folder
            for file in files:
                if os.path.splitext(file)[1].upper() in photos:
                    fullpath = top + os.sep + file

                    recommended_fld = get_date_taken(fullpath)

                    if recommended_fld != "skip":

                        if fullpath != recommended_fld:
                            post_file(fullpath, recommended_fld)
                        # sys.exit(0)

                        # size = os.path.getsize(fullpath)
                        #results.add(size, fullpath)
        sys.exit(0)


def post_file(source_file, dest_folder):
    # Date: 20150426
    # Author: braidj@gmail.com
    # Purpose: Moves file(s) to destination folder
    # Inputs: 1) full file or list of full files 2) destination folder 3) current folder
    # Output: True or False

    # log("Processing %s" % source_file, False)
    top_fld, src_file = os.path.split(os.path.abspath(source_file))
    new_path = os.path.join(top_fld, dest_folder)

    if not os.path.exists(new_path):
        try:
            os.makedirs(new_path)
            log("", False)
            log("Created new folder %s" % new_path)
        except:
            log("ERROR: Fuck")

    dest_file = os.path.join(new_path, src_file)

    try:
        shutil.move(source_file, dest_file)
        log(".", False)
    except:
        log("ERROR: in function %s" % sys._getframe().f_code.co_name)
        log(sys.exc_info()[0], False)
        sys.exit(1)


def archive(tgt, dest=archive_folder):
    # handles lists or single files
    # Moves any duplicated file to a holding folder

    if isinstance(tgt, list):
        for file in tgt:
            arch = os.path.join(dest, os.path.basename(file))
            try:
                shutil.move(file, dest)
                print("archived %s to %s" % (file, dest))
            except:
                print("balls archive did n't work")
    else:

        arch = os.path.join(dest, os.path.basename(tgt))
        try:
            shutil.move(tgt, dest)
            print("archived %s to %s" % (tgt, dest))
        except:
            print("balls archive did n't work")


def check_list(files):
    # Converts all files in a list to md5, adds to a temp dict
    # then uses that to decide which ones are duplicates
    temp = {}

    for f in files:

        key = get_signature(f)

        if key in temp:  # key already exists, duplicate
            temp[key].append(f)
        else:  # fist time seen this key
            temp[key] = [f, ]

    # loop just through the duplicates
    for key in temp:
        if len(temp[key]) > 1:
            dupes = temp[key]
            nos_dupes = len(dupes) - 1
            print("duplicates are %d" % (nos_dupes))
            print(dupes[1:])
            archive(dupes[1:])


def extract_file_details(target, desc, file_ext=filter_by):
    # For the supplied root work down extracting out
    # all files, that match the file extension

    results = fileContainer(desc)  # create instance of class

    for top, folder, files in os.walk(target):
        if len(files) > 0:
            # print folder
            for file in files:
                if os.path.splitext(file)[1].upper() in file_ext:
                    fullpath = top + os.sep + file
                    size = os.path.getsize(fullpath)
                    results.add(size, fullpath)

    return results


def get_signature(file):
    # function performs md5 sum check on contents of file
    testFile = open(file, "rb")
    hash = hashlib.md5()

    while True:
        piece = testFile.read(1024)

        if piece:
            hash.update(piece)
        else:  # we're at end of file
            hex_hash = hash.hexdigest()
            return hex_hash
            break


def log(msg, with_ts=True):
    # -------------------------------------------------------------------------------
    # Author: braidj
    # Date: 20150415
    # Purpose: Adds timestamp to message for std out
    # Special processing on receivng a single dot, useful for not filling up a log
    # for an all day processing job.
    # -------------------------------------------------------------------------------

    if msg == ".":
        sys.stdout.write('.')  # useful for not filling log
    else:
        if with_ts:
            ts_line = "%s\t%s" % (get_ts(), msg)
        else:
            ts_line = msg

        print(ts_line)

    sys.stdout.flush()


def get_ts(with_space=True):
    # -------------------------------------------------------------------------------
    # Author: braidj
    # Date: 20141010
    # Purpose: Simply returns a useful formatted time stamp
    # Useful to have option of no spaces output, controlled by default param
    # -------------------------------------------------------------------------------
    t = time.localtime()

    if with_space:
        time_stamp = '%d-%02d-%02d %02d:%02d:%02d' % (
            t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    else:
        time_stamp = '%d%02d%02d_%02d%02d%02d' % (
            t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

    return time_stamp


class fileContainer(object):
    """ holds the results of a directory scan"""
    loadCount = 0  # tracks how many data loads have been processed
    combinedFileCount = 0
    combinedFiles = {}  # all loads merged

    def __init__(self, desc):
        self._container = {}
        self.nos_files = 0
        self.desc = desc
        fileContainer.loadCount += 1
        print("processing %s" % self.desc)

    def add(self, file_size, file_path):
        # update instance of files processed
        if str(file_size) in self._container:
            self._container[str(file_size)].append(file_path)
        else:
            self._container[str(file_size)] = [file_path, ]

        self.nos_files += 1

        # update class files processed
        if str(file_size) in fileContainer.combinedFiles:
            fileContainer.combinedFiles[str(file_size)].append(file_path)
        else:
            fileContainer.combinedFiles[str(file_size)] = [file_path, ]

        fileContainer.combinedFileCount += 1

    def print_files(self):
        '''prints out all file details'''
        for key in self._container:
            print(key, len(self._container[key]), self._container[key])

    def files(self, key=None):
        # return dict of all the files processed if no key supplied
        if key == None:
            return self._container
        else:
            return self._container[key]  # list of files

    def potentials(self):
        # Returns a list of any keys for the scan that have more than one
        # file in a byte size (key id)
        # Should only be run after scan completed

        potential_dupes = []
        for key in self._container:
            if len(self._container[key]) > 1:
                potential_dupes.append(key)

        if len(potential_dupes) > 0:
            print("Potential duplicates found within %s (%d)" %
                  (self.desc, len(potential_dupes)))
        else:
            print("No duplicates found within %s" % self.desc)

        return potential_dupes


if __name__ == '__main__':
    main()
