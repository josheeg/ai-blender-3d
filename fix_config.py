import pathlib
p = pathlib.Path(r'C:\Users\joshe\Desktop\blender-ai\_bmad\custom\config.user.toml')
p.write_text('[core]\nactive_initiative = "initiative-blender-ai"\n', encoding='utf-8')
print(p.read_bytes()[:10])