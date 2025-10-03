from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_contents
from functions.write_file import write_file
from functions.run_python_file import run_python_file
#cases = [

#	("calculator","."),
#	("calculator","pkg"),
#	("calculator","/bin"),
#	("calculator","../")
#	]

#for wd, d in cases:
#	print(f"Result for {d} directory:")
#	print(get_files_info(wd,d))
#	print()

#for case in cases:
#	print(get_files_info(case[0],case[1]))

#cases = [
#	("calculator","main.py"),
#	("calculator","pkg/calculator.py"),
#	("calculator","/bin/cat"),
#	("calculator","pkg/does_not_exist.py")
#	]

#for case in cases:
#	print(get_file_contents(case[0],case[1]))


#cases = [
#	("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
#	("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
#	("calculator", "/tmp/temp.txt", "this should not be allowed")
#	]

#for case in cases:
#	print(write_file(case[0],case[1],case[2] + "\n"))


cases = [
	("calculator","main.py"),
	("calculator","main.py",["3 + 5"]),
	("calculator","tests.py"),
	("calculator","../main.py"),
	("calculator","nonexistent.py")
	]

for case in cases:
	print(run_python_file(*case)+"\n")
