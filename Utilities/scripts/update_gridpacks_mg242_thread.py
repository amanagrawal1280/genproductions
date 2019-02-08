import os,sys
import hashlib
import string
import argparse

parser = argparse.ArgumentParser(description='script to patch the nthreads problem in MG5_aMC LO configurations.')
parser.add_argument('--prepid', type=str, help="check mcm requests using a single prepid", nargs=1)
args = parser.parse_args()

if args.prepid is not None:
    parser.parse_args('--prepid 1'.split())
    prepid = args.prepid
else:
   print "the script needs a prepid,i.e. python update_gridpacks_mg242_thread.py --prepid HIG-... "
   sys.exit()

my_path = '/tmp/'+os.environ['USER']+'/replace_gridpacks/'

print requests

for prepid in requests:

        os.system('echo '+prepid)
        
        os.system('mkdir -p '+my_path+'/'+prepid)
        os.chdir(my_path+'/'+prepid)
        os.system('wget -q https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/'+prepid+' -O '+prepid)
        gridpack_cvmfs_path = os.popen('grep \/cvmfs '+prepid+'| grep -v \'#args\' ').read()
        gridpack_cvmfs_path = gridpack_cvmfs_path.split('\'')[1]
	gridpack_eos_path = gridpack_cvmfs_path.replace("/cvmfs/cms.cern.ch/phys_generator","/eos/cms/store/group/phys_generator/cvmfs")

        print gridpack_cvmfs_path
	if not 'madgraph' in gridpack_cvmfs_path: continue
	if not '.tar.xz' in gridpack_cvmfs_path: continue
	if '_noiter.tar.xz' in gridpack_cvmfs_path: continue
        
	prepid = hashlib.sha224(gridpack_cvmfs_path).hexdigest()
        print 'gridpack_cvmfs_path',gridpack_cvmfs_path; sys.stdout.flush()
        print 'prepid',prepid; sys.stdout.flush()
        os.system('mkdir -p '+my_path+'/'+prepid)
        os.chdir(my_path+'/'+prepid)

        gridpack_eos_path = gridpack_cvmfs_path.replace('/cvmfs/cms.cern.ch/phys_generator/gridpacks/','/eos/cms/store/group/phys_generator/cvmfs/gridpacks/')
        gridpack_eos_path_noiter = gridpack_eos_path.replace('.tar.xz','_runmode0_TEST.tar.xz')
                
        ##############################################
        ############ START REPLACE ###################
        ##############################################        
        if not os.path.exists(gridpack_eos_path_noiter):
            print "ERROR: BACKUP GRIDPACK NOT EXISTING! COPYING"
            print('cp -n '+gridpack_eos_path+' '+gridpack_eos_path_noiter); sys.stdout.flush()
            os.system('cp -n '+gridpack_eos_path+' '+gridpack_eos_path_noiter)
            # continue
        # else:
            # print "Backup gridpack",gridpack_eos_path_noiter,"already existing, i.e. should be patched!";
            # continue
        if "_NLO_" in gridpack_eos_path or "_FXFX_" in gridpack_eos_path:
            print "gridpack seems to be NLO, skipping";
            continue
        statinfo_noiter = os.stat(gridpack_eos_path_noiter)
        if statinfo_noiter.st_size <= 10485760:
            print "ERROR: BACKUP CORRUPTED! SKIPPING"; sys.stdout.flush()
            continue
        # print('rm -rf '+my_path+'/'+prepid+'/*'); sys.stdout.flush()
                
        print 'PATCHING: untarring',gridpack_eos_path_noiter; sys.stdout.flush()
        os.system('rm -rf '+my_path+'/'+prepid+'/*'); sys.stdout.flush()
        os.system('tar xf '+gridpack_eos_path_noiter)
        
          
        merge = os.popen('grep toomanythreads runcmsgrid.sh').read()
        if merge == "":
            if merge == "":
                print 'replacing the string in runcmsgrid.sh'; sys.stdout.flush()
                os.system("patch < /eos/cms/store/group/phys_generator/cvmfs/gridpacks/mg_amg_patch/mg242_runmode.patch")

                
            print 'tarring to gridpack.tar.xz for',prepid; sys.stdout.flush()
            os.system('tar cfJ gridpack.tar.xz ./*')
            statinfo_new = os.stat('gridpack.tar.xz')
            print 'statinfo_new',statinfo_new; sys.stdout.flush()
            if statinfo_new.st_size > statinfo_noiter.st_size*0.9:
                print 'copying gridpack.tar.xz to',gridpack_eos_path; sys.stdout.flush()
                os.system('rm '+gridpack_eos_path+'; cp gridpack.tar.xz '+gridpack_eos_path)
            else:
                print 'ERROR: from the size, gridpack.tar.xz seems corrupted, skipping'; sys.stdout.flush()
        else:
            print "GRIDPACK SEEMS TO BE PATCHED (i.e. merge already present)\n"; sys.stdout.flush()
            continue
        # os.system('rm -rf '+my_path+'/'+prepid+'/*'); sys.stdout.flush()


        ##############################################
        ################# END REPLACE ################
        ##############################################
        
        print '\n'; sys.stdout.flush()
              

              
