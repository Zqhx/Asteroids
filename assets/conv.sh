# Warning: Edit this file in binary mode or stuff will break.

macro='Go0/ 

echo $macro | cat - $1 $2 > $3
vim -c 'normal gg"qdd@q;q