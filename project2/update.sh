#/bin/bash 

PYTHON="/usr/local/bin/python3.7"
#TARGET="results"
TARGET="/Users/jayanti/Projects/Softlab/Covid-19-draft/"
SOURCE="output/"

declare -a StringArray=("Canada.pdf" "France.pdf" "Germany.pdf"\
    "India.pdf" "Iran.pdf" "Italy.pdf" "Russia.pdf" "Spain.pdf" "Brazil.pdf" "US.pdf")


$PYTHON  create_param_table.py  -i $SOURCE  -o $TARGET/tables/ 
$PYTHON  create_R0_table.py  -i $SOURCE  -o $TARGET/tables/ 
$PYTHON  create_country_data.py -i $SOURCE/MODEL1_SIR_exp/fit_params.csv -o $TARGET/tables/ 
$PYTHON  plot_R0_hist.py -i $SOURCE/R0_ALL.csv  -o $TARGET/figures/

dir=`ls -d $SOURCE*/ | xargs -n1 -I{} basename "{}"`
#dir=`ls -d $SOURCE*/`

for d in $dir; do
   for val in ${StringArray[@]}; do
       echo $SOURCE$d/plots/$val  $TARGET/figures/countries/$d
      `cp $SOURCE$d/plots/$val  $TARGET/figures/countries/$d`
   done
done

