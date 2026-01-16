from typing import List, Optional, Union


def escape_latex(text: str) -> str:
    escape_dict = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
        "|": r"\textbar{}",
    }
    result = str(text)
    for char, escaped in escape_dict.items():
        result = result.replace(char, escaped)
    return result


def wrap_in_brackets(content: str) -> str:
    return f"{{{content}}}"


def join_with_separator(items: List[str], separator: str) -> str:
    return separator.join(items)


def make_cell(content: str, escape: bool = True) -> str:
    return wrap_in_brackets(escape_latex(content) if escape else content)


def make_cells(row: List[Union[str, int, float]], escape: bool = True) -> List[str]:
    return [make_cell(str(cell), escape) for cell in row]


def make_row(cells: List[str], separator: str = " & ") -> str:
    return f"{join_with_separator(cells, separator)} \\\\"


def make_hline() -> str:
    return r"\hline"


def make_column_spec(
    specs: Optional[List[str]] = None,
    default: str = "c",
    alignment: Optional[str] = None,
) -> str:
    if alignment:
        length = len(specs) if specs else 1
        return f"{{{alignment * length}}}"
    elif specs:
        return f"{{{join_with_separator(specs, '')}}}"
    else:
        return f"{{{default}}}"


def generate_table(
    data: List[List[Union[str, int, float]]],
    caption: Optional[str] = None,
    label: Optional[str] = None,
    column_alignments: Optional[List[str]] = None,
    header: Optional[List[str]] = None,
    escape_content: bool = True,
    add_hline: bool = True,
    centered: bool = True,
    column_spec: Optional[str] = None,
) -> str:
    if not data:
        raise ValueError("Данные таблицы не могут быть пустыми")

    first_len = len(data[0])
    for row in data:
        if len(row) != first_len:
            raise ValueError("Все строки должны иметь одинаковую длину")

    num_columns = first_len

    if column_spec:
        col_spec = column_spec
    elif column_alignments:
        if len(column_alignments) != num_columns:
            raise ValueError(
                f"Количество выравниваний ({len(column_alignments)}) "
                f"не совпадает с количеством столбцов ({num_columns})"
            )
        col_spec = make_column_spec(column_alignments)
    else:
        col_spec = make_column_spec([], "c", "c" * num_columns)

    header_lines = []
    if header:
        if len(header) != num_columns:
            raise ValueError(
                f"Количество заголовков ({len(header)}) "
                f"не совпадает с количеством столбцов ({num_columns})"
            )
        header_cells = make_cells(header, escape_content)
        header_lines.append(make_row(header_cells))
        if add_hline:
            header_lines.append(make_hline())

    data_lines = []
    for row in data:
        cells = make_cells(row, escape_content)
        data_lines.append(make_row(cells))

    all_lines = header_lines + data_lines

    if add_hline and not header:
        table_body = [make_hline()] + all_lines + [make_hline()]
    else:
        table_body = all_lines

    table_content = "\n        ".join(table_body)

    table_code = f"""\\begin{{table}}{"[h!]" if centered else ""}
    \\centering
    \\begin{{tabular}}{col_spec}
        {table_content}
    \\end{{tabular}}"""

    if caption:
        table_code += f"\n    \\caption{{{escape_latex(caption)}}}"

    if label:
        table_code += f"\n    \\label{{{label}}}"

    table_code += "\n\\end{table}"

    return table_code


def generate_image(
    filepath: str,
    caption: Optional[str] = None,
    label: Optional[str] = None,
    width: Optional[str] = None,
    height: Optional[str] = None,
    scale: Optional[float] = None,
    centered: bool = True,
) -> str:
    if not filepath:
        raise ValueError("Путь к файлу не может быть пустым")

    escaped_path = escape_latex(filepath)

    options = []
    if width:
        options.append(f"width={width}")
    if height:
        options.append(f"height={height}")
    if scale:
        options.append(f"scale={scale}")

    options_str = ""
    if options:
        options_str = f"[{','.join(options)}]"

    image_code = ""
    if centered:
        image_code += "\\begin{center}\n"

    image_code += f"\\includegraphics{options_str}{{{escaped_path}}}"

    if caption:
        image_code += f"\n\\caption{{{escape_latex(caption)}}}"

    if label:
        image_code += f"\n\\label{{{label}}}"

    if centered:
        image_code += "\n\\end{center}"

    return image_code


