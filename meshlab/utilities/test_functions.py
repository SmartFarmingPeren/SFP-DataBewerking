def file_is_not_git_file(file_name):
    """
    This function checks if a file is a git file.
    :param file_name: Name of the file
    :return: False if file == git file, else true
    """
    GIT_FILE_NAMES = [".gitignore", "README.md", ".gitkeep"]
    for git_file in GIT_FILE_NAMES:
        if file_name == git_file:
            return False
    else:
        return True
