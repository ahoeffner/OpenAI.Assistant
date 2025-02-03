import openai

#Use the provided files as the sole source of information to answer my questions. Do not use any external knowledge or attempt to access the internet. If the answer cannot be found in the provided files, state that you do not have enough information


class Assistant :
	def __init__(self, client:openai.OpenAI, model:str, name:str) :
		self.name = name
		self.model = model
		self.client = client
		self.assistant = None


	def id(self) :
		return(self.assistant.id)


	def create(self, instructions:str, tools:list, files:list=[]) :
		self.assistant = self.client.beta.assistants.create(
			tools=tools,
			file_ids=files,
			name=self.name,
			model=self.model,
			instructions=instructions)

		return(self.assistant)


	def retrieve(self, assistid:str) :
		self.assistant = self.client.beta.assistants.retrieve(assistid)
		return(self.assistant)




client = openai.OpenAI()
assistant = Assistant(client, "gpt-4-turbo", "Knowlwedge Base")

file = client.files.create(file=open("src/files.py", "rb"), purpose="assistants")
assistant.create("This is a test assistant", [{"type": "retrieval"}],[file.id])