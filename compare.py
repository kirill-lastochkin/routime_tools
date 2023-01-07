import os

def main():
    files = os.listdir('.')
    files_rotated = os.listdir('./output')

    for file in files:
        if file[-4:] != ".mp4":
            continue

        for file_rotated in files_rotated:
            if file_rotated.find(file[:-4]) != -1:
                os.rename(file, './copied/' + file)
                break

if __name__ == "__main__":
    main()
