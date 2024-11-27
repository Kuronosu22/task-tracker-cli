WINDOWS:


Set Up the PATH on Windows
On Windows, to run your script as a command, you need to add the directory containing the script to the system PATH. Here's how to do it:

Move or copy your script to a permanent directory:

Choose a directory to store the script, e.g., C:\Scripts.

Add the directory to the system PATH:

Open the Start Menu and search for "Environment Variables".

Click on Edit the system environment variables.

In the window that appears, click on Environment Variables.

Locate the variable named Path and click Edit.

Click New and enter the path to the directory containing your script, e.g., C:\Scripts.

Confirm all changes.

LINUX:


Make the file executable:

chmod +x script_name.py

Move the script to a directory in the PATH: To run your CLI from anywhere in the terminal, move the file to a directory that’s already in the system PATH. Common choices include /usr/local/bin:

sudo mv script_name.py /usr/local/bin/taskcli

Test the CLI: You can now run the program directly from the terminal:

$ taskcli add "Learn CLI"