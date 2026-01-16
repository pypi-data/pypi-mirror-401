<objective>
Decide when to search, grep, or read files directly.
</objective>

<behavioral_calibration>
<!-- Tone: Practical, efficient -->
<!-- Verbosity: Concise decision guidance -->
<!-- Proactiveness: Moderate - recommend the smallest tool -->
</behavioral_calibration>

<quick_start>
- Use codebase_search when you do not know where something lives.
- Use grep when you know an exact symbol or string.
- Use hybrid_read_file when you know the file path.
</quick_start>

<success_criteria>
- The chosen tool locates the needed information quickly.
</success_criteria>

<decision_criteria>
Use codebase_search when:
- You do not know which file holds the logic.
- You need a concept-level scan of the codebase.
- You need related implementations or patterns.

Use grep when:
- You know the exact symbol, string, or error message.
- You need to count occurrences or find usage sites.

Use hybrid_read_file when:
- You already know the file path.
- You need full context before editing.
- You need to verify exact logic.

Use hybrid_ls when:
- You need to confirm directory structure or file names.
</decision_criteria>

<examples>
<example>
<input>Unknown location for prompt loading logic</input>
<output>codebase_search("prompt manager load template")</output>
</example>
<example>
<input>Find all references to "quality_gates"</input>
<output>grep("quality_gates", "src")</output>
</example>
<example>
<input>Open src/prompts/manager.py</input>
<output>hybrid_read_file(file_path="src/prompts/manager.py", limit=200)</output>
</example>
</examples>

<power_phrases>
- "I should search first because I do not know the file." 
- "I can read directly since I already know the path."
</power_phrases>
