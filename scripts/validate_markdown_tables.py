from __future__ import annotations

import re
from dataclasses import dataclass

from _ci_utils import display_path, git_ls_files, masked_fenced_lines, read_text

SEPARATOR_CELL_PATTERN = re.compile(r"^:?-{3,}:?$")
TABLE_VALIDATION_EXCLUDED_FILES = {
    "standard/appendix/Compliance_Matrix.md",
}


@dataclass
class ParsedRow:
    cells: list[str]
    separator_count: int


def parse_table_row(row: str) -> ParsedRow:
    text = row.strip()

    if text.startswith("|"):
        text = text[1:]

    if text.endswith("|"):
        text = text[:-1]

    cells: list[str] = []
    current: list[str] = []
    separator_count = 0
    code_delimiter_length = 0
    backslash_run = 0
    index = 0

    while index < len(text):
        character = text[index]

        if character == "`":
            run_end = index
            while run_end < len(text) and text[run_end] == "`":
                run_end += 1

            run_length = run_end - index
            if code_delimiter_length == 0:
                code_delimiter_length = run_length
            elif run_length == code_delimiter_length:
                code_delimiter_length = 0

            current.append(text[index:run_end])
            backslash_run = 0
            index = run_end
            continue

        if code_delimiter_length == 0 and character == "|":
            if backslash_run % 2 == 1:
                current.append(character)
            else:
                cells.append("".join(current).strip())
                current = []
                separator_count += 1

            backslash_run = 0
            index += 1
            continue

        current.append(character)

        if code_delimiter_length == 0 and character == "\\":
            backslash_run += 1
        else:
            backslash_run = 0

        index += 1

    cells.append("".join(current).strip())
    return ParsedRow(cells=cells, separator_count=separator_count)


def is_header_candidate(row: str, parsed_row: ParsedRow) -> bool:
    return bool(row.strip()) and parsed_row.separator_count >= 1 and len(parsed_row.cells) >= 2


def is_separator_row(parsed_row: ParsedRow) -> bool:
    return (
        parsed_row.separator_count >= 1
        and len(parsed_row.cells) >= 2
        and all(SEPARATOR_CELL_PATTERN.fullmatch(cell.strip()) for cell in parsed_row.cells)
    )


def is_body_candidate(row: str, parsed_row: ParsedRow, expected_columns: int) -> bool:
    stripped = row.strip()
    if not stripped or parsed_row.separator_count == 0:
        return False

    if stripped.startswith("|") or stripped.endswith("|"):
        return True

    return parsed_row.separator_count >= expected_columns - 1


def validate_markdown_tables() -> int:
    markdown_files = git_ls_files("*.md")

    if not markdown_files:
        print("No Markdown files found. Skipping Markdown table validation.")
        return 0

    failed = False

    for path in markdown_files:
        display_name = display_path(path)

        if display_name in TABLE_VALIDATION_EXCLUDED_FILES:
            print(
                "Skipping Markdown table validation for known existing table issues: "
                f"{display_name}"
            )
            continue

        lines = masked_fenced_lines(read_text(path))
        index = 0

        while index < len(lines) - 1:
            header_line_number, header_line = lines[index]
            separator_line_number, separator_line = lines[index + 1]
            parsed_header = parse_table_row(header_line)

            if not is_header_candidate(header_line, parsed_header):
                index += 1
                continue

            parsed_separator = parse_table_row(separator_line)
            if not is_separator_row(parsed_separator):
                index += 1
                continue

            expected_columns = len(parsed_header.cells)

            if len(parsed_separator.cells) != expected_columns:
                print(
                    f"FAILED: {display_name}:{separator_line_number}: "
                    "Markdown table separator column count does not match the header row."
                )
                failed = True

            row_index = index + 2

            while row_index < len(lines):
                row_line_number, row = lines[row_index]
                if not row.strip():
                    break

                parsed_row = parse_table_row(row)
                if not is_body_candidate(row, parsed_row, expected_columns):
                    break

                if len(parsed_row.cells) != expected_columns:
                    print(
                        f"FAILED: {display_name}:{row_line_number}: "
                        f"Markdown table row has {len(parsed_row.cells)} columns; "
                        f"expected {expected_columns}."
                    )
                    failed = True

                row_index += 1

            index = row_index

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(validate_markdown_tables())
