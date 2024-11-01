# autoMS
LC-MS tool for fast, automated mzML preprocessing in untargeted metabolomics analysis.


## Install and launch
```bash
git clone https://github.com/michael-jopiti/autoMS.git
echo "alias autoMS='python3 $PWD/autoMS/main.py'" >> ~/.bashrc
source ~/.bashrc
autoMS -h
```

## Simple launch with basic summary of (each) files(s)

```bash
autoMS -i path/to/file(s).mzML -o path/to/output -sum
```

## Affiliation
This project is affiliated with [EMI](https://www.earthmetabolome.org/) and [DBGI](https://www.dbgi.org/).
