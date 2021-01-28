# csv_merge_script

Script merges csv files stored in a folder into one csv

**Usage:**

1. Store csv files into a folder in script location('files' by default)
2. Run csv_aggregator script with params if needed

```shell
python csv_aggregator.py --files_path <path> --file_prefix <prefix>  
                         --filename=<filename> 
```

3. Result will be saved in the script location directory

**For additional info, use:**

```shell
python csv_aggregator.py --help
```

**Run tests**
```shell
python tests.py
```

P.S. Add empty folder 'files_empty' for tests to pass