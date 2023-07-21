from transformers import TextGenerationPipeline
from transformers.pipelines.text_generation import ReturnType

STYLE = "{{text_prompt_start}}{instruction}{{end_of_sentence}}{{text_answer_separator}}"


class H2OTextGenerationPipeline(TextGenerationPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = STYLE

    def preprocess(
        self, prompt_text, prefix="", handle_long_generation=None, **generate_kwargs
    ):
        prompt_text = self.prompt.format(instruction=prompt_text)
        return super().preprocess(
            prompt_text,
            prefix=prefix,
            handle_long_generation=handle_long_generation,
            **generate_kwargs,
        )

    def postprocess(
        self,
        model_outputs,
        return_type=ReturnType.FULL_TEXT,
        clean_up_tokenization_spaces=True,
    ):
        records = super().postprocess(
            model_outputs,
            return_type=return_type,
            clean_up_tokenization_spaces=clean_up_tokenization_spaces,
        )
        for rec in records:
            rec["generated_text"] = (
                rec["generated_text"]
                .split("{{text_answer_separator}}")[1]
                .strip()
                .split("{{text_prompt_start}}")[0]
                .strip()
            )
        return records
