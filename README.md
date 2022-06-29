# bti-ph-2
## concrete
Data on 2 MPa strength is pretty unknown currently. Standard referenced in the challenge doc only goes up to ~1 MPa. It does list things that can strengthen it but not in numbers.

The data concrete-data file contains 1030 concrete recipes, their age, and their corresponding compressive strengths. The only issue is that the lowest compressive strength is at ~8.5 MPa.

It may be possible to gather data to extend this model down to a range that is applicable to us. The data in the referenced standard is an initial look at how the model predicts it. Closer look at the model needs to use first principles to help eliminate variables that do not make sense for further simplicity.

### To Use
Fill out input-data.csv
Run recipe.py
out-put.csv will be updated with new data