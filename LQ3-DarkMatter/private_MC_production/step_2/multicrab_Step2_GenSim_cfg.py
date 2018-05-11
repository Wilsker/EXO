from WMCore.Configuration import Configuration

config = Configuration()
config.section_("General")
#config.General.requestName   = 'test_gen-sim_task' #task-dependent
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName    = 'GEN-SIM_cfg.py' #this is the config file you created with cmsDriver
config.JobType.maxJobRuntimeMin = 47 #Increased from default ~ 23 hours

config.section_("Data")
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1 #Suggests how many units (splitting is FileBased here so 1 unit = file) to include in each job.
config.Data.publication = True
config.Data.ignoreLocality = True # Allows one to run on any site regardless of where the dataset is. Requires whitelist with T2_*

# This string is used to construct the output dataset name
#config.Data.outputDatasetTag  = 'GEN-SIM' #something you like

dataset_name = 'GEN-SIM-v2'
print 'Dataset name = ' , dataset_name
config.Data.outputDatasetTag  = dataset_name

config.section_("Site")
# Where the output files will be transmitted to
config.Site.storageSite = 'T2_CN_Beijing'
config.Site.whitelist = ['T2_*'] # Required if want to use ignoreLocality option
#config.Site.blacklist = ['T2_CN_Beijing']
if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from optparse import OptionParser

    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.General.workArea = 'crab_projects-GEN-SIM-CMSSW_9_3_4-v2'

    def submit(config):
        parser=OptionParser()
        parser.add_option('-o', '--crabCmdOpts',
                          dest = 'crabCmdOpts',
                          default = '--dryrun',
                          help = "options for crab command CMD",
                          metavar = 'OPTS')
        (options, arguments) = parser.parse_args()
        print config

        try:
            #crabCommand('submit', config = config, *options.crabCmdOpts.split())
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################

    Sample=[['LQ800_DM_300_X_330','/DM_Codex_LQ800_DM_300_X_330/jthomasw-wmLHE-62e8c908700c91ef6aa76c64433eb866/USER']]

    '''Sample=[['LQ800_DM_300_X_330','/DM_Codex_LQ800_DM_300_X_330/jthomasw-wmLHE-62e8c908700c91ef6aa76c64433eb866/USER'],
        ['LQ900_DM_350_X_385','/DM_Codex_LQ900_DM_350_X_385/jthomasw-wmLHE-18a08332eee293e5b6ac029f0aec8b4d/USER'],
        ['LQ1000_DM_400_X_440','/DM_Codex_LQ1000_DM_400_X_440/jthomasw-wmLHE-2834776f875f21b1a2d9e807952be14c/USER'],
        ['LQ1100_DM_450_X_495','/DM_Codex_LQ1100_DM_450_X_495/jthomasw-wmLHE-94ce8bb8550e8699d0f28fba9970cfac/USER'],
        ['LQ1200_DM_500_X_550','/DM_Codex_LQ1200_DM_500_X_550/jthomasw-wmLHE-116bf7a8bbb827037722050a4c6a409c/USER'],
        ['LQ1300_DM_550_X_605','/DM_Codex_LQ1300_DM_550_X_605/jthomasw-wmLHE-ca555c0e0e694d7a851e53ae0896931f/USER'],
        ['LQ1500_DM_650_X_715','/DM_Codex_LQ1500_DM_650_X_715/jthomasw-wmLHE-9548264ecf197ad39d1a681a2ce1b68b/USER'],
        ['LQ1600_DM_700_X_770','/DM_Codex_LQ1600_DM_700_X_770/jthomasw-wmLHE-caf5e56411c7a1dca6df87d237a2ca5a/USER'],
        ['LQ1700_DM_750_X_825','/DM_Codex_LQ1700_DM_750_X_825/jthomasw-wmLHE-54477f04fcc55bfed741dc44e5dc2366/USER'],
        ['LQ1800_DM_800_X_880','/DM_Codex_LQ1800_DM_800_X_880/jthomasw-wmLHE-bd98af90f969574f89f0965c4bf69e77/USER'],
        ['LQ1400_DM_600_X_660','/DM_Codex_LQ1400_DM_600_X_660/jthomasw-wmLHE-3c8975b568015912aaddca8b0d513135/USER'],
        ['LQ1900_DM_850_X_935','/DM_Codex_LQ1900_DM_850_X_935/jthomasw-wmLHE-67edf01604865f2ac48be426d1bf0867/USER'],
        ['LQ2000_DM_900_X_990','/DM_Codex_LQ2000_DM_900_X_990/jthomasw-wmLHE-0b8cca44d0bcd31852ab01b6e58cdc41/USER'],
        ['LQ1000_DM_400_X_420','/DM_Codex_LQ1000_DM_400_X_420/jthomasw-wmLHE-7ac23be6e393861e1a3e57751850a329/USER'],
        ['LQ1100_DM_450_X_475','/DM_Codex_LQ1100_DM_450_X_475/jthomasw-wmLHE-a7b7933479e0dcf4ebc091fc984b7c9f/USER'],
        ['LQ1200_DM_500_X_525','/DM_Codex_LQ1200_DM_500_X_525/jthomasw-wmLHE-78f86acfae5973a5a31af66c4c069d34/USER'],
        ['LQ1300_DM_550_X_580','/DM_Codex_LQ1300_DM_550_X_580/jthomasw-wmLHE-fa3bc758f35c345620bdff11f319ee4f/USER'],
        ['LQ1400_DM_600_X_630','/DM_Codex_LQ1400_DM_600_X_630/jthomasw-wmLHE-1064bdc339e490da3ed2190ba35bd98b/USER'],
        ['LQ1500_DM_650_X_685','/DM_Codex_LQ1500_DM_650_X_685/jthomasw-wmLHE-aca3b082ae5804f2610664547e42e5a3/USER'],
        ['LQ1600_DM_700_X_735','/DM_Codex_LQ1600_DM_700_X_735/jthomasw-wmLHE-347aa29eaf5eaec4ac175111900bfd39/USER'],
        ['LQ1800_DM_800_X_840','/DM_Codex_LQ1800_DM_800_X_840/jthomasw-wmLHE-6a49200816b43293f24ab9b65b01830f/USER'],
        ['LQ1700_DM_750_X_790','/DM_Codex_LQ1700_DM_750_X_790/jthomasw-wmLHE-c23c000a793d61094d1a003cd0ec7501/USER'],
        ['LQ1000_DM_400_X_460','/DM_Codex_LQ1000_DM_400_X_460/jthomasw-wmLHE-b174f6c898daf7d49eb95252f0b4c4a8/USER'],
        ['LQ1200_DM_500_X_575','/DM_Codex_LQ1200_DM_500_X_575/jthomasw-wmLHE-706de9c1433a7a647c54937ee68f439c/USER'],
        ['LQ1300_DM_550_X_635','/DM_Codex_LQ1300_DM_550_X_635/jthomasw-wmLHE-09a7acb9ebb46de255a1cc97de4a1b12/USER'],
        ['LQ1400_DM_600_X_690','/DM_Codex_LQ1400_DM_600_X_690/jthomasw-wmLHE-85af49358bb98628371ac6ba405ebd49/USER'],
        ['LQ1900_DM_850_X_895','/DM_Codex_LQ1900_DM_850_X_895/jthomasw-wmLHE-08c7bcd6263b4305e0ff7419f6ffab96/USER'],
        ['LQ1100_DM_450_X_520','/DM_Codex_LQ1100_DM_450_X_520/jthomasw-wmLHE-72715cdd1f34c0287c271b6a80de3951/USER'],
        ['LQ1600_DM_700_X_805','/DM_Codex_LQ1600_DM_700_X_805/jthomasw-wmLHE-13a00bcafba14058adf4d662e3507daa/USER'],
        ['LQ1700_DM_750_X_865','/DM_Codex_LQ1700_DM_750_X_865/jthomasw-wmLHE-2355fe5530970346b739c45f0d7e9472/USER'],
        ['LQ1800_DM_800_X_920','/DM_Codex_LQ1800_DM_800_X_920/jthomasw-wmLHE-72e1a620d19c2d3e3431ed6745a07698/USER'],
        ['LQ1900_DM_850_X_975','/DM_Codex_LQ1900_DM_850_X_975/jthomasw-wmLHE-714a99904f76094f7adfaa60109d73e1/USER'],
        ['LQ1200_DM_600_X_600','/DM_Codex_LQ1200_DM_600_X_600/jthomasw-wmLHE-98c94a69989d8e3749e57b996ce425ce/USER'],
        ['LQ1300_DM_600_X_600','/DM_Codex_LQ1300_DM_600_X_600/jthomasw-wmLHE-036d45c33fb2d8e15660cb05f3d3febb/USER'],
        ['LQ1500_DM_600_X_600','/DM_Codex_LQ1500_DM_600_X_600/jthomasw-wmLHE-d4a6d273c0207a585f3177b27e223e1b/USER'],
        ['LQ1600_DM_600_X_600','/DM_Codex_LQ1600_DM_600_X_600/jthomasw-wmLHE-7dc847e4b97fa2e60bc4f22eb880581b/USER'],
        ['LQ1700_DM_600_X_600','/DM_Codex_LQ1700_DM_600_X_600/jthomasw-wmLHE-ce28765548c70d06051e3f7f41ce6259/USER'],
        ['LQ1500_DM_650_X_750','/DM_Codex_LQ1500_DM_650_X_750/jthomasw-wmLHE-14da528386258adab362fe44fa757ee9/USER'],
        ['LQ1800_DM_600_X_600','/DM_Codex_LQ1800_DM_600_X_600/jthomasw-wmLHE-c62f8eabba851c509f89fb0f979e100e/USER'],
        ['LQ1400_DM_600_X_600','/DM_Codex_LQ1400_DM_600_X_600/jthomasw-wmLHE-547565395962bfe0c36900bfc4b7c74d/USER']]'''


    #Older production
    '''Sample=[['LQ1000_DM_400_X_420','/DM_Codex_LQ1000_DM_400_X_420/jthomasw-wmLHE-8d2a815449a35f1ab84c6b0ef22d7800/USER'],
        ['LQ1000_DM_400_X_440','/DM_Codex_LQ1000_DM_400_X_440/jthomasw-wmLHE-a8bc45f439b3a94dfe492a296e7819e3/USER'],
        ['LQ1000_DM_400_X_460','/DM_Codex_LQ1000_DM_400_X_460/jthomasw-wmLHE-5b5f6c0d9175f88ab6facd7eadeb28fd/USER'],
        ['LQ1100_DM_450_X_475','/DM_Codex_LQ1100_DM_450_X_475/jthomasw-wmLHE-15231219cc7f083f886292e4a5344823/USER'],
        ['LQ1100_DM_450_X_495','/DM_Codex_LQ1100_DM_450_X_495/jthomasw-wmLHE-097ff54728adb3a7575a63636a925b2c/USER'],
        ['LQ1100_DM_450_X_520','/DM_Codex_LQ1100_DM_450_X_520/jthomasw-wmLHE-8df94cb36d2cddda4d6a91284124e825/USER'],
        ['LQ1200_DM_500_X_525','/DM_Codex_LQ1200_DM_500_X_525/jthomasw-wmLHE-38d4853df44c80189614972ce87e8e86/USER'],
        ['LQ1200_DM_500_X_550','/DM_Codex_LQ1200_DM_500_X_550/jthomasw-wmLHE-f019a3aa677dc0764b5d42a2bd106df2/USER'],
        ['LQ1200_DM_500_X_575','/DM_Codex_LQ1200_DM_500_X_575/jthomasw-wmLHE-5183ea5cc7e6ecac43f6e4167ef1c6f4/USER'],
        ['LQ1200_DM_600_X_600','/DM_Codex_LQ1200_DM_600_X_600/jthomasw-wmLHE-af60ff38a6bdf5c2158a3f890f6f655f/USER'],
        ['LQ1300_DM_550_X_580','/DM_Codex_LQ1300_DM_550_X_580/jthomasw-wmLHE-6e3b7e16c137da623294b7abc317e1ce/USER'],
        ['LQ1300_DM_550_X_605','/DM_Codex_LQ1300_DM_550_X_605/jthomasw-wmLHE-0ba0ba0618004a33ed4054e9b837f35e/USER'],
        ['LQ1300_DM_550_X_635','/DM_Codex_LQ1300_DM_550_X_635/jthomasw-wmLHE-6baf1f3b6d9a4b35b9685d63c504d3c2/USER'],
        ['LQ1300_DM_600_X_600','/DM_Codex_LQ1300_DM_600_X_600/jthomasw-wmLHE-9f756f4f7ad1bc8bba79597dec71b53d/USER'],
        ['LQ1400_DM_600_X_600','/DM_Codex_LQ1400_DM_600_X_600/jthomasw-wmLHE-ab084245e8b36837b968d71dc74e8c68/USER'],
        ['LQ1400_DM_600_X_630','/DM_Codex_LQ1400_DM_600_X_630/jthomasw-wmLHE-f43a6224a93dfdf66bbe07329358c6de/USER'],
        ['LQ1400_DM_600_X_660','/DM_Codex_LQ1400_DM_600_X_660/jthomasw-wmLHE-6c2742509bce596b6b7cb3ffd3385df7/USER'],
        ['LQ1400_DM_600_X_690','/DM_Codex_LQ1400_DM_600_X_690/jthomasw-wmLHE-0849115fb2a6ce2cd2fb52d81dbe101f/USER'],
        ['LQ1500_DM_600_X_600','/DM_Codex_LQ1500_DM_600_X_600/jthomasw-wmLHE-4c7b68cc0c68d399af21c3266d1141e0/USER'],
        ['LQ1500_DM_650_X_685','/DM_Codex_LQ1500_DM_650_X_685/jthomasw-wmLHE-2d1ca94cd06d8b0b945b4a8c8a9c3c24/USER'],
        ['LQ1500_DM_650_X_715','/DM_Codex_LQ1500_DM_650_X_715/jthomasw-wmLHE-6998477b94b3748c2c621433223a7b29/USER'],
        ['LQ1500_DM_650_X_750','/DM_Codex_LQ1500_DM_650_X_750/jthomasw-wmLHE-77983c63795b9a73d799cfd87bce628d/USER'],
        ['LQ1600_DM_600_X_600','/DM_Codex_LQ1600_DM_600_X_600/jthomasw-wmLHE-892547024c87bb1281fe70f5f8cab2ee/USER'],
        ['LQ1600_DM_700_X_735','/DM_Codex_LQ1600_DM_700_X_735/jthomasw-wmLHE-004bd28273efe7f35b3872388d0a0b98/USER'],
        ['LQ1600_DM_700_X_770','/DM_Codex_LQ1600_DM_700_X_770/jthomasw-wmLHE-24c34b5f77b91f4deba8dc7e5122e7a0/USER'],
        ['LQ1600_DM_700_X_805','/DM_Codex_LQ1600_DM_700_X_805/jthomasw-wmLHE-1bd7de35b9e5b8ffdc9e222ef1a54562/USER'],
        ['LQ1700_DM_600_X_600','/DM_Codex_LQ1700_DM_600_X_600/jthomasw-wmLHE-4adb6b9c51af6d421468d36b0efdd920/USER'],
        ['LQ1700_DM_750_X_790','/DM_Codex_LQ1700_DM_750_X_790/jthomasw-wmLHE-50ca55aa746aef805d6416f2569c54bf/USER'],
        ['LQ1700_DM_750_X_825','/DM_Codex_LQ1700_DM_750_X_825/jthomasw-wmLHE-c1b1048c08bd38da3791a9768ea0f1d2/USER'],
        ['LQ1700_DM_750_X_865','/DM_Codex_LQ1700_DM_750_X_865/jthomasw-wmLHE-efa477b984abee52856b8bf12131a6f5/USER'],
        ['LQ1800_DM_600_X_600','/DM_Codex_LQ1800_DM_600_X_600/jthomasw-wmLHE-4d82318018e148881882c3346c1acbce/USER'],
        ['LQ1800_DM_800_X_840','/DM_Codex_LQ1800_DM_800_X_840/jthomasw-wmLHE-44bee94032c92411795fe697aa288592/USER'],
        ['LQ1800_DM_800_X_880','/DM_Codex_LQ1800_DM_800_X_880/jthomasw-wmLHE-5878255c534c8464d550a31004af4a83/USER'],
        ['LQ1800_DM_800_X_920','/DM_Codex_LQ1800_DM_800_X_920/jthomasw-wmLHE-ee810375b672acee746f11f5cf0fa9c4/USER'],
        ['LQ1900_DM_850_X_895','/DM_Codex_LQ1900_DM_850_X_895/jthomasw-wmLHE-c10d859f35344524e88bc4bbe476ba83/USER'],
        ['LQ1900_DM_850_X_935','/DM_Codex_LQ1900_DM_850_X_935/jthomasw-wmLHE-bf505c9923959fb50e1140bcc4796538/USER'],
        ['LQ1900_DM_850_X_975','/DM_Codex_LQ1900_DM_850_X_975/jthomasw-wmLHE-50e93b087a63cd2e6d3cc1037af75dd7/USER'],
        ['LQ2000_DM_900_X_990','/DM_Codex_LQ2000_DM_900_X_990/jthomasw-wmLHE-3ee2e892e74da20e62ed3479cdca974c/USER'],
        ['LQ900_DM_350_X_385','/DM_Codex_LQ900_DM_350_X_385/jthomasw-wmLHE-5c7d9b58f8bbea0dd73741918a413629/USER']]'''


    for sam in Sample:
        task_dependant_name = 'DM_Codex_%s'%sam[0]
        config.General.requestName   = task_dependant_name
        config.Data.inputDataset = sam[1]
        print 'Submitting . . . . '
        submit(config)
