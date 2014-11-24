# Warning: Edit this file in binary mode or stuff will break.

macro='Go0/ nvnhxj"wddgg;g/^[^vf]/dG?vV?fjxOgg/fO;g/^v /normal @wgg/fVG:s/\(\d*\)/\=(submatch(0)-1)/gggVG:s/^[^ ]* \(.*\)$/\1/ggVG:s/^-1$//GoggOO$rso$ggjjV/^$k:s/ / +/ggjj0/^$kI+ggVG:s/+-/-/g;w'

echo $macro | cat - $1 $2 > $3
vim -c 'normal gg"qdd@q;q' $3
