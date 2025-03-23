## Databricks Cluster Cost Savings Summary

### 📊 Cluster Configuration
- **Driver Node:** `E64ds_v4` (64 vCPUs)
- **Worker Nodes:** `E20ds_v4` Spot Instances (20 vCPUs each)
- **Total Compute:** 1600 vCPUs
  - 1 Driver (64 vCPUs)
  - 77 Workers (1536 vCPUs total)
- **Spot Instance Discount:** ~85% off on-demand price

---

### 💰 Estimated Hourly Cost Breakdown

| Component           | Units               | Rate (USD/hr) | Total Cost (USD/hr) |
|---------------------|---------------------|---------------|----------------------|
| **Driver VM**        | 1 x E64ds_v4         | $2.50         | $2.50                |
| **Worker VMs (spot)**| 77 x E20ds_v4 (spot)| $0.117        | $9.01                |
| **Driver DBU**       | 6.0 DBUs             | $0.55         | $3.30                |
| **Worker DBUs**      | 77 x 2.5 DBUs        | $0.55         | $105.88              |
| **Total Hourly Cost**|                     |               | **$120.69/hr**       |

---

### 🕒 Annual Usage Savings

- **Compute Hours Saved:** 1600 hrs/year
- **Total Annual Savings:**  
  `1600 hrs * $120.69/hr` = **~$193,104**

---

### ✅ Summary

By eliminating or optimizing 1600 compute hours annually on this Databricks cluster setup, you save approximately:

> ## 💵 **$193,000 per year**


---

## 📈 Scaled Databricks Cost Savings (Based on File Count)

### 🔍 Previous Savings
- **Files Processed:** 600
- **Annual Compute Hours Saved:** 1600 hrs
- **Total Annual Savings:** ~$193,104

---

### 📦 New Scenario
- **Files Processed:** 1500
- **Scaling Factor:** 1500 / 600 = 2.5x

---

### 💰 New Estimated Annual Savings

\[
1500 \text{ files} \Rightarrow 2.5 \times 1600 \text{ hrs} = 4000 \text{ hrs saved}
\]

\[
4000 \text{ hrs} \times \$120.69/\text{hr} = \$482,760
\]

> ## 💵 **~$482,760 saved per year**  
> By optimizing compute usage across 1500 files on the same Databricks cluster setup.

