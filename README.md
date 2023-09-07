# LLMManuGen (c) 2023 - Marko T. Manninen - All Rights Reserved

A Python class for structured, automated generation and management of manuscripts using JSON and Markdown formats.

Use with ChatGPT + Advanced Data Analysis plug-in activated.

## Prompt

To replicate the manuscript generation process, follow steps:

STEP 1.

Ask user to give a JSON data, or generate it by asking the topic, title, guidelines and table of contents for the manuscript.

1a. If data is given by uploading a file or giving a JSON data string, use it.

Reading the JSON Prompt String/File: Start by reading a JSON data that contains the blueprint of the manuscript, including meta-information like title, subtitle, author, disclaimer, and guidelines, as well as an outline of sections and their respective prompts.

1b. Else generate JSON string with the format described in JSON Structure and Example part.

STEP 2. Initialize Manuscript Class

import json

class Manuscript:
    def __init__(self, json_data):
        for k, d in {"title": "", "subtitle": "", "author": "", "disclaimer": "", "guidelines": {}, "constraints": {}, "sections": []}.items():
            setattr(self, k, json_data.get(k, d))
        self.current_path = [0]

    def _get_section(self, path):
        section = self.sections
        for idx in path:
            try:
                section = section["sections"] if "sections" in section else section[idx]
            except (IndexError, KeyError, TypeError):
                return None
        return section

    def get_current_section_prompts(self):
        cs = self._get_section(self.current_path)
        ct, cp = (cs.get("title", ""), cs.get("prompt", "")) if cs else ("", "")
        tpath, self.current_path = self.current_path.copy(), self.current_path.copy()
        s = self.move_to_next_section()
		if s == "end":
			nt, np = "End", "End."
        else:
			ns = self._get_section(self.current_path)
		    nt, np = ns.get("title", ""), ns.get("prompt", "")
		self.current_path = tpath
		return {
			"current": {"title": ct, "prompt": cp}, 
			"next": {"title": nt, "prompt": np}
		}

    def move_to_next_section(self):
        section, path = self.sections, self.current_path.copy()
        for idx in path[:-1]:
            section = section[idx]["sections"]
        if 'sections' in section[path[-1]]:
            self.current_path.append(0)
            return "continue"
        if len(section) > path[-1] + 1:
            self.current_path[-1] += 1
        else:
            while len(self.current_path) > 1:
                self.current_path.pop()
                ps = self.sections
                for idx in self.current_path[:-1]:
                    ps = ps[idx]["sections"]
                if len(ps) > self.current_path[-1] + 1:
                    self.current_path[-1] += 1
                    break
            else:
                return "end"
        return "continue"

    def add_current_content(self, text, title=None):
        cs = self._get_section(self.current_path)
        if cs:
            cs["content"] = text
            if title: cs["title"] = title

    def to_json(self, op=None):
        js = json.dumps({k: v for k, v in vars(self).items() if k != "current_path"}, indent=4)
        if op: open(op, 'w').write(js)
        return js

    def to_md(self, op=None, hl=1):
        def s2md(s, l):
            c = [f"{'#' * l} {s.get('title', '')}", f"> {s.get('prompt', '')}", s.get('content', "")]
            for ss in s.get("sections", []):
                c.append(s2md(ss, l + 1))
            return "\n".join(c)
        
        md = "\n".join([
			f"{'#' * hl} {self.title}", 
			f"{'#' * (hl + 1)} {self.subtitle}", 
			f"{'#' * (hl + 2)} {self.author}", 
			f"{'#' * (hl + 3)} {self.disclaimer}"
		] + [s2md(s, hl + 1) for s in self.sections])
        if op: open(op, 'w').write(md)
        return md

STEP 3. Traversing Sections One by One

- Start at the first section and proceed sequentially.
- At each section, read the current and next prompt from the JSON data.

STEP 4. Content Generation:

- Use the prompts guide to generate full-length content for that section. Indicate the length of the generated text with len() function.

STEP 5. User Review and Approval:

- Present the generated content to the user for review.
- Allow for any modifications if the user wishes to make them.
- Once accepted, store this content in the Manuscript class object. If Title is not given for the section, provide it as well.

STEP 6. Continue to Next Section:

- Once the content for the current section is approved, move on to the next section and repeat steps 3-5 until all sections have been covered.

STEP 7. Finalize Manuscript:

- After all sections have been completed, call the methods in the Manuscript class to save all the content to a Markdown (.md) and JSON files.

STEP 8. Download the Markdown File:

 - Provide the user with an option to download the finalized Markdown file AND JSON file containing the complete manuscript.

By following these steps, the process of reading the prompt, generating and reviewing content section-by-section, and finally saving it to a Markdown file will be accomplished.

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

-----

Start from STEP 1. Use Quick reply buttons/action suggestions when applicable.
