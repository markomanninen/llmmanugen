# LLMManuGen (c) 2023 - Marko T. Manninen - All Rights Reserved

LLMManuGen is a Python module for traversing hierachically structured, or in other words, nested data. In conjuction with ChatGPT, Advanced Data Analysis, and Noteable plugins, it is suitable for automated content planning, starting from building a table of contents, to the actual content and summary generation.

You can manage documents of varying types: task lists, manuscript table of contents, for instance. Initialization can be guided by ChatGPT, which helps you to form structured data, which in turn can be fed to the LLMManuGen module for a systematic iteration. Data import/export can be done in Python a native dictionary, JSON, and Markdown formats.

Use cases:

1. Use with ChatGPT + Advanced Data Analysis plug-in
2. Use with ChatGPT + Noteable plug-in
  2.1. Node Class
  2.2. Section Class
  2.3. Prompt Class
  2.4. Manuscript Class
  2.5. Extending Manuscript Class
3. Use locally using ChatGPT in autopilot mode (coming...)

# 1. Use with ChatGPT + Advanced Data Analysis plug-in

Please read [ChatGPT + ADA Manual](https://github.com/markomanninen/llmmanugen/blob/main/chatgpt_ada_manual.md) and use the [initial prompt](https://github.com/markomanninen/llmmanugen/blob/main/chatgpt_ada_pseudoclass_prompt.txt) given and explained in the manual in ChatGPT activated with the Advanced Data Analysis plugin.

# 2. Use with ChatGPT + Noteable plug-in

Use the [initial prompt](https://github.com/markomanninen/llmmanugen/blob/main/chatgpt_noteable_initialization_prompt.txt) with Noteable plug-in activated. Copy and paste the prompt to the chat window and follow the instructions. Learn by interacting with the environment.

## 2.1 Node Class



## 2.2 Section Class



## 2.3 Prompt Class



## 2.4 Manuscript Class



## 2.5 Extending Manuscript Class



# PROMPT - START WIZARD

This step-by-step procedure facilitates manuscript generation using ChatGPT and Noteable plugin. The process involves installing `llmmanugen` module, importing the required classes, accessing documentation, initializing class instances, collecting table of contents (TOC) titles and prompts, iteratively generating content section by section, and ultimately saving the completed manuscript as a markdown text file. Each step is permanently stored in notebook cells, allowing for independent execution at any time.


## STEP 1 (a-f)

a) Start with a new or existing project/notebook.

b) If the `llmmanugen` module is not present in the Noteable project:

```
!pip install llmmanugen
```

c) Then:

```
from llmmanugen import Manuscript, Section, Prompt, Node
```

d) Access the documentation for the `Manuscript`, `Section`, `Node`, and `Prompt` classes for future reference. Each class has a plenty of documentation, so you may want to retrieve them independently:

```
help({class})
```

e) Prompt the user for 1. a topic, 2. the manuscript title, subtitle, and author details.

f) Initialize `manuscript_dict` instance deduced from the given information:

```
manuscript_dict = {title, subtitle, author, disclaimer, created, updated, completed}
```

Any field can be later accessed by: `manuscript.field` getter and setter.


## STEP 2

In this stage, the user should supply the TOC titles formatted as any sort of hierarchical tree:

```
Heading 1
 - Heading 1.1
   - Heading 1.1.1
Heading 2
...
```

Either retrieve the TOC from the user or assist the user in crafting one.

Translate the given document to the following nested structure:

```
manuscript_dict["sections"] = [
    {
        "title": "Heading 1",
        "sections": [
            {
                "title": "Heading 1.1",
                "sections": [
                    {
                        "title": "Heading 1.1.1",
                    },
                    ...
                ]
            },
            ...
        ]
    },
    {
        "title": "Heading 2",
    },
    ...
]

manuscript = Manuscript.from_dictionary(manuscript_dict)
```
## STEP 3

Establish general rules for LLM/GPT (Large Language Model/Generative Pre-trained Transformer) prompts. For example:

```
guidelines = {
    'Role': 'Author', 
    'Style': 'Formal', 
    'Format': 'Essay', 
    'Context': 'Academic Research'
}
constraints = {
    'Content': 'Omit the inclusion of a main heading or title at the outset; Omit a concluding summary at the end of the sections; Avoid discussing topics reserved for future sections and steer clear of creating a fragmented structure with excessive subtitles.'
}
```

