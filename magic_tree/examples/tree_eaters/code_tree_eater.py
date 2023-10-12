import asyncio
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

from magic_tree.controller.builders.directory_tree_builder import DirectoryTreeBuilder
from magic_tree.examples.tree_eaters.helpers.code_llm_chains import create_code_review_chain
from magic_tree.models.configuration.directory_tree_builder_configuration import DirectoryTreeConfig

load_dotenv()


async def code_tree_eater(root_path: Union[Path, str]):
    output_text = ""

    code_review_chain = create_code_review_chain()
    code_tree = DirectoryTreeBuilder.from_path(path=root_path,
                                               config=DirectoryTreeConfig(include=["*.py"]))
    code_tree_string = f"```\n\n{code_tree.print()}\n\n```\n\n"
    print(code_tree_string)

    input_texts = []
    all_text = []
    sub_folders_to_skip = []
    for path in Path(root_path).rglob("*"):
        if any(sub_folder in str(path).lower() for sub_folder in sub_folders_to_skip):
            continue
        if path.is_file():
            if path.suffix == ".py":

                file_content = path.read_text()

                if not file_content:
                    continue

                print(f"=============================================================\n"
                      f"Path - {path}\n\n")


                text_to_analyze = (f"============================================\n\n"
                                   f"{str(path)}\n\n"
                                   f"{file_content}\n\n")

                all_text.append(text_to_analyze)
                input_texts.append({"text": text_to_analyze})

    all_summaries = await code_review_chain.abatch(input_texts)

    for summary in all_summaries:
        file_summary = (f"+++++++++++++++++++++++++++++++++++\n\n"
                        f"{summary.content}\n\n"
                        f"-----------------------------------\n\n")
        print(file_summary)
        output_text += file_summary

    print(output_text)

    global_review = code_review_chain.invoke({"text": "\n".join(all_text)}).content

    output_text += (f"=============================================================\n\n"
                    f"=============================================================\n\n"
                    f"___ \n > Global Summary \n {global_review}\n\n")

    with open("document_summary.md", "w", encoding="utf-8") as file:
        file.write(output_text)


if __name__ == "__main__":
    code_root_path_in = Path(__file__).parent.parent
    asyncio.run(code_tree_eater(root_path=code_root_path_in))
