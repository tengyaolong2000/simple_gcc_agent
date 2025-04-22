import json
import argparse
import pandas as pd
from . import common
from .browsecomp_eval import BrowseCompEval
from .sampler.chat_completion_sampler import (
    OPENAI_SYSTEM_MESSAGE_API,
    OPENAI_SYSTEM_MESSAGE_CHATGPT,
    ChatCompletionSampler,
)

from agent.computer_agent import manager_agent as sampler

def main():
    parser = argparse.ArgumentParser(
        description="Run sampling and evaluations using different samplers and evaluations."
    )
    parser.add_argument(
        "--list-models", action="store_true", help="List available models"
    )
    parser.add_argument("--model", type=str, help="Select a model by name", default="gpt-4.1-nano")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument(
        "--examples", type=int, default=2, help="Number of examples to use (overrides default)"
    )

    args = parser.parse_args()

    models = {

        # gpt 4.1 models
        "gpt-4.1": ChatCompletionSampler(
            model="gpt-4.1-2025-04-14",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        "gpt-4.1-mini": ChatCompletionSampler(
            model="gpt-4.1-mini-2025-04-14",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        "gpt-4.1-nano": ChatCompletionSampler(
            model="gpt-4.1-nano-2025-04-14",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        # gpt 4o models
        "gpt-4o": ChatCompletionSampler(
            model="gpt-4o",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        "gpt-4o-mini": ChatCompletionSampler(
            model="gpt-4o-mini-2024-07-18",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        # gpt 4.5 models
        "gpt-4.5-preview": ChatCompletionSampler(
            model="gpt-4.5-preview-2025-02-27",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        # gpt 4 turbo models 
         "gpt-4-turbo-2024-04-09": ChatCompletionSampler(
            model="gpt-4-turbo-2024-04-09",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        # chatgpt models:
        "chatgpt-4o-latest": ChatCompletionSampler(
            model="chatgpt-4o-latest",
            system_message=OPENAI_SYSTEM_MESSAGE_CHATGPT,
            max_tokens=2048,
        ),
        "gpt-4-turbo-2024-04-09_chatgpt": ChatCompletionSampler(
            model="gpt-4-turbo-2024-04-09",
            system_message=OPENAI_SYSTEM_MESSAGE_CHATGPT,
        ),

    }

    if args.list_models:
        print("Available models:")
        for model_name in models.keys():
            print(f" - {model_name}")
        return

    if args.model:
        if args.model not in models:
            print(f"Error: Model '{args.model}' not found.")
            return
        models = {args.model: models[args.model]}

    grading_sampler = ChatCompletionSampler(model="gpt-4o")
    equality_checker = ChatCompletionSampler(model="gpt-4-turbo-preview")
    # ^^^ used for fuzzy matching, just for math

    def get_evals(eval_name, debug_mode):
        num_examples = (
            args.examples if args.examples is not None else (5 if debug_mode else None)
        )
        # Set num_examples = None to reproduce full evals
        match eval_name:

            case "browsecomp":
                return BrowseCompEval(
                    grader_model=grading_sampler,
                    num_examples=2 if debug_mode else num_examples,
                )
            case _:
                raise Exception(f"Unrecognized eval type: {eval_name}")

    evals = {
        eval_name: get_evals(eval_name, args.debug)
        for eval_name in ["browsecomp"]
    }
    print(evals)
    debug_suffix = "_DEBUG" if args.debug else ""
    print(debug_suffix)
    mergekey2resultpath = {}
    #for model_name, sampler in models.items(): #models are the agent

    for eval_name, eval_obj in evals.items():
        result = eval_obj(sampler)
        # ^^^ how to use a sampler
        #file_stem = f"{eval_name}_managed_agent"
        #report_filename = f"/tmp/{file_stem}{debug_suffix}.html"
        #print(f"Writing report to {report_filename}")
        #with open(report_filename, "w") as fh:
            #fh.write(common.make_report(result))
        metrics = result.metrics | {"score": result.score}
        print(metrics)
        """
        result_filename = f"/tmp/{file_stem}{debug_suffix}.json"
        with open(result_filename, "w") as f:
            #f.write(json.dumps(metrics, indent=2))
        print(f"Writing results to {result_filename}")
        mergekey2resultpath[f"{file_stem}"] = result_filename
    merge_metrics = []
    for eval_model_name, result_filename in mergekey2resultpath.items():
        try:
            result = json.load(open(result_filename, "r+"))
        except Exception as e:
            print(e, result_filename)
            continue
        result = result.get("f1_score", result.get("score", None))
        eval_name = eval_model_name[: eval_model_name.find("_")]
        model_name = eval_model_name[eval_model_name.find("_") + 1 :]
        merge_metrics.append(
            {"eval_name": eval_name, "model_name": model_name, "metric": result}
        )
    merge_metrics_df = pd.DataFrame(merge_metrics).pivot(
        index=["model_name"], columns="eval_name"
    )
    print("\nAll results: ")
    print(merge_metrics_df.to_markdown())
    """
    #return merge_metrics
    return None


if __name__ == "__main__":
    main()
