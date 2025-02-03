import os
import time
import json
import openai
from files import readFile
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
		runner = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
		time.sleep(0.1)

		while(True) :
			runner = client.beta.threads.runs.retrieve(run_id=runner.id, thread_id=thread.id)

			if (runner.status == "completed") :
				break

			if (runner.status == "requires_action") :
				runCallOuts(runner,thread)

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


def runCallOuts(runner, thread) :
	response = []
	callsouts = runner.required_action.submit_tool_outputs.tool_calls

	for call in callsouts :
		func = call.function.name
		args = json.loads(call.function.arguments)
		
		result = readFile("src/"+args["file"])
		response.append({"tool_call_id": call.id, "output": "content: "+result})

	# show file yy on AlexMac
	# from AlexMac cat file files.py
	client.beta.threads.runs.submit_tool_outputs(thread_id=thread.id, run_id=runner.id, tool_outputs=response)


main()