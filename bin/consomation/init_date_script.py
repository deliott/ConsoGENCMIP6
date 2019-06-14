"""
Small script written to get the init_date of a project.

To be integrated into the bigger project.
Here used with data manually extracted from gen0826 ccc_myproject logs.


"""

import datetime
import pandas as pd

# Tpc = 0.5492
# today = pd.to_datetime('2019-05-21')
# deadline = pd.to_datetime('2019-11-04')
# deltaT = deadline - today
# factor = Tpc/(1-Tpc)
# initial_date = today - factor * deltaT
#
# print(initial_date)

Tpc = [52.73, 53.01, 53.28, 53.55]
today = pd.to_datetime('2019-05-13')
deadline = pd.to_datetime('2019-11-04')
deltaT = deadline - today

for i in range(len(Tpc)):
	factor = Tpc[i]/(100-Tpc[i])

	today = today + datetime.timedelta(days=1)
	deltaT = deadline - today
	initial_date = today - factor * deltaT

	print(initial_date)
