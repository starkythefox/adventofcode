def readlines(file_path: str) -> list[str]:
    with open(file_path, 'r') as f:
        data = f.read().splitlines()

    return data
