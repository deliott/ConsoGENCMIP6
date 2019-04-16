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
bin/${script}.py -fv
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
else
  echo "${script} OK"
fi

script="plot_bilan_jobs"
printf "\n${script}\n"
echo "--------------------"
bin/${script}.py -fv
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
else
  echo "${script} OK"
fi

script="plot_jobs_daily"
printf "\n${script}\n"
echo "--------------------"
bin/${script}.py -fv
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
else
  echo "${script} OK"
fi

script="plot_login"
printf "\n${script}\n"
echo "--------------------"
bin/${script}.py -v
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

bin/${script}.py -fv
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
rsync -var ${ROOT_DIR}/web/* igcmg@ciclad.ipsl.jussieu.fr:dods/ConsoGENCMIP6


printf "\nEnd of script OK\n"

