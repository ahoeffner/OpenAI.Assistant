def readFile(filename):
  """Reads the contents of a file and returns its content.

  Args:
    filename: The path to the file to be read.

  Returns:
    The contents of the file as a string.
  """
  try:
    with open(filename, 'r') as f:
      content = f.read()
      return content
  except FileNotFoundError:
    return f"Error: File '{filename}' not found."
  except Exception as e:
    return f"An error occurred while reading the file: {e}"