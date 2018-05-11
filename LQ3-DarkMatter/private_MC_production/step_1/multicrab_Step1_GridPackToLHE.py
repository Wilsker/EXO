from WMCore.Configuration import Configuration

config = Configuration()
config.section_("General")
#config.General.requestName   = 'DM_Codex_1800_600_600' #task-dependent
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName  = 'PrivateMC'
#config.JobType.inputFiles = ['Codex_LQ1800_DM_600_X_600_gen2_tarball.tar.xz']
#config.JobType.psetName    = 'wmLHE_DM_LQ_1000_400_440_cfg.py' #this is the config file you created with cmsDriver

config.section_("Data")
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 500 #task-dependent - set up to make just one output file
config.Data.totalUnits  = 50000 #task-dependent
config.Data.publication = True
config.Data.outLFNDirBase = '/store/user/jthomasw/Codex_Gridpack_CMSSW_9_3_4/'

# These strings are used to construct the output dataset name
config.Data.outputDatasetTag  = 'wmLHE' #something you like
#config.Data.outputPrimaryDataset  = 'DM_Codex_1000_400_440' #this is the dataset name that all tiers will have.  e.g. VBFHToBB_M-125_13TeV_powheg_pythia8

config.section_("Site")
config.Site.storageSite = 'T2_CN_Beijing' # Where the output files will be transmitted to



if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.General.workArea = 'crab_projects3'

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################
    #Sample=['LQ800_DM_300_X_330']
    Sample=[#'LQ800_DM_300_X_330',
            #'LQ900_DM_350_X_385',#
            #'LQ1000_DM_400_X_440',#
            #'LQ1100_DM_450_X_495',#
            #'LQ1200_DM_500_X_550',#
            #'LQ1300_DM_550_X_605',#
            #'LQ1500_DM_650_X_715',#
            #'LQ1600_DM_700_X_770',#
            #'LQ1700_DM_750_X_825',#
            #'LQ1800_DM_800_X_880',#
            #'LQ1400_DM_600_X_660',#
            #'LQ1900_DM_850_X_935',#
            #'LQ2000_DM_900_X_990',#
            #'LQ1000_DM_400_X_420',#
            #'LQ1100_DM_450_X_475',#
            #'LQ1200_DM_500_X_525',#
            #'LQ1300_DM_550_X_580',#
            #'LQ1400_DM_600_X_630',#
            'LQ1500_DM_650_X_685',
            'LQ1600_DM_700_X_735',
            'LQ1800_DM_800_X_840',
            'LQ1700_DM_750_X_790',
            'LQ1000_DM_400_X_460',
            'LQ1200_DM_500_X_575',
            'LQ1300_DM_550_X_635',
            'LQ1400_DM_600_X_690',
            'LQ1900_DM_850_X_895',
            'LQ1100_DM_450_X_520',
            'LQ1600_DM_700_X_805',
            'LQ1700_DM_750_X_865',
            'LQ1800_DM_800_X_920',
            'LQ1900_DM_850_X_975',
            'LQ1200_DM_600_X_600',
            'LQ1300_DM_600_X_600',
            'LQ1500_DM_600_X_600',
            'LQ1600_DM_600_X_600',
            'LQ1700_DM_600_X_600',
            'LQ1500_DM_650_X_750',
            'LQ1800_DM_600_X_600',
            'LQ1400_DM_600_X_600']


    for sam in Sample:
        config.General.requestName   = 'DM_Codex_%s'%sam #task-dependent
        config.JobType.inputFiles = ['Codex_%s_gen3.tar.xz'%sam]
        config.JobType.psetName    = 'wmLHE_%s_cfg.py'%sam #this is the config file you created with cmsDriver
        config.Data.outputPrimaryDataset  = 'DM_Codex_%s'%sam #this is the dataset name that all tiers will have.  e.g. VBFHToBB_M-125_13TeV_powheg_pythia8
        submit(config)

'''
    config.General.requestName   = 'DM_Codex_1600_700_770' #task-dependent
    config.JobType.inputFiles = ['Codex_LQ1600_DM_700_X_770_gen2_tarball.tar.xz']
    config.JobType.psetName    = 'wmLHE_DM_LQ_1200_500_550_cfg.py' #this is the config file you created with cmsDriver
    config.Data.outputPrimaryDataset  = 'DM_Codex_1200_500_550' #this is the dataset name that all tiers will have.  e.g. VBFHToBB_M-125_13TeV_powheg_pythia8
    submit(config)
'''
