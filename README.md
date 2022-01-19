
# Fantasy Premier League Insights

Insights to help FPL managers make transfer decisions using the FPL API and xG data from understat. Project still only runs on local machine, plan is to have it run automatically on AWS.


## Tableau Public 

[Link to tableau story](https://public.tableau.com/app/profile/sitwala.mundia/viz/FPLInsightGW1-GW1920212022Season/Story1)

 ![](images/volatility.PNG)

## Deployment

To use this project.
* Clone repo
* Python scripts are in the [scripts folder](https://github.com/SitwalaM/fpl/tree/main/scripts)
* Install environment dependencies in the folder  using

```bash
  pip install -r requirements.txt 
```

To get the latest FPL data, run main.py file using your IDE or
```bash
  python3 main.py
```
The csv files used for the insights will be in the [data folder](https://github.com/SitwalaM/fpl/tree/main/data). Note that you have certain variables available to you in the module for fixture difficulty rating and the xG data.

## Badges

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

## Authors

- [@SitwalaM](https://github.com/SitwalaM)
  
## Acknowledgements

 - [Detailed guide to FPL endpoints](https://medium.com/@frenzelts/fantasy-premier-league-api-endpoints-a-detailed-guide-acbd5598eb19)
 - [Code examples for python FPL data](https://towardsdatascience.com/fantasy-premier-league-value-analysis-python-tutorial-using-the-fpl-api-8031edfe9910)
 - [understat to FPL ID MAP](https://github.com/ChrisMusson/Football-Datasets)
 - [FPL Dev Discord](https://discord.gg/rEuX54nz)
 

    
