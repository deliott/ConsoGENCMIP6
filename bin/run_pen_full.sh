#!/bin/bash
#
# cron pour garder trace des jobs running et en attente
# a executer chaque heure
# ======================================================================
#. /etc/profile

# Functions
# =========
function get_run {
  ccc_mpp -rn | grep -i skylake
}

function get_pen {
  # ccc_mpp -pn | awk '{ print $4, $NF }' | \
  ccc_mpp -pn | grep -i skylake | \
          grep -v JobHeldAdmin | \
          grep -v Dependency | \
          grep -v BeginTime | \
          grep -v RESV | \
          grep -v AssocGrpJobsLimit | \
          grep -v AssociationResourceLimit
}


# Default values
# ==============
fg_dry=false
fg_verbose=false

fg_all=true

# Get arguments from command line
# ===============================
while getopts :hdaltsv Opt ; do
  case $Opt in
    h)
      echo "usage: $0 [-h] [-a] [-d] [-v]"
      echo ""
      echo "options :"
      echo "  -h : print this help and exit"
      echo "  -d : dry run, no file produced"
      echo "  -a : produce all files (default)"
      echo "  -v : verbose"
      exit 0 ;;
    d)
      fg_dry=true
      ;;
    a)
      fg_all=true
      ;;
    v)
      fg_verbose=true
      ;;
    :)
      echo "$0: -"${OPTARG}" option: missing value"
      exit 1
      ;;
    \?)
      echo "$0: -"${OPTARG}" option: not supported"
      exit 1
      ;;
  esac
done
shift $(($OPTIND-1))


# Files and directories
# =====================
## LOCAL_DIR="${HOME}/IRENE/ConsoGENCMIP6/output"
LOCAL_DIR="/ccc/cont003/home/gencmip6/p86ipsl/IRENE/ConsoGENCMIP6/output"
## SAVE_DIR="${CCCWORKDIR}/IRENE/ConsoGENCMIP6/data"
SAVE_DIR="/ccc/work/cont003/gencmip6/p86ipsl/IRENE/ConsoGENCMIP6/data"

if ( ${fg_dry} ) ; then
  OUT_PENDING="/dev/stdout"
  OUT_TOUSJOBS="/dev/stdout"
else
  OUT_PENDING="OUT_JOBS_PEN_FULL"
  OUT_TOUSJOBS="OUT_TOUSJOBS_FULL"
fi

Today=$( date +"%F" )
Now=$( date +"%F-%R" )


# Produce files
# =============

cd ${LOCAL_DIR}

# 1- tous les jobs running et pending
# -----------------------------------

if ( ${fg_all} ) ; then
  get_run > ${OUT_TOUSJOBS}
  get_pen >> ${OUT_TOUSJOBS}
fi

# 2- Nombre de procs running et pending
# -------------------------------------
if ( ${fg_all} ) ; then
  get_run | \
      gawk -v Now="$Now" ' {NPROC+=$4} END {printf "%16s  %-6d ", Now, NPROC }' \
      > ${OUT_PENDING}
  get_pen | \
      gawk               ' {NPROC+=$4} END {printf      " %-6d ",      NPROC }' \
      >> ${OUT_PENDING}
  printf "\n" >> ${OUT_PENDING}
fi

# Save files (WORK)
# =================
if ( ! ${fg_dry} ) ; then
  Suffix=$( echo ${Today} | sed 's/-//g' )
  [ -f ${SAVE_DIR}/${OUT_PENDING}_${Suffix} ] || echo "AAAA-MM-DD-HH:MM RUN   PENDING" > ${SAVE_DIR}/${OUT_PENDING}_${Suffix}
  cat ${OUT_PENDING} >>${SAVE_DIR}/${OUT_PENDING}_${Suffix}
  cp ${OUT_TOUSJOBS} ${SAVE_DIR}/${OUT_TOUSJOBS}_${Suffix}
fi

