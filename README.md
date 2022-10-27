# NormConf API
Welcome to the most impactful API you've never heard of!

Using latent-space embeddings we synthesize every arxiv deep learning finding in the last 10 years into a k8s cluster. Then we decompose the logits into a novel, multi-headed attention model with distributed compute across 13 time zones. 

....


| API            | endpoint                        | description                |
| -------------- | ------------------------------- | -------------------------- |
| normconf       | api.normconf.com/normconf       | ASCII Goodness             |
| random_goodies | api.normconf.com/random_goodies | Random Goodness            |
| schedule       | api.normconf.com/schedule       | Normconf Schedule Goodness |


Ideas

1 a randomized response of our curated list of blog posts,
2 same as 1 but shitposts,
3 pizza-delimited values and maybe a link to that twitter conversation about delimiters


# To Develop Locally: 

1. Clone and go to repo root
2. `make integration` to build and run locally with Poetry (requires Python 3.10+)
3. `make run` to build and run Docker image locally