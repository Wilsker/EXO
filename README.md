#             NOTES
##     Joshuha Thomas-Wilsker,
##      IHEP Beijing, CERN

### Private Signal Sample Production
The procedure described here is an
attempt to assimilate all the steps
to produce a private MC sample.

The following steps are described:
1.) GridPack creation.
2.) LHE file creation.
3.) GEN-SIM step.
4.) MiniAOD files from LHE on PSI.

Step 1 Needs the gridpacks hence the first step is to generate said gridpacks as described beneath. Starting with a clean environment (i.e. steps up until GEN-SIM step do not need to be in a CMSSW src directory) then do:
```
git clone git@github.com:cms-sw/genproductions.git genproductions
cd genproductions/bin/MadGraph5_aMCatNLO/
```

You can copy scripts from here:
```
https://github.com/abdollah110/DarkMatter/tree/master/GridPack
https://cms-project-generators.web.cern.ch/cms-project-generators/?C=M;O=A
```

This, amongst other things will copy the model to your directory (DarkMatter_Codex.zip). In particular this will also copy across a 'Templates' directory which contains the templates:
  - 'customizecards.dat': Sets model parameters e.g. masses, couplings . . .
  - 'extramodels.dat': If non-SM Lagrangian is used it must be declared and uploaded to the generator web repository.
  - 'proc_card.dat': Declare processes to be generated (syntax: https://cp3.irmp.ucl.ac.be/projects/madgraph/wiki/InputEx).
  - 'run_card.dat': Declare options on how generator will run and generate the process + specific kinematic cuts.

### Single gridpack creation
First I describe how to generate a single gridpack. This process is then parallelised and run on the grid. The 'dirGenerator_gridpack.py' script which should perform the steps as described on the twiki: 'https://twiki.cern.ch/twiki/bin/view/CMS/QuickGuideMadGraph5aMCatNLO'
```
python dirGenerator_gridpack.py
```
This will make the directories for all mass points, copy the Madgraph cards in corresponding directories and create script (create_submit_gridpack_generation.sh) to create the gridpacks using lxbatch. The following command allows one can run a sample locally and ensure the gridpack production runs ok. The command is taken from
create_submit_gridpack_generation.sh:
```
./gridpack_generation.sh Codex_LQ1100_DM_450_X_520_gen2 cards/production/13TeV/DarkMatter_Codex/Codex_LQ1100_DM_450_X_520_gen2
```
If this command runs ok, one should try making some LHE files locally to ensure everything is ok.

### LHE file creation
```
tar -xavf <path of gridpack creation>/XXX.tar.xz
./runcmsgrid.sh <NEvents> <RandomSeed> <NumberOfCPUs>
```

- NEvents = number of events
- seed = seed number used for event generation.
- nCPU = number of CPUs used for the computation.

Final LHE file should be in 'genproductions/bin/MadGraph5_aMCatNLO/' with filename: 'cmsgrid_final.lhe'

### Gridpack creation
If everything above ran ok one can create the remainder of the gridpacks, one can either run locally using the 'create_gridpack_generation.py' script. Two alternative options (not used here) are beneath: One could run the 'toSubmit_Codex_LQ_DM_X_gen3.sh' scripts to run the same commands but can be sent off remotely. You also have e.g. submit_cmsconnect_gridpack_generation.sh scripts that provide alternative run options.

### Step 1: wmLHE creation

This step needs the gridpacks generated above along with the multicrab_Step1_GridPackToLHE.py, the relevant wmLHE_XXXXX_cfg.py configs and the multicrab_step1 submission config. We need to set up a CMSSW environment. 'http://cms-sw.github.io/latestIBs.html' - Latest integration build webpage. Info on which scram arch to use for the latest IB's. Can use 'scram list' to see which CMSSW version are available for a given scram arch.
```
export SCRAM_ARCH="slc6_amd64_gcc630"
```
I ended up using 'CMSSW_9_3_4' because that was what was used in the 'Fall2017' production.
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH="slc6_amd64_gcc630"
export CMSSW_VERSION="CMSSW_9_3_4"
cmsrel $CMSSW_VERSION
cd $CMSSW_VERSION/src
scram b -j 3
```

The jobs were submitted from '/afs/cern.ch/work/j/jthomasw/private/IHEP/EXO/CMSSW_9_3_4/src/step_1/' directory.

- Copy gridpack tarballs (Code_####tar.xz) here from genproduction directory. In this case, the gridpacks were generated from:
  /afs/cern.ch/work/j/jthomasw/private/IHEP/EXO/genproductions/bin/MadGraph5_aMCatNLO/
  but copied from:
  /afs/cern.ch/work/j/jthomasw/private/IHEP/EXO/CMSSW_9_3_4/src/step_1/
- Used generic_open_n_edit_template.py script to copy wmLHE template and create new file for each mass point (simply changing name and gridpack used in wmLHE script).
  Note that the wmLHE template is specific to MonoLQ analyses. Can be generated using cmsDriver command at top of script.
- Edit multicrab_step1 config options: outLFNDirBase, storageSite, Sample list, inputFiles, psetName and outputPrimaryDataset as they are analysis/filename specific.


NOTE: I also wrote a generic script to rename .tar files 'generic_renameFiles.py' in case this is needed.
```
python multicrab_Step1_GridPackToLHE.py
```
Can find output files on IHEP nodes by ls-ing:
```
ls /pnfs/ihep.ac.cn/data/cms/store/user/jthomasw/Codex_Gridpack/
```

### Step 2: GEN-SIM creation
This step makes the 'GEN-SIM' from the wmLHE published samples. This step also requires a GEN-SIM_cfg.py. For this step your working directory should be the same CMSSW work area that was used to create the LHE files.

Useful link:
```
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookGeneration#PythiaHZZmumuSampleCfg
```

Creating the GEN-SIM_cfg.py requires the fragment code which depends on the analysis and signal model. You can find the information for the fragments used for a samples production during a given campaign in McM (circle icon with cross in the middle).

For the Mono-LQ3 analysis we use Madgraph:
```
https://github.com/cms-sw/genproductions/blob/master/python/ThirteenTeV/Hadronizer/Hadronizer_TuneCP5_13TeV_generic_LHE_pythia8_cff.py
```
To use the fragment, you need to make a directory called "Configuration", cd into that directory and checkout the genproduction repo. I forked the genproduction package in my private gitHub repository first then cloned it locally so I can track edits to the official repo while maintaining my own edits.
```
git clone https://Wilsker@github.com/cms-sw/genproductions.git GenProduction
```

This is not part of CMSSW so you need to change back into CMSSW/src and recompile. One can then run the command beneath to generate a GEN-SIM_cfg.py. Note, one can look up the newest campaign in McM to find out the most recent cmsDriver command.
```
cmsDriver.py Configuration/GenProduction/python/ThirteenTeV/Hadronizer/Hadronizer_TuneCP5_13TeV_generic_LHE_pythia8_cff.py --filein file:LHE.root --fileout file:GEN-SIM.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 93X_mc2017_realistic_v3 --beamspot Realistic25ns13TeVEarly2017Collision --step GEN,SIM --nThreads 8 --geometry DB:Extended --era Run2_2017 --python_filename GEN-SIM_cfg.py --customise Configuration/DataProcessing/Utils.addMonitoring --no_exec -n 10
```
Based on the following that was used for the Fall 2017 production:
```
'https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/TOP-RunIIFall17wmLHEGS-00001'
```
which contains the following options.

For 2016 data:
```
cmsDriver.py Configuration/GenProduction/python/ThirteenTeV/Hadronizer/Hadronizer_TuneCUETP8M1_13TeV_generic_LHE_pythia8_cff.py --filein file:LHE.root --fileout file:GEN-SIM.root --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step GEN,SIM --magField 38T_PostLS1 -n 10 --python_filename GEN-SIM_cfg.py --no_exec
```
Taken from here:
```
https://share.nuclino.com/p/topDM-private-production-RYyDP8h8hkgk1ZAAyh4K1H
```
Note, the importance of the '--no_exec' option which means the driver command generates the cfg but doesn't attempt to run it. The GEN-SIM python script that is generated is necessary as it is the pset for the multicrab2 config.

!WARNING!
You need to change the 'fileNames' in GEN-SIM_cfg.py:
```
fileNames = cms.untracked.vstring('file:LHE.root')
```
You can use the LFN's of the files you generated in step1 to replace 'file:LHE.root' as the default. In this case you can find a file on the IHEP farm (Beijing T2 farm defined output for step1). Just log onto any IHEP node and do:
```
ls /pnfs/ihep.ac.cn/data/cms/store/user/jthomasw/Codex_Gridpack/.....
```

For the filename replacement you only need to use the name after '/pnfs/ihep.ac.cn/data/cms'. For example: /store/user/jthomasw/Codex_Gridpack/DM_Codex_LQ1000_DM_400_X_420/wmLHE/171122_115457/0000/wmLHE_1.root You can test the 'fragment' code locally using the cmsRun executable:
```
cmsRun GEN-SIM_cfg.py
```
The multicrab2 script will use the GEN-SIM pset and run on the grid via crab. This multicrab2 needs altering:

1.) Change storage site (T2_CN_Beijing).
2.) General.workArea (crab_projects-GEN-SIM-vX).
3.) Samples for inputDataset needs to resemble the output dataset names from Step1.

Using inputsDataset published on DBS. Dataset names in DBS are as follows:
```
/<primary-dataset>/<CERN-username_or_groupname>-<publication-name>-<pset-hash>/USER

example: /DM_Codex_LQ800_DM_300_X_330/jthomasw-wmLHE-<pset-hash>/USER
```

- lfn-prefix = crab config Data.outLFN
- primary-dataset = crab config Data.outputPrimaryDataset
- publication-name	 = crab config  Data.outputDatasetTag
- time-stamp	= A timestamp, based on when the task was submitted. A task submitted at 17:38:49 on 27 April 2014 would result in a timestamp of 140427_173849.
- counter = A four-digit counter, used to prevent more than 1000 files residing in the same directory.
- file-name	= crab config JobType.outputFiles.
- pset-hash = hash produced from the CMSSW code used by the cmsRun job.

One can get the pset-hash (and the full output name one needs for the step2 multicrab config) by simply running the command:
```
crab status -d <crab-job-dir>
```
and it will appear in the 'Output dataset'. Can use 'crab_manager.py' script to loop over all job dirs from step 1 and get status'.

Before submitting any jobs, you should figure out how to split your jobs up on crab. This can be done by using the genius '--dryrun' option with the crab 'submit' command. Instead of submitting your jobs to the grid, this will write the splitting results to a splitting summary .json file. It will then create an tarball containing the splitting summary .json and all files neccessary to run the job and upload this to the crab user file cache. The crab client will then download this file, unpack it in a temp directory and run a mini test job over a few events on the users local machine. When the job is finished, the crab client prints out a summary with the results of the splitting and the expected performance of the job e.g. memory consumption, job runtime etc.

Multicrab script can be run using the following command:
```
python multicrab_Step2_GenSim_cfg.py
```
Output files can be found on the Beijing T2 farm @ e.g. /pnfs/ihep.ac.cn/data/cms/store/user/jthomasw/DM_Codex_LQ1000_DM_400_X_420/GEN-SIM/

### Step 3: DIGI-RECO-1 creation

Following commands in DIGI-RECO section of webpage:
```
https://share.nuclino.com/p/topDM-private-production-RYyDP8h8hkgk1ZAAyh4K1H
```
This step was run in cmssw working directory: /afs/cern.ch/work/j/jthomasw/private/IHEP/EXO/CMSSW_8_0_21/src/step_3/

### DIGI-RECO: Step 1

Creates DIGI-RECO-1 from GEN-SIM root files. This step requires the multicrab_Step3_DR1_cfg.py
python script along with the DIGI-RECO_1_cfg.py script. The DIGI-RECO_1_cfg.py script can be
generated using a cmsDriver command.

```
cmsDriver.py step1 --filein file:GEN-SIM.root --fileout file:DIGI-RECO_step1.root --pileup_input filelist:/afs/cern.ch/work/j/jthomasw/private/IHEP/EXO/CMSSW_8_0_21/src/step_3/pileup_filelist.txt --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 --nThreads 4 --datamix PreMix --era Run2_2016 --python_filename DIGI-RECO_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1
```
May need to remove line from RECO_1_cfg.py:
```
process.options.numberOfThreads=cms.untracked.uint32(4)
```
It is advised to test the config locally before running lots of jobs on the grid. Before testing the python config DIGI-RECO_1_cfg.py it must be edited so default input filename is valid e.g. change line in config to:
```
fileNames = cms.untracked.vstring('/store/user/jthomasw/DM_Codex_LQ1000_DM_400_X_420/GEN-SIM-CMSSW_7_1_20_patch3_v1/171218_170902/0000/GEN-SIM_100.root'),
```

Now try running:
```
cmsRun DIGI-RECO_1_cfg.py
```

This command uses a local list of pileup files specified in the text files:
```
/afs/cern.ch/work/j/jthomasw/private/IHEP/EXO/CMSSW_8_0_21/src/step_3/pileup_filelist.txt
```
This list is a copy of the text file:
```
/afs/cern.ch/user/d/dpinna/public/gridpacks/pileup_filelist.txt
```

Check multicrab parameters:
1.) Change storage site (T2_CN_Beijing).
2.) General.workArea (crab_projects-GEN-SIM-vX).
3.) Samples for inputDataset needs to resemble the output dataset names from Step2.
4.) Ensure the correct samples are listed in multicrab_Step3_DR1_cfg.py, the storageSite is set correctly and add the following lines:
    `config.Data.ignoreLocality = True` which allows one to run on any site regardless of where the dataset is. Requires whitelist with T2_*
    `config.Site.whitelist = ['T2_*']` which is required if want to use ignoreLocality option

Run multicrab_Step3_DR1_cfg.py to submit to grid:
```
python multicrab_Step3_DR1_cfg.py
```

### DIGI-RECO: Step 2

Generate cmssw config using cmsDriver command:
```
cmsDriver.py step2 --filein file:DIGI-RECO_step1.root --fileout file:DIGI-RECO_step2.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RAW2DIGI,RECO,EI --nThreads 4 --era Run2_2016 --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --python_filename DIGI-RECO_2_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1
```
Follow steps above again for this file but ensure the fileNames parameter is set to output from previous step.

Check multicrab parameters:
1.) Change storage site (T2_CN_Beijing).
2.) General.workArea (crab_projects-GEN-SIM-vX).
3.) Samples for inputDataset needs to resemble the output dataset names from Step3 part 1.
4.) Ensure the correct samples are listed in multicrab_Step3_DR1_cfg.py, the storageSite is set correctly and add the following lines:
    `config.Data.ignoreLocality = True` which allows one to run on any site regardless of where the dataset is. Requires whitelist with T2_*
    `config.Site.whitelist = ['T2_*']` which is required if want to use ignoreLocality option

Run multicrab command:
```
python multicrab_Step3_DR2_cfg.py
```

### Step 4: MINIAODSIM creation

Create cmssw config using cmsDriver command:
```
cmsDriver.py step1 --filein file:DIGI-RECO.root --fileout file:MiniAODv2.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step PAT --nThreads 4 --era Run2_2016 --python_filename MiniAODv2_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1
```

### Post-production
First step after post production is to copy files from the T2 node to the T3 node as requested by the IHEP farm management. Files copied from T2 node:
```
/pnfs/ihep.ac.cn/data/cms/store/user/jthomasw/
```
Into T3 directory:
```
/publicfs/cms/user/joshuha/Exotics/mc/
```
Using the code in:
```
/afs/ihep.ac.cn/users/j/joshuha/Exotics/download_2018
```

### MiniAOD to Analysis Ntuple
We now want to convert our MiniAOD into format suitable for interactive analysis via a method called ntupling. We can do this using the BSMFramework developed by the IHEP CMS team. We first need to install the CMSSW software and create the CMSSW environment. To do this we used the following commands:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH="slc6_amd64_gcc630"
cmsrel CMSSW_9_4_2
cd CMSSW_9_4_2/src/
cmsenv
git cms-init
git cms-merge-topic guitargeek:ElectronID_MVA2017_940pre3
git clone https://github.com/BinghuanLi/BSMMaker.git
cp /afs/cern.ch/user/b/binghuan/public/4Joshua/runTauIdMVA.py /afs/cern.ch/work/j/jthomasw/private/IHEP/EXO/CMSSW_9_4_2/src/BSMMaker/BSM3G_TNT_Maker/python/
scram b -j 10
```



###########################
# Grid/CRAB Advice
###########################

In case one wants to retrieve some output ROOT files of a task, one can do so with the following CRAB command:

$>crab getoutput --dir=crab_projects-GEN-SIM-v5/crab_DM_Codex_LQ1200_DM_500_X_550

The files are copied into the results subdirectory of the corresponding CRAB project directory. To get the logs files
one can run e.g.:

$> crab getlog --dir=crab_projects-GEN-SIM-v5/crab_DM_Codex_LQ1200_DM_500_X_550 --jobids=44

The log files (assembled in zipped tarballs) are copied into the results subdirectory of the corresponding CRAB
project directory. To unzip and extract the log files, one can use the command tar -zxvf'



MONITORING PRODUCTION:
- Important to note that the dashboard monitoring is updated when it receives UPD packets from the services monitoring the jobs.
  These packets can sometimes be lost in which case the dashboard will not be updated.
- One should always cross-check a jobs status using e.g. 'crab status' especially if you see some unusual behaviour.

Are jobs taking too long / failing due to too much wall time?
  - Estimate the number of events you want to run, the time taken per event and the time you want the job to run in.
  - Check config.Data.unitsPerJob parameter in multicrab script.
  - unitsPerJob should be set to = desiredTime / (<time per event> * <number of events>)


Wrote script to kill/get status of all crab jobs in given crab working directory. Usage e.g.:

  $> python crab_manager.py -d crab_projects-GEN-SIM-v1 -o (resubmit,kill,status)

At the end of the for an given directory you can see e.g.

['finished', '<job_number>']
['failed', '<job_number>']

If the job failed, you may want to use the above getlog command for the failed job_number to understand why the job failed.
Also try using the --long option in the crab status command.


#########################
# Bash scripting
#########################

Find subdirectories and list in files:
find /pnfs/ihep.ac.cn/data/cms/store/user/jthomasw/*/MiniAODv2/*/* -maxdepth 0 > test.txt



#########################
# Working on IHEP nodes
#########################

Editing any code can be difficult (slow, bad tools etc.).
Would suggest editing scripts on lxplus node and scp edited files to IHEP in order to run.


### For copying to lxplus
Files copied to work are on lxplus:
> /afs/cern.ch/work/j/jthomasw/private/IHEP/EXO/MiniAOD

Using script:
> /afs/cern.ch/work/j/jthomasw/private/IHEP/EXO/MiniAOD/xrdcp_script_private_production.py
