#!/bin/bash


#=========================================
#Relocate CRAB outputs to improve directory structure.
#=========================================

#CRAB output
#lnfpath=/store/group/phys_btag/Commissioning/TTbar/JTWcrab_CMSSW8026_v3/
lnfpath=/store/group/phys_btag/Commissioning/TTbar/Jan052017/7c84d07/
#Directory for new structure.
#newlfnpath=/store/group/phys_btag/Commissioning/TTbar/JTW_KIN_CMSSW8026_v3/
newlfnpath=/store/group/phys_btag/Commissioning/TTbar/KinMethod_StructuredDir_08Jan2017/
datasets=(
MuonEG
)

pos=0
for d in $datasets; do

  dataset=${datasets[$pos]}

  #Get full path
  eos ls $lnfpath$dataset > temp.txt
  eos ls $lnfpath$dataset/ > multicrab_temps.txt

  multicrabsubfolds=`cat multicrab_temps.txt`

  for rf in $multicrabsubfolds; do

    # Can avoid copying all directories by blacklisting here.
    if [[ $rf == *"crab_Data13TeV_MuonEG_2017B_Prompt"* ]]; then
      continue
    fi
    if [[ $rf == *"crab_Data13TeV_MuonEG_2017C1_Prompt"* ]]; then
      continue
    fi
    if [[ $rf == *"crab_Data13TeV_MuonEG_2017C2_Prompt"* ]]; then
      continue
    fi
    if [[ $rf == *"crab_Data13TeV_MuonEG_2017C3_Prompt"* ]]; then
      continue
    fi
    if [[ $rf == *"crab_Data13TeV_MuonEG_2017D_Prompt"* ]]; then
      continue
    fi
    if [[ $rf == *"crab_Data13TeV_MuonEG_2017E_Prompt"* ]]; then
      continue
    fi
    if [[ $rf == *"crab_Data13TeV_MuonEG_2017F_Prompt"* ]]; then
      continue
    fi

    if [[ $rf == *"crab_Data13TeV_MuonEG_2017B_Nov17"* ]]; then
      continue
    fi
    if [[ $rf == *"crab_Data13TeV_MuonEG_2017D_Nov17"* ]]; then
      continue
    fi
    if [[ $rf == *"crab_Data13TeV_MuonEG_2017E_Nov17"* ]]; then
      continue
    fi
    

    # ===== Create new folder place =====
    #eos rm -r $newlfnpath$rf
    #xrd eoscms mkdir $newlfnpath$rf

    eos ls $lnfpath$dataset/$rf > temp.txt
    eos ls $lnfpath$dataset/$rf > multicrab_temps2.txt
    multicrabsubfolds_2=`cat multicrab_temps2.txt`

    for tf in $multicrabsubfolds_2; do
      eos ls $lnfpath$dataset/$rf/$tf > temp.txt
      subfolds=`cat temp.txt`

      #Get files
      for sf in $subfolds; do
        eos ls $lnfpath$dataset/$rf/$tf/$sf >temp.txt
        subsubfolds=`cat temp.txt`
        files=`cat temp.txt | sed -e "s/.*\///" | grep root | awk '{ print $NF }'`

        if [[ $sf == *"failed"* ]]; then
          echo "Don't want this file"
          continue
          fi
          counter=0
          #Copy files
          for f in $files; do
            #if [ $counter -gt 0 ];
            #then
            #  continue
            #  fi
            #let "counter += 1"
            if [ -e "$newlfnpath/$rf/$f" ]
            then
              echo 'File already exists!'
              continue
            else
              echo 'cp files from:'
              echo $lnfpath$dataset/$rf/$tf/$sf/$f
              echo ' into: '
              echo $newlfnpath/$rf/$f
              xrd eoscms cp $lnfpath$dataset/$rf/$tf/$sf/$f $newlfnpath/$rf/$f
              fi
            done
          done
        done
        let pos=pos+1
      done
    done
