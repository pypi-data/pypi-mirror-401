<img src="https://raw.githubusercontent.com/digital-chemistry-laboratory/racerts/main/docs/img/logo.png" alt="Logo" width="1000">

**Ra**pid **C**onformer **E**nsembles with **R**DKit for **T**ransition **S**tates

<img src="https://raw.githubusercontent.com/digital-chemistry-laboratory/racerts/main/docs/img/TOC.png" alt="TOC" width="400">

# Installation

```shell
$ pip install racerts
```

# Usage

racerTS can be imported as a Python module that is easily integrated into
workflows for transition state conformer ensemble generation.
For further information, see the separate [documentation](https://digital-chemistry-laboratory.github.io/racerts/).

```shell
>>> from racerts import ConformerGenerator
>>> cg = ConformerGenerator()
>>> ts_conformers_mol = cg.generate_conformers(file_name="example.xyz", charge=0, reacting_atoms=[2,3,4])
>>> cg.write_xyz("ensemble.xyz")
```

It can also be accessed via a command line interface.

```console
$ racerts example.xyz --charge 0 --reacting_atoms 2 3 4
```

# Cite this work
If you use racerTS in one of your works, please make sure to cite it:

```
@misc{schmid_rapid_2025,
	title = {Rapid generation of transition-state conformer ensembles via constrained distance geometry},
	url = {https://chemrxiv.org/engage/chemrxiv/article-details/69173ebea10c9f5ca165ef65},
	doi = {10.26434/chemrxiv-2025-d50pd},
	language = {en},
	publisher = {ChemRxiv},
  month = nov,
	author = {Schmid, Stefan P. and Seng, Henrik and Kläy, Thibault and Jorner, Kjell},
	year = {2025},
}
```

# Data availability

All data to reproduce the study can be found on [Zenodo](https://doi.org/10.5281/zenodo.17610186).

# License
MIT License

Copyright &copy; 2025 ETH Zürich
