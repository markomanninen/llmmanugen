import json
import os
from datetime import datetime
import re

class Manuscript:

    def __init__(self, data, title_field="title", children_field="sections"):
        self.title_field = title_field
        self.children_field = children_field
        self.data = data
        if self.children_field not in self.data:
            self.data[self.children_field] = []
        if not self.validate_schema(self.data):
            raise ValueError("Invalid schema")
        self.reset_current_section_path()

    def validate_schema(self, schema):
        def _(s):
            if not isinstance(s, dict):
                return False
            if self.title_field not in s or not s[self.title_field]:
                return False
            if self.children_field in s:
                if not isinstance(s[self.children_field], list):
                    return False
                for child in s[self.children_field]:
                    if not _(child):
                        return False
            return True
        return _(schema)

    def reset_current_section_path(self, path_indices=None):
        self.current_path = path_indices or [0]

    def get_section(self, path_indices):
        section = self.data[self.children_field]
        for index in path_indices:
            try:
                if self.children_field in section:
                    section = section[self.children_field]
                section = section[index]
            except:
                return None
        return section

    def get_current_section(self):
        return self.get_section(self.current_path)

    def get_current_and_next_sections(self, without_children=True):
        current_section = self.get_current_section()
        temp_path = self.current_path.copy()
        next_section = None
        if self.move_to_next_section() == "continue":
            next_section = self.get_current_section()
        self.current_path = temp_path
        if without_children:
            if current_section:
                current_section = {k: v for k, v in current_section.items() if k != self.children_field}
            if next_section:
                next_section = {k: v for k, v in next_section.items() if k != self.children_field}
        return current_section, next_section

    def move_to_next_section(self, only_at_the_same_level=False):
        section = self.data[self.children_field]
        path = self.current_path.copy()
        for index in path[:-1]:
            section = section[index][self.children_field]
        if not only_at_the_same_level and self.children_field in section[path[-1]] and section[path[-1]][self.children_field]:
            self.current_path.append(0)
            return "continue"
        if len(section) > path[-1] + 1:
            self.current_path[-1] += 1
            return "continue"
        else:
            if only_at_the_same_level:
                return "end"

            while len(self.current_path) > 1:
                self.current_path.pop()
                sections = self.data[self.children_field]
                for index in self.current_path[:-1]:
                    sections = sections[index][self.children_field]
                if len(sections) > self.current_path[-1] + 1:
                    self.current_path[-1] += 1
                    return "continue"
            else:
                return "end"
        return "continue"

    def add_current_content(self, content):
        current_section = self.get_current_section()
        if current_section:
            content_copy = {k: v for k, v in content.items() if k != self.children_field}
            current_section.update(content_copy)

    @staticmethod
    def from_json(file_path):
        with open(file_path, 'r') as f:
            return Manuscript(json.load(f))

    def to_json(self, directory=None):
        if not self.validate_schema(self.data):
            raise ValueError("Invalid schema")
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        filename = self.get_safe_filename('.json')
        filepath = os.path.join(directory or '', filename)
        with open(filepath, 'w') as f:
            json.dump(self.data, f, indent=4)
        return filename, filepath

    def get_safe_filename(self, extension):
        title = self.data.get(self.title_field, "Untitled")
        title = re.sub(r'[^\w\s]', '', title).replace(' ', '_')
        return f"{title}_{datetime.now().strftime('%Y%m%d%H%M%S')}{extension}"

    def get_table_of_contents(self, tree_structure=True):
        toc = []
        current_section = self.get_current_section()
        current_title = current_section[self.title_field] if current_section else ""
        def _(sections, level, prefix=''):
            for i, section in enumerate(sections):
                is_last = i == len(sections) - 1
                new_prefix, spacer = ('└── ', '    ') if is_last else ('├── ', '│   ')
                if not tree_structure:
                    new_prefix, spacer = '', '  ' * (level - 1)
                toc.append(f"{prefix}{new_prefix}{section[self.title_field]}{'*' if section[self.title_field] == current_title else ''}")
                if self.children_field in section:
                    _(section[self.children_field], level + 1, prefix + spacer)
        _(self.data[self.children_field], 1)
        return '\n'.join(toc)

    def to_md(self, content_field=None, directory=None):
        md = []
        def _(subsection, level):
            for section in subsection:
                md.append(f"{'#' * level} {section[self.title_field]}")
                if content_field:
                    md.append(section.get(content_field, f"Section content not present for the field: {content_field}"))
                if self.children_field in section:
                    _(section[self.children_field], level + 1)
        _(self.data[self.children_field], 1)
        markdown_str = '\n'.join(md)
        filename = self.get_safe_filename('.md')
        filepath = os.path.join(directory or '', filename)
        with open(filepath, 'w') as f:
            f.write(markdown_str)
        return filename, filepath

    def search(self, query, field=None, path=None):
        results = []
        search_field = field or self.title_field
        def _(sections, new_path=[]):
            for i, section in enumerate(sections):
                local_path = new_path + [i]
                if search_field in section and ((isinstance(query, str) and query.lower() in section[search_field].lower()) or
                                                (isinstance(query, re.Pattern) and query.search(section[search_field]))):
                    if path is None or path == local_path[:len(path)]:
                        results.append({"section": section, "path": local_path})
                if self.children_field in section:
                    _(section[self.children_field], local_path)
        _(self.data[self.children_field])
        return results

    def find_path_indices(self, field_values):
        def _(subsections, remaining_fields, new_path=[]):
            for i, section in enumerate(subsections):
                if section[self.title_field] == remaining_fields[0]:
                    local_path = new_path + [i]
                    if len(remaining_fields) == 1:
                        return local_path
                    if self.children_field in section:
                        return _(section[self.children_field], remaining_fields[1:], local_path)
        return _(self.data[self.children_field], field_values)
