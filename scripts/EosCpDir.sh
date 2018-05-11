#!/bin/bash
#Relocate CRAB outputs to improve directory structure.
#=========================================
#CRAB output
#lnfpath=/store/group/phys_btag/Commissioning/TTbar/JTWcrab_CMSSW8026_v4/
lnfpath=/store/group/phys_btag/Commissioning/TTbar/Jan052017/7c84d07/

#New dir
#newlfnpath=/store/group/phys_btag/Commissioning/TTbar/JTW_KIN_CMSSW8026_v4/
newlfnpath=/store/group/phys_btag/Commissioning/TTbar/KinMethod_StructuredDir_08Jan2017/

#CRAB output dataset titles.
datasets=(
"
TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8
"
#TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8
#TTToHadronic_TuneCP5_13TeV-powheg-pythia8
#TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8
#ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8
#ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8
#TT_TuneCUETP8M2T4_13TeV-powheg-fsrdown-pythia8
#TT_TuneCUETP8M2T4_13TeV-powheg-fsrup-pythia8
#TT_TuneCUETP8M2T4_13TeV-powheg-isrdown-pythia8
#TT_TuneCUETP8M2T4_13TeV-powheg-isrup-pythia8
#TT_TuneCUETP8M2T4_mtop1695_13TeV-powheg-pythia8
#TT_TuneCUETP8M2T4_mtop1755_13TeV-powheg-pythia8
#TT_TuneCUETP8M2T4down_13TeV-powheg-pythia8
#TT_TuneCUETP8M2T4up_13TeV-powheg-pythia8
)

#Dataset titles for new directory structure.
newdatasets=(
#MC13TeV_ST_TW_antitop
#MC13TeV_ST_TW_top
MC13TeV_TTJets_DL
#MC13TeV_TTJets_AH
#MC13TeV_TTJets_SL
#MC13TeV_TTJets_fsrdown
#MC13TeV_TTJets_fsrup
#MC13TeV_TTJets_isrdown
#MC13TeV_TTJets_isrup
#MC13TeV_TTJets_m169v5
#MC13TeV_TTJets_m175v5
#MC13TeV_TTJets_CUETP8M2T4down
#MC13TeV_TTJets_CUETP8M2T4up
)

pos=0
for d in $datasets; do
 dataset=$d #${datasets[$pos]}
 newdataset=${newdatasets[$pos]}
 #Create new folder place
 eos rm -r $newlfnpath$newdataset
 xrd eoscms mkdir $newlfnpath$newdataset

 #Get full path
 echo 'Add path to directory:'
 echo 'Path:'
 echo $lnfpath$dataset
 echo 'Files:'
 eos ls $lnfpath$dataset
 eos ls $lnfpath$dataset > temp.txt

 newfolder1=`cat temp.txt`
 echo 'Add newfolder1 to directory:'
 echo 'Path:'
 echo $lnfpath$dataset/$newfolder1
 echo 'Files:'
 eos ls $lnfpath$dataset/$newfolder1
 eos ls $lnfpath$dataset/$newfolder1 > temp.txt

 newfolder2=`cat temp.txt`
 echo 'Add newfolder2 to directory:'
 echo 'Path:'
 echo $lnfpath$dataset/$newfolder1/$newfolder2
 echo 'Files:'
 eos ls $lnfpath$dataset/$newfolder1/$newfolder2
 eos ls $lnfpath$dataset/$newfolder1/$newfolder2 > temp.txt
 subfolds=`cat temp.txt`

 #Get files
 for sf in $subfolds; do
  eos ls $lnfpath$dataset/$newfolder1/$newfolder2/$sf > temp.txt
  files=`cat temp.txt | sed -e "s/.*\///" | grep root | awk '{ print $NF }'`
  #Copy files
  for f in $files; do
    echo 'cp file:'
    echo $lnfpath$dataset/$newfolder1/$newfolder2/$sf/$f
    echo 'into:'
    echo $newlfnpath$newdataset/$f
    xrd eoscms cp $lnfpath$dataset/$newfolder1/$newfolder2/$sf/$f $newlfnpath$newdataset/$f
  done
 done
 let pos=pos+1
done
