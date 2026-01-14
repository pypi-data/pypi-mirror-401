# abcard  

**abcard** is a Python package primarily used for developing binary classification models and generating reports for production work.  
It supports Logit and LGBM models, can generate PDF model reports and production-ready deployment code.  
It emphasizes concise and efficient API calls, rich visualizations, and retention of the development process.  


# Installation  

**abcard** requires **Python 3.9 or later**, install using **pip** with:  

`pip install abcard`  

Additional dependencies: numpy, pandas, tqdm, statsmodels, scikit-learn, matplotlib, PyMuPDF, lightgbm  


# Main Features  

from abcard import Frame, LogitFrame, LGBMCFrame, Report, ModReport, LogitReport, LGBMCReport  

train: 'pandas.DataFrame datasets'  
test: 'pandas.DataFrame datasets'  
oot: 'pandas.DataFrame datasets'  
flag: 'target label (y)'  
time: 'name of the time column, optional'  
exclude: 'column names to be excluded, optional'  
Mod: 'Logit, LGBM models'  

df = LogitFrame(flag = flag, time = time, exclude = exclude) # Initial sample set field configuration.  
df = LGBMCFrame(flag = flag, time = time, exclude = exclude) # Initial sample set field configuration.  
df.set_samp(train, 'train') # Set the sample dataset.  
df.get_samp(test, 'test') # Get the sample dataset.  
df.del_samp(oot, 'oot') # Delete the sample dataset.  

df.describe_sample() # Descriptive analysis of samples.  
df.describe_feature() # Descriptive analysis of fearures.  
df.chi2_split() # Perform chi-square binning on all features.  

df.mergebins() # Merge bins manually.  

df.drop_nan(nan = 0.9) # Various feature filtering methods starting with 'drop'.  

df.transform() # Convert the sample set into bins or WOE.  

train_set = df.get_xy(label = 'train') # Get the X and y for model training or prediction.  
df.get_metric() # Retrieve the model's evaluation metrics on all sample sets.  
df.scorecard() # Calculate Logistic Regression Scorecard for Selected Features.  

df._mod = Mod  # A fully trained model.  

rep = LGBMCReport(df) # Initialize a PyMuPDF Document object for a LGBMClassifier model Frame object.  
rep.design()  
rep.describe_feature()  
rep.bins() # Generate a chapter for the feature binning results.  
rep.filter() # Generate a chapter for the feature filtering results.  
rep.modres() # Generate a chapter containing the model results.  
rep.analysis('train') # Generate a chapter containing the model analysis and evaluation for the specified samples.  
rep.plotcuts(cores = 4) # Generate a chapter containing the model binning plots.  
rep.code() # Generate a chapter containing the deployment code.  
rep.log()  
rep.save("model_name_report.pdf")  
rep.close()  


# License and Copyright  

**abcard** is available under [open-source AGPL](https://www.gnu.org/licenses/agpl-3.0.html) and commercial license agreements.  
