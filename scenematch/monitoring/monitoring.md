#### Below is what each query measures and the insight it adds to feedback dashboard.

#### Average Rating Trend

``` sql
SELECT
  date_trunc('hour', timestamp) AS "time",
  AVG(rating)                   AS "Average Rating"
FROM public.user_feedback
WHERE $__timeFilter(timestamp) AND rating IS NOT NULL
GROUP BY 1
ORDER BY 1;
```

- What it does: Aggregates all rating values within each hour (or whatever time range the user selects) and returns their average.

- Why it matters: Shows how overall sentiment changes over time. Rising numbers signal improving user satisfaction; falling numbers warn of emerging issues.

#### Rating Distribution


``` sql
SELECT
  rating::text AS "Rating",
  COUNT(*)     AS "Count"
FROM public.user_feedback
WHERE rating IS NOT NULL
GROUP BY rating
ORDER BY rating;
```

- What it does: Counts how many feedback entries fall into each rating bucket (1-star, 2-star, … ).

- Why it matters: Reveals the spread of opinions. A distribution skewed toward high values confirms general happiness, while a long tail of low scores highlights dissatisfaction pockets.

#### Latest Feedback Table


``` sql
SELECT
  timestamp    AS "Time",
  rating       AS "Rating",
  comment      AS "Comment",
  user_message AS "User Message"
FROM public.user_feedback
WHERE rating IS NOT NULL
ORDER BY timestamp DESC
LIMIT 20;
```
- What it does: Shows the 20 most-recent rated submissions with the user’s comment and original message.

- Why it matters: Gives real-time, qualitative context behind the numbers. You can quickly scan fresh complaints or praise and act before patterns affect the averages.


##### Together, these three panels let you:

Track sentiment over time (trend),

See the overall score balance (distribution), and

Read the underlying stories (latest feedback).