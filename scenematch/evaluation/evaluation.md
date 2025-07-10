### 1. Precision@k

What it tells you: How many of the top-k results are actually relevant?

Why it's useful: Recommenders usually show a short list. If top results aren't good, users won't scroll.

`Formula:`


<br>



>$$
\text{Precision@k} = \frac{\text{Number of relevant results in top-}k}{k}
$$

<br>

---
​
### 2. Recall@k

What it tells you: How many of all relevant results were retrieved?

Why it's useful: Shows coverage — are we missing good recommendations?

`Formula:`
<br>
<br>


> $$
\text{Recall@k} = \frac{\text{Number of relevant results in top-}k}{\text{Total number of relevant results}}
$$
​
 
---

<br>

### 3. MRR (Mean Reciprocal Rank)

What it tells you: How high was the first relevant result?
Why it's useful: Measures early relevance, which is crucial — users care about the first result.


`Formula:`

<br>
<br>

>$$
\text{MRR} = \frac{1}{N} \sum_{i=1}^{N} \frac{1}{\text{rank}_i}
\quad \text{where} \quad
\begin{aligned}
& N &&= \text{total number of queries} \\
& i &&= \text{index of the current query} \\
& \text{rank}_i &&= \text{rank position of the first relevant document for query } i
\end{aligned}
$$

<br>

---


#### Summary


- Quality of top results (Precision@k)

- Coverage of all relevant movies (Recall)

- How soon relevant items appear (MRR)

#### I might add

- Frequency of hitting any relevant item in top-k (Hit Rate @k) 

 
