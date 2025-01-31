import os
import time
import openai
from dotenv import load_dotenv

load_dotenv()
model="gpt-3.5-turbo"
client = openai.OpenAI()


def main() :
	thread = getThread()
	assistent = get_assistant()
	prompt(assistent, thread)


def prompt(assistant, thread) :
	while(True) :
		try: text = input("Enter a query: ")
		except EOFError : break
		except KeyboardInterrupt : break

		if (text.__len__() == 0) :
			continue

		if(text.lower() == "exit") :
			break

		client.beta.threads.messages.create(thread.id, role="user", content=text)
		exec = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
		time.sleep(0.1)

		while(True) :
			exec = client.beta.threads.runs.retrieve(run_id=exec.id, thread_id=thread.id)
			if (exec.status == "completed") : break
			print(".",end="",flush=True)
			time.sleep(0.1)

		messages = client.beta.threads.messages.list(thread.id)

		print()
		print()
		print(messages.data[0].content[0].text.value)
		print()
		print()


def getThread() :
	thread = client.beta.threads.create()
	return(thread)


def get_assistant() :
	assistid = os.getenv("ASSISTANT_ID")
	assistant = client.beta.assistants.retrieve(assistid)
	return(assistant)


main()