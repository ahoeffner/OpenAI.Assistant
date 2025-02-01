def read_file(filename):
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
    print(f"Error: File '{filename}' not found.")
    return None
  except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    return None