def generate_figure(
    filepath: str,
    caption: Optional[str] = None,
    label: Optional[str] = None,
    width: Optional[str] = None,
    height: Optional[str] = None,
    scale: Optional[float] = None,
    placement: str = "h!",
    centered: bool = True,
) -> str:
    image_code = generate_image(
        filepath=filepath,
        caption=None,
        label=None,
        width=width,
        height=height,
        scale=scale,
        centered=False,
    )

    figure_code = f"""\\begin{{figure}}{"[" + placement + "]" if placement else ""}
    \\centering
    {image_code}"""

    if caption:
        figure_code += f"\n    \\caption{{{escape_latex(caption)}}}"

    if label:
        figure_code += f"\n    \\label{{{label}}}"

    figure_code += "\n\\end{figure}"

    return figure_code


def generate_complete_document(
    content: str,
    title: Optional[str] = None,
    author: Optional[str] = None,
    document_class: str = "article",
    packages: List[str] = None,
    add_graphics_package: bool = True,
) -> str:
    if packages is None:
        packages = []

    base_packages = ["amsmath", "amssymb", "booktabs"]

    if add_graphics_package:
        base_packages.append("graphicx")

    all_packages = []
    for pkg in base_packages + packages:
        if pkg not in all_packages:
            all_packages.append(pkg)

    preamble_lines = []
    for package in all_packages:
        if package == "xcolor":
            preamble_lines.append("\\usepackage[dvipsnames]{xcolor}")
        else:
            preamble_lines.append(f"\\usepackage{{{package}}}")

    preamble = "\n".join(preamble_lines)

    title_section = ""
    if title or author:
        if title:
            title_section += f"\\title{{{escape_latex(title)}}}\n"
        if author:
            title_section += f"\\author{{{escape_latex(author)}}}\n"
        title_section += "\\maketitle\n\n"

    document = f"""\\documentclass{{{document_class}}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T2A]{{fontenc}}
\\usepackage[english, russian]{{babel}}

{preamble}

\\begin{{document}}

{title_section}{content}

\\end{{document}}"""

    return document


def save_to_file(content: str, filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def compile_latex_to_pdf(
    latex_content: str,
    output_filename: str,
    latex_engine: str = "pdflatex",
    working_dir: str = ".",
    cleanup: bool = True,
) -> bool:
    import os
    import subprocess
    import tempfile

    if not output_filename.endswith(".tex"):
        output_filename += ".tex"

    pdf_filename = output_filename.replace(".tex", ".pdf")

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = os.path.join(tmpdir, output_filename)

        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(latex_content)

        try:
            result = subprocess.run(
                [
                    latex_engine,
                    "-interaction=nonstopmode",
                    "-output-directory",
                    tmpdir,
                    tex_file,
                ],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                print(f"Ошибка компиляции LaTeX:")
                print(result.stdout)
                print(result.stderr)
                return False

            generated_pdf = os.path.join(tmpdir, pdf_filename)

            if os.path.exists(generated_pdf):
                final_pdf = os.path.join(working_dir, pdf_filename)
                import shutil

                shutil.copy(generated_pdf, final_pdf)

                if cleanup:
                    aux_files = [".aux", ".log", ".out", ".toc"]
                    for ext in aux_files:
                        aux_file = os.path.join(
                            tmpdir, output_filename.replace(".tex", ext)
                        )
                        if os.path.exists(aux_file):
                            os.remove(aux_file)

                return True
            else:
                print(f"PDF файл не создан: {generated_pdf}")
                return False

        except subprocess.TimeoutExpired:
            print("Таймаут компиляции LaTeX")
            return False
        except FileNotFoundError:
            print(
                f"LaTeX движок '{latex_engine}' не найден. Установите TeX Live или MikTeX"
            )
            return False
        except Exception as e:
            print(f"Ошибка при компиляции: {e}")
            return False
