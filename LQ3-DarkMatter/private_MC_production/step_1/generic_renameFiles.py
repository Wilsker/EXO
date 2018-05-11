########################################
#       generic_renameFiles.py
########################################
#           Author: JTW
#           IHEP, CERN
########################################
#    Does what it says on the tin.
########################################


import glob, os

def rename(dir, pattern):
    for path_n_filename in glob.iglob(os.path.join(dir, pattern)):
        title, ext2 =os.path.splitext(os.path.basename(path_n_filename))
        name, ext1 = os.path.splitext(os.path.basename(title))
        newname = os.path.join(dir, name.rpartition('_slc6')[0])
        path_n_newname = newname + ext1 + ext2
        print 'newname = ' , path_n_newname
        os.rename(path_n_filename, path_n_newname)

full_path = '/afs/cern.ch/work/j/jthomasw/private/IHEP/EXO/CMSSW_9_4_0/src/genproductions/bin/MadGraph5_aMCatNLO'
search_filename_pattern = '*_gen3_slc6_amd64_gcc481_CMSSW_9_4_0_tarball.tar.xz'
rename(full_path, search_filename_pattern)
