This module is an implementation of archiver for a7d8473 archive format.
It can archive directories, files, soft links, has shell interface.
## What is a7d8473?
A7d8473 or simply a7d is a simple archive format, that has some nice features:
* If source directory has only text files, then archive will also be text file.
* Changing one line in the source file results in changing only one line in the archive.
* If all source files have line lenght limit, then archive will also have line lenght limit.
* Archived files are stored in compressor-friendly way:
  all the contents of the source file are usually included in the final archive file unchanged.
* Metadata is saved in git-like manner. Thus only this metadata is saved:
  * Executable flag.
  * Link flag.
* There is a bijection between the set of archive files and the set of directory structures.

## Hello world
This is "Hello, world!" file pushed into a7d8473 archive.
```
a7d8473
:hello.txt/
Hello, world!
~ ~ ~
```
Here is a little more complex archive:
```
a7d8473
/name_of_directory/
:name_of_file.txt/
-> here is the content of file <-
~ ~ ~
!name_of_another_file_that_is_executable.py/
print('Hi')
~ ~ ~
@name_of_soft_link/
target_of_this_soft_link
~ ~ ~
@link_to_Hi.py/
./name_of_another_file_that_is_executable.py
~ ~ ~
/empty_directory/
\
\
```
The first line of archive file is always "a7d8473".
Other lines describe archived files and directories.
`:` before `hello.txt` means, that file `hello.txt` is neither executable nor soft link.
There are other prefixes of file names:
* `@` denotes soft links.
* `!` denotes executable files.
* `/` denotes directories.
* `:` denotes simple files, which are neither executable nor soft links.

`/` is also used as the end of the name because it is not a valid character in file names.
`\` means end of directory, while `~ ~ ~` denotes end of file content.
Only printable ASCII characters are used outside of file contents.
Thus, archive files are text files as long as source files are text files.
