from openai import OpenAI
client=OpenAI()

def convert_file_to_png(file_id,write_path):
    data=client.files.content(file_id)
    data_bytes=data.read()
    with open(write_path,'wb') as file:
        file.write(data_bytes)