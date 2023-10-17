import asyncio
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


async def conversation_tree_eater(chats: Dict[str, DiscordChatDocument]):
    output_text = ""

    component_summary_chain = create_component_summary_chain()
    global_summary_chain = create_global_summary_chain()
    input_texts = []
    all_text = []
    subfolders_to_skip = ["bibliography", "boilerplate", "figures", "header"]
    for path in Path(document_root_path).rglob("*"):
        if any(subfolder in str(path).lower() for subfolder in subfolders_to_skip):
            continue
        if path.is_file():
            if path.suffix == ".tex":
                print(f"=============================================================\n"
                      f"Processing {path}")
                file_content = path.read_text()

                text_to_analyze = (f"{str(path)}\n"
                                   f"{file_content}")
                all_text.append(text_to_analyze)
                input_texts.append({"text": text_to_analyze})

    all_summaries = await component_summary_chain.abatch(input_texts)
    for summary in all_summaries:
        file_summary = (f"+++++++++++++++++++++++++++++++++++\n\n"
                        f"{summary.content}\n\n"
                        f"-----------------------------------\n\n")
        print(file_summary)
        output_text += file_summary

    print(output_text)

    global_summary = global_summary_chain.invoke({"text": "\n".join(all_text)}).content

    output_text += (f"=============================================================\n\n"
                    f"=============================================================\n\n"
                    f"___ \n > Global Summary \n {global_summary}\n\n")

    document_tree = DirectoryTreeBuilder.from_path(path=document_root_path)

    document_tree_string = f"```\n\n{document_tree.print()}\n\n```\n\n"
    print(document_tree_string)
    output_text += document_tree_string

    with open("document_summary.md", "w", encoding="utf-8") as file:
        file.write(output_text)


if __name__ == "__main__":
    chats_json_path = Path(
        r"D:\Dropbox\Northeastern\Courses\neural_control_of_real_world_human_movement\2023-09-Fall\classbot_data\backup\2023-10-16_jonbot_database.chats.json")
    chats_json = json.loads(chats_json_path.read_text())

    chats = asyncio.run(get_chats(database_name=database_name,
                                  query={"server_id": server_id}))
