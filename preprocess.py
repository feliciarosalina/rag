import os
import pandas as pd

# Import data
audience = pd.read_csv("data/audience_reviews.csv")
critic = pd.read_csv("data/critic_reviews.csv")

# Get top 10 most-reviewed shows
audience_100 = audience.groupby("Show")["Review"].count().reset_index().sort_values("Review", ascending=False).head(30)
critic_100 = critic.groupby("Show")["Review"].count().reset_index().sort_values("Review", ascending=False).head(30)
top_10 = audience_100.merge(critic_100, on="Show", how="inner").sort_values(["Review_x", "Review_y"], ascending=[False, False]).head(10)['Show'].to_list()

# Get reviews for top 10 shows
audience_top_10 = audience.loc[audience['Show'].isin(top_10), ["Show", "Review"]]
audience_top_10['Source'] = 'Audience'
critic_top_10 = critic.loc[critic['Show'].isin(top_10), ["Show", "Review"]]
critic_top_10['Source'] = 'Critic'
shows_top_10 = pd.concat([audience_top_10, critic_top_10])

# Get 20 audience reviews and 20 critic reviews for each show
reviews = shows_top_10.groupby(["Show", "Source"]).apply(lambda x: x.sample(20)).reset_index(drop=True)

# Save to csv
reviews.to_csv("output/reviews.csv", index=False)