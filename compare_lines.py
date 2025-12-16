def compare_files(file1_path, file2_path):
    # Read and strip lines
    with open(file1_path, 'r', encoding='utf-8') as f1:
        lines1 = set(line.strip() for line in f1 if line.strip())

    with open(file2_path, 'r', encoding='utf-8') as f2:
        lines2 = set(line.strip() for line in f2 if line.strip())

    added = lines2 - lines1
    removed = lines1 - lines2

    if added:
        print("Lines Added:")
        for line in sorted(added):
            print(f"+ {line}")
    else:
        print("No lines added.")

    if removed:
        print("\nLines Removed:")
        for line in sorted(removed):
            print(f"- {line}")
    else:
        print("\nNo lines removed.")

if __name__ == "__main__":
    # Example usage
    compare_files("S2C_SERVICE_POLICY_NOT_0.6.2.6210-1086.txt", "S2C_SERVICE_POLICY_NOT_0.12.103.6355-1178.txt")
