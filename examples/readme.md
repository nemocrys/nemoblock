# Examples for nemoblock

Collection of examples for nemoblock

## blocks_01

This is the same example as in the main readme. The resulting mesh looks like this:

![example mesh](../images/blocks_01.png)

## blocks_02

This is a slightly more complex examples showing how to work with blocks. The resulting mesh looks like this:

![example mesh](../images/blocks_02.png)

## ds_grid

This is a more advanced mesh used for Directional Solidification growth simulation consisting out of 8 blocks:

![example mesh](../images/grid_ds.png)

The geometry parameters are defined in *ds_points.py*, the mesh is generated with *ds_grid.py*. The mesh looks like this (vertical cut):

![example mesh](../images/gridstart_ds.png)

## cz_grid

This is a complex mesh used for Czochralski growth simulation consisting out of 27 blocks:

![example mesh](../images/grid_cz.png)

The geometry parameters are defined in *cz_points.py*, the mesh is generated with *cz_grid.py*. The mesh looks like this (vertical cut):

![example mesh](../images/gridstart_cz.png)

## cz_2d

This is a simple 2D mesh for Czochralski growth consisting of 7 blocks.
![example mesh](../images/cz_2d_topology.png)
![example mesh](../images/cz_2d.png)
