from genesis.providers.huggingface_local import HuggingFaceLocalProvider


provider = HuggingFaceLocalProvider("models/sshleifer-tiny-gpt2")
response = provider.generate("GENESIS is", max_new_tokens=8)

print(response.text)
print({
    "provider": response.provider,
    "model": response.model,
    "input_tokens": response.input_tokens,
    "output_tokens": response.output_tokens,
})