Apply these as a global system prompt for ChatGPT:

```
manuscript.guidelines = guidelines
manuscript.constraints = constraints
```

Remember: these general rules can be overridden for any specific section prompt.

## STEP 4 (a-b, iterative)

These definitions will guide the future content creation in STEP 5.

a) Formulate prompts for individual sections:

```
section_1_prompt = Prompt(
    directives = {'Instruction': '...'}
)
```

To override global guidelines and constraints, specify them either during the `prompt` initialization or later through separate assignments:

```
section_1_prompt.guidelines = {}
section_1_prompt.constraints = {}
```

For more information on prompt examples, consult: `print(Prompt.directives)`, `print(Prompt.guidelines)`, and `print(Prompt.constraints)`

b) Set a prompt for a section. There are different ways of doing this. Either traversing the tree one by one and updating each section prompt:

```
manuscript.move_to_next_section()
# and then:
manuscript.set_current_prompt(section_1_prompt)
# or:
manuscript.update_current_section(prompt=section_1_prompt)
```

or finding wanted section by indices:

```
current_section = manuscript.set_and_get_current_section_by_index([0])
current_section.update(prompt=section_1_prompt)
```

or by title(s):

```
current_section = manuscript.set_and_get_current_section_by_title("Heading 1")
current_section.update(prompt=section_1_prompt)
```

Batch initialization of sections is possible but advisable to limit to a small number, such as half a dozen, due to context window or max_token limitations of ChatGPT. It's preferable to proceed with smaller tasks.

Repeat STEP 4 for each of the sections.

---

The JSON file should adhere to a specific structure to be compatible with the Manuscript class. Here is the format description:

JSON Structure

title: The main title of the manuscript. (String)
subtitle: The subtitle for the manuscript, providing additional context or focus. (String)
author: Name of the author(s). (String)
disclaimer: Phrase the intention of the manuscript generation. (String)
guidelines: A dictionary containing guidelines for writing the manuscript.
constraints: A dictionary detailing any constraints on the manuscript.
sections: An array of dictionaries, each describing a section of the manuscript.
  - title: The title of the section. (String)
  - prompt: The writing prompt for that section. (String)
  - sections: (Optional) An array of sub-section dictionaries, recursively following the same structure as a section.
  - content: (Optional) To be generated. (String)

JSON Example

Here's a simplified example:

```
{
    "title": "The Interplay of Quantum Computing and Artificial Intelligence",
    "subtitle": "Unlocking New Frontiers in Technology",
    "author": "Marko T. Manninen",
	"disclaimer": "Content is A.I. generated by the given prompts. Facts are not checked. This document is for conceptual research purposes only.",
    "guidelines": {
        "format": "Academic Paper",
        "general": "Aim for clarity and conciseness;",
		"section_length": "3000-5000 characters"
    },
    "constraints": {
        "structure": "Do not write headings;",
        "blacklist_phrases": "In conclusion; Obviously; Basically; Anticipate; Foreshadow; Mystery;"
    },
    "sections": [
        {
            "title": "Introduction",
            "prompt": "Introduce the concept of The Interplay of Quantum Computing and Artificial Intelligence and its significance."
        },
        {
            "title": "Historical Perspective",
            "prompt": "Provide historical background or context for The Interplay of Quantum Computing and Artificial Intelligence."
        },
        {
            "title": "Technological Foundations",
            "prompt": "Discuss the core technologies in Quantum Computing and Artificial Intelligence.",
            "sections": [
                {
                    "title": "Quantum Mechanics",
                    "prompt": "Explain the principles of quantum mechanics that enable Quantum Computing."
                },
                {
                    "title": "Machine Learning Algorithms",
                    "prompt": "Describe the algorithms that are fundamental to Artificial Intelligence."
                }
            ]
        },
        {
            "title": "Challenges, Limitations, and Future Potential",
            "prompt": "Outline the challenges and limitations in marrying Quantum Computing with Artificial Intelligence. Conclude with future potential."
        }
    ]
}
```
-----

Start from STEP 1. Use Quick reply buttons/action suggestions when applicable.
