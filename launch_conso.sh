#!/bin/bash
#
# Cron to keep track of the consumption and data volume 
# for GENCMIP6 project.
# To be executed every day at 6am
# ======================================================================

# Initialize module command
# =========================
if [ -f /etc/bashrc ] ; then
  . /etc/bashrc
fi

# Load python
# ===========
# python/2.7.3 is the default, but it comes with matplotlib 1.2, 
# which is too old (no context manager for PdfPages)
module load python/2.7.8

# Go to root directory
# ====================
ROOT_DIR=$( dirname $0 )
cd ${ROOT_DIR}

# Main script to get data
# =======================
script="conso_gencmip6"
printf "${script}\n"
echo "--------------------"
bin/${script}.py -v
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
  exit
else
  echo "${script} OK"
fi

# Plot daily consumption
# ======================
# -f : plot the whole period of the project
# -d : copy plot on dods
# -v : verbose mode
script="plot_bilan"
printf "\n${script}\n"
echo "--------------------"
bin/${script}.py -fdv
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
else
  echo "${script} OK"
fi

script="plot_bilan_jobs"
printf "\n${script}\n"
echo "--------------------"
bin/${script}.py -fdv
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
else
  echo "${script} OK"
fi

script="plot_jobs_daily"
printf "\n${script}\n"
echo "--------------------"
bin/${script}.py -fdv
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
else
  echo "${script} OK"
fi

script="plot_login"
printf "\n${script}\n"
echo "--------------------"
bin/${script}.py -dv
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
else
  echo "${script} OK"
fi

script="plot_store"
printf "\n${script}\n"
echo "--------------------"
# Last STORE file produced
data_file="OUT_CONSO_STORE"
OUTDIR="${HOME}/ConsoGENCMIP6/output"
# Directories in last file
dirlist=$( gawk '{if ($4 != "dirname") print $4}' ${OUTDIR}/${data_file} )
# Where to find the saved files
SAVEDIR="${WORKDIR}/ConsoGENCMIP6/data"
# Previous STORE files
filelist=$( ls ${SAVEDIR}/${data_file}_* )
fileout="${data_file}_INIT"
echo "date       login      dirsize dirname" > ${OUTDIR}/${fileout}
for dir in ${dirlist} ; do
  grep -h "$dir\$" ${filelist} | head -1
  grep -h "$dir\$" ${filelist} | head -1 >> ${OUTDIR}/${fileout}
done

bin/${script}.py -fdv
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
else
  echo "${script} OK"
fi


# Copy web files to ciclad
# ========================
echo "=> Copy web files to ciclad"
echo "==========================="
echo "rsync -var ${ROOT_DIR}/web/* igcmg@ciclad.ipsl.jussieu.fr:dods/ConsoGENCMIP6"
rsync -var ${ROOT_DIR}/web/* igcmg@ciclad.ipsl.jussieu.fr:dods/ConsoGENCMIP6

# # Copy cpt file to slipsl
# # =======================
# echo "=> Copy cpt file to slipsl"
# echo "=========================="
# 
# local_dir="output"
# # remote_dir="/data/slipsl/ConsoGENCI"
# remote_dir="/home_local/slipsl/ConsoGENCI/data/tgcc/tmp"
# remote_login="slipsl"
# # remote_host="ciclad.ipsl.jussieu.fr"
# remote_host="pc-236"
# bounce_login=${remote_login}
# # bounce_host="calcul2.ipsl.jussieu.fr"
# bounce_host="ciclad.ipsl.jussieu.fr"
# 
# local_fileout="ccc_myproject.dat"
# date_amj=$( head -n 2 ${local_dir}/${local_fileout} | tail -n 1 | gawk '{ print $NF }' | gawk -F "-" '{ print $1$2$3 }' )
# remote_fileout="cpt_tgcc_gencmip6_${date_amj}_2359.dat"
# 
# ssh_options="-T -ax -o ClearAllForwardings=yes -c blowfish"
# 
# 
# # scp ${filein} igcmg@ciclad.ipsl.jussieu.fr:/data/igcmg/ConsoGENCI/data/tmp/tgcc/${fileout}
# 
# set -vx
# 
# rsync -va -e "ssh ${ssh_options} ${bounce_login}@${bounce_host} ssh ${ssh_options}" \
#              ${local_dir}/${local_fileout} \
#              ${remote_login}@${remote_host}:${remote_dir}/${remote_fileout}

printf "\nEnd of script OK\n"

exit

