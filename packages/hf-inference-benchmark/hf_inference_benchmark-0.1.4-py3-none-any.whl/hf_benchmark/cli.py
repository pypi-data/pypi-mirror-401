import click
import json
import os
from hf_benchmark.runner import load_model, run_once
from hf_benchmark.profiler import profile_inference

@click.command()
@click.argument("model")
@click.option("--tokens", default=32, help="Number of tokens to generate")
@click.option("--out", type=click.Path(), help="Save results to a JSON file") # <--- New Option
def main(model, tokens, out):
    click.echo(f"⏳ Loading {model}...")
    model_obj, tokenizer, device = load_model(model)

    task = lambda: run_once(model_obj, tokenizer, device, max_new_tokens=tokens)

    # 1. Capture the stats dictionary
    stats = profile_inference(task, token_count=tokens)

    # 2. Add the model name to the stats for better reporting
    stats["model"] = model
    stats["device"] = device.type.upper()

    # 3. Persistence Logic (The Day-4 Upgrade)
    if out:
        output_dir = os.path.dirname(out)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        with open(out, "w") as f:
            # We map your profiler keys to standard names for the reporter
            export_data = {
                "model": model,
                "throughput": stats['throughput'],
                "latency_p50": stats['p50'],
                "memory_mb": stats['memory_mb']
            }
            json.dump(export_data, f, indent=2)
        click.secho(f"✨ Results archived to {out}", fg="cyan")

    # 4. Keep the UI print for immediate feedback
    print(f"\n✅ Device: {stats['device']}")
    print("-" * 30)
    print(f"📊 Latency (P50) : {stats['p50']:.2f} ms")
    print(f"🚀 Throughput    : {stats['throughput']:.2f} tokens/sec")
    print(f"💾 Peak Memory   : {stats['memory_mb']:.2f} MB")
    print("-" * 30)

if __name__ == "__main__":
    main()