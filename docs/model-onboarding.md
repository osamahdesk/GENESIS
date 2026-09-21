# Model Onboarding

GENESIS provides a single entry point for users who do not already have a local model. The dashboard detects approximate system memory, presents suitable catalog entries, and accepts three input forms: a Hub repository identifier such as `owner/model`, a Hugging Face URL, or an existing local model directory.

The selected model is saved to `teacher.json`. This record is an experiment input and does not automatically download or execute code. Downloading and loading remain explicit provider operations.

The optional public Hub API adapter calls the public model endpoint only after the user requests a search and enables both the Hugging Face capability and read-only network access. Search results are advisory. The user chooses the model, and the model becomes a Teacher reference for future experiments.

A Teacher may propose a new model project through the sandbox AI Builder. A proposal is not a self-copying autonomous process. It is a candidate artifact that requires review, independent evaluation, regression checks, and an explicit promotion decision.
