import yaml

# 讀取YAML檔案
with open("data.yaml", "r") as file:
    lines = file.readlines()

names = []
for line in lines[1:]:
    line = line.strip()
    if line.startswith("nc:"):
        break
    name = line.replace("-", "").strip()
    names.append(name)

print("names:", names)

