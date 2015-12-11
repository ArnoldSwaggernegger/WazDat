# WazDat

WazDat is a simple audio retrieval system based on the algorithms Shazam uses.
It can compare a signal with the database in a time invariant, amplitude invariant and noise resistant way. 
The project is written in python.

## Usage

A database is created as follows

``` 
python main.py -d dbname --train datafolder/subfolder
```

Files can then be classified using

```
python main.py -d dbname -f filename
```

## Cloning

The project can be cloned as follows:

```
git clone git@github.com:ArnoldSwaggernegger/WazDat.git
```

Note that the used datasets are stored on the Git Large File Storage (LFS) system.
