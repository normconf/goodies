# NormConf API
![](https://raw.githubusercontent.com/normconf/goodies/main/app/goodies/media/normconf_logo.png?token=GHSAT0AAAAAABZNNDSLZ7QY2VCAIFC54ILKY2653VQ)

Welcome to the most impactful API you've never heard of!

From the creators of [NormConf the conference](https://normconf.com/), happening December 15. 

Using latent-space embeddings we synthesize every arxiv deep learning finding in the last 10 years into a k8s cluster. Then we decompose the logits into a novel, multi-headed attention model with distributed compute across 13 time zones. 



| API      | endpoint                  | description                                                   |
| -------- | ------------------------- | ------------------------------------------------------------- |
| normconf | api.normconf.com/ascii | ASCII Goodness                                                |
| random   | api.normconf.com/random   | Random Goodness                                               |
| schedule | api.normconf.com/schedule | Normconf Schedule Goodness                                    |
| wisdom   | api.normconf.com/wisdom   | Normconf Schedule Goodness                                    |
| talks    | api.normconf.com/get_talk | Find out what someone's talk will be about according to GPT-2 |

[API Docs](api.normconf.com/docs)

## To Develop Locally

1. Clone and go to repo root
2. `make integration` to build and run locally with Poetry (requires Python 3.10+)
3. `make run` to build and run Docker image locally
