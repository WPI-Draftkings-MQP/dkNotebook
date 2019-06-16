# Predicting Contest Profitability for DraftKings

This project was completed as a Senior Capstone project for the Worcester Polytechnic Institute MQP graduation requirement. It was also sponsored by DraftKings, who provided the dataset. The data is company property, and as a result it has not been included in the repository.

### Instructions left to DraftKings

We've really enjoyed working on this project! We learned a lot and are proud of our results. If you have any questions at all, please email or text me. 

In order to fit on the flash drive, I had to compress the folder in _data/_. (Specifically, _Chunks_, _Chunks\_Raw_, _Chunks\_Scale_, and _Vault_)

The majority of the code we produced was written in python 3.6 in a Jupyter Notebook. The primary libraries used were Numpy, Pandas, SciKitLearn, and MatPlotLib. The time series data is modeled to the equation _y=A*e^(B*x)_ The following is a list of files provided with a short explanation of what they do:

* _[1.1] Chunking Series_: The original time series data (_Chunks\_Raw/_) was separated by month, so individuals contests occassionally had data spread between two files. This script 're-chunked' the data into new files (_Chunks/_) such that all time series data for individual contests is contained in a single chunk.

* _[1.2] Durations_: It was necessary to know the ammount of time between the first entry into a contest and when the contest ended. This script produces a list of contest durations (_Durations.csv_).

* _[2] Scaling Chunks_: It was also necessary to scale the time series data (_Chunks/_) such that each contest ended at Time=100 Entries=100. This enables the parameters computed via Weighted Least Squares and Extended Kalman Filters to be comparable. The scaled versions of the data is in _Chunks\_Scaled/_

* _[3.1] Kalman Processing_: This script computes the A and B values of our model via an Extended Kalman Filter with varying confidence parameters. Those cofidence parameters are in _data/QR_Values.csv_.  The list of these computed values are in _data/KF_Values.csv_.

* _[3.2] Linear Regression Processing_: This script computes the A and B values of our model via Weighted Least Squares with varying Forgetting Factors. The list of these computed values are in _data/LR_Values.csv_.

* _[4] AeBX Processing_: This script computes the actual prediction from each variant of the Extended Kalman Filter and Weighted Least Squares. These results are stored in _data/KF\_Preds.csv_ and _data/LR\_Preds.csv_ respectively. 

* _[5] Full Data Processing_: This script combines the header data and time series results. It processes the raw header data (_data/WorkingData.csv_) into (_data/MetaData.csv_). It additionally scales _data/KF\_Results.csv_ and _data/LR\_Results.csv_ by contest durations, such that predictions of successfully filling contests have values >=1. This script then combines _data/MetaData.csv_, _data/KF\_Results.csv_, and _data/LR\_Results.csv_ into a single file, _data/WorkedData.csv_.

* _[6]  Splitting Data (Train, Test, and Vault)_: This script partitions the data (_data/workedData.csv_) into 5 chunks. The largest chunk becomes _data/Vault/train.csv_, and the remaining data is split into 4 equally sized testing chunks (_data/Vault/test1.csv_, ._.../test2.csv_, _.../test3.csv_, and _.../test4.csv_).

* _[7]  Forest + ROC Curves_: This script contains examples of ROC Curves, both for single feature columns and Random Forest Classifier Ensembles results of multiple features.

* _[7+]  Results Analysis! (Vault1)_: This script explores the effectiveness of different parts of our algorithm, as well as our final algorithm: the Situational Predictor. By adjusting the vault variables at the top, you can cross-validate the results.

* _[viz]  Final Analytics_: This script produces a few graphs to show the power of the Situational Predictor.

* _[viz]  Series Graphs_: This script produces a few graphs to visualize how we implement the Extended Kalman Filter and Weighted Least Squares on a single contest.


Data Files not mentioned above:
* _Baseline.csv_: Measurements of how full each contest is at 4-hours-remaining.
* _DK\_Predictions\_Raw.csv_: The file containing all DraftKings Predictions for contests. 
* _DK\_Pacer\_Success.csv_: The 4-hours-out predictions extrapolated from _DK\_Predictions\_Raw.csv_. 
