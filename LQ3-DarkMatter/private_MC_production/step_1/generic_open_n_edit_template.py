import os, shutil

mass_point_list=['LQ800_DM_300_X_330',
                'LQ900_DM_350_X_385',
                'LQ1000_DM_400_X_440',
                'LQ1100_DM_450_X_495',
                'LQ1200_DM_500_X_550',
                'LQ1300_DM_550_X_605',
                'LQ1500_DM_650_X_715',
                'LQ1600_DM_700_X_770',
                'LQ1700_DM_750_X_825',
                'LQ1800_DM_800_X_880',
                'LQ1400_DM_600_X_660',
                'LQ1900_DM_850_X_935',
                'LQ2000_DM_900_X_990',
                'LQ1000_DM_400_X_420',
                'LQ1100_DM_450_X_475',
                'LQ1200_DM_500_X_525',
                'LQ1300_DM_550_X_580',
                'LQ1400_DM_600_X_630',
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
                'LQ1400_DM_600_X_600'
]

full_path = '/afs/cern.ch/work/j/jthomasw/private/IHEP/EXO/CMSSW_9_3_4/src/step_1/'
template_file = 'wmLHE_DM_LQ_template_cfg.py'
os.path.join(full_path,template_file)
print 'Template file = ' , template_file
for masspoint in mass_point_list:

        masspoint_script_name = 'wmLHE_'+masspoint+'_cfg.py'
        #new_file_name = os.path.join(full_path,masspoint_script_name)
        print 'mass point script name = ' , masspoint_script_name
        with open(template_file, 'r') as input_file:
            with open(masspoint_script_name,'w') as output_file:
                #shutil.copyfile(template_file, masspoint_script_name)
                for line in input_file:
                    if '.tar.xz' in line:
                        replacement_string = '    args = cms.vstring(\'../Codex_' + masspoint + '_gen3.tar.xz\')'
                        output_file.write(replacement_string)
                    else:
                        output_file.write(line)
