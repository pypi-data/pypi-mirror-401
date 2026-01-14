**Bgolearn** : *a powerful Bayesian Global Optimization package specifically designed for materials discovery*. This document is written and produced by **[Bin Cao](https://bin-cao.github.io/)** to help new learners master the basics of Bayesian Optimization and use **Bgolearn** to solve real-world optimization problems. 


Bgolearn is a Python package developed by **[Bin Cao](https://bin-cao.github.io/) at Hong Kong University of Science and Technology (Guangzhou)** that implements state-of-the-art Bayesian optimization algorithms for both single-objective and multi-objective optimization. It's particularly powerful for materials discovery, where experiments are costly and time-consuming. 


**Key Features:**
- Single-objective optimization with multiple acquisition functions
- Multi-objective optimization via MultiBgolearn
- Materials-focused design and applications
- Flexible surrogate model selection
- Bootstrap uncertainty quantification

---


Quick Usage Example
from Bgolearn.BGOsampling import Bgolearn
import pandas as pd

# Load your data
data = pd.read_csv('data.csv')
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# (Optional) Provide virtual samples for screening
vs = pd.read_csv('virtual_data.csv')

# Create and configure optimizer
optimizer = Bgolearn()
model = optimizer.fit(data_matrix=X, Measured_response=y, virtual_samples=vs)

# Run Expected Improvement acquisition
candidates = model.EI()


### Support & Contribution
Author & Maintainer: Dr. Bin Cao (CaoBin) — email: bcao686@connect.hkust-gz.edu.cn.

### Collaboration Welcome: Open for issues, pull requests, and research partnerships.

