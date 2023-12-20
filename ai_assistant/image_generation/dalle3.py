from openai import OpenAI
client = OpenAI()

response = client.images.generate(
  model="dall-e-3",
  prompt="帮我画一幅画，要求体现侠客风格，并描述以下场景：”赵客缦胡缨，吴钩霜雪明。银鞍照白马，飒沓如流星“",
  size="1792x1024", 
  quality="standard",
  n=1,
)

image_url = response.data[0].url

print(image_url)