def build_judge_prompt():
    system_prompt = (
        "You are an evaluator of programming tutor responses. "
        "Evaluate the response for correctness, relevance, "
        "beginner-friendliness, and instruction-following. "
        "Give a score from 0 to 1 for each criterion. "
        "For instruction-following, a short response means no more than 80 words. "
        "Return ONLY valid JSON. "
        "Do not include explanations, markdown, or any text outside the JSON. "
        "Use exactly these keys: correctness, relevance, "
        "beginner_friendly, instruction_following."
    )

    return system_prompt