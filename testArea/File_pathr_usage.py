from Config.filePaths.filePath import get_filePath

if __name__ == "__main__":
    # Request paths dynamically
    log_path = get_filePath("LOG")
    print(f"Log Path: {log_path}")

    config_path = get_filePath("CONFIG")
    print(f"Config Path: {config_path}")