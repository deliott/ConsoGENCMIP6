#!/bin/bash
#
# Cron to keep track of core usage for GENCMIP6 project.
# To be executed every hour
# ======================================================================

# Initialize module command
# =========================
if [ -f /etc/bashrc ] ; then
  . /etc/bashrc
fi
# Load python
# ===========
# python/2.7.3 is the default, but it comes with matplotlib 1.2, 
# which is too old (no context manager for PdfPages)
module load python/2.7.8

# Go to root directory
# ====================
ROOT_DIR=$( dirname $0 )
cd ${ROOT_DIR}

# Main script to get data for gencmip6
# ====================================
script="run_pen_v2"
printf "${script}\n"
echo "--------------------"
bin/${script}.sh
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
  exit
else
  echo "${script} OK"
fi

# Main script to get data for whole Irene
# =======================================
script="run_pen_full"
printf "${script}\n"
echo "--------------------"
bin/${script}.sh
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
  exit
else
  echo "${script} OK"
fi

# Plot running and pending jobs
# =============================
# -d : copy plot on dods
# -m : mode, 'project' (=default) or 'machine'
script="plot_jobs"
printf "\n${script}\n"
echo "--------------------"
bin/${script}.py -vd
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
else
  echo "${script} OK"
fi

printf "\n${script}\n"
echo "--------------------"
bin/${script}.py -vdm machine
rc=$?
if [ ${rc} -ne 0 ] ; then
  echo "${script} terminated abnormally"
else
  echo "${script} OK"
fi

script="plot_jobs_hourly"
printf "\n${script}\n"
echo "--------------------"
bin/${script}.py -vd
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
rsync -var ${ROOT_DIR}/web/* igcmg@ciclad.ipsl.jussieu.fr:dods/IRENE/ConsoGENCMIP6
scp  /ccc/cont003/home/gencmip6/oboucher/CONSO/IRENE/conso.png igcmg@ciclad.ipsl.jussieu.fr:dods/IRENE/ConsoGENCMIP6/img


printf "\nEnd of script OK\n"

