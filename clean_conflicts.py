import re
import os

def clean_conflicts(filepath):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple strategy: Find <<<<<<< HEAD ... ======= ... >>>>>>> [branch]
    # and pick the second part (the one from the branch, usually the 'Terre' side here)
    # Regex pattern to match the conflict blocks
    pattern = re.compile(r'<<<<<<< HEAD\n(.*?)\n?=======\n?(.*?)\n?>>>>>>> .*?\n', re.DOTALL)
    
    cleaned_content = pattern.sub(r'\2', content)
    
    # If there are stray markers without matching pairs, clean them too
    cleaned_content = re.sub(r'<<<<<<< HEAD\n', '', cleaned_content)
    cleaned_content = re.sub(r'=======\n', '', cleaned_content)
    cleaned_content = re.sub(r'>>>>>>> .*?\n', '', cleaned_content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Cleaned {filepath}")

# Clean both files
clean_conflicts(r'c:\Users\ELITE COMPUTER\Desktop\learn programming\webs\AgriTech\frontend\templates\agritecture.html')
clean_conflicts(r'c:\Users\ELITE COMPUTER\Desktop\learn programming\webs\AgriTech\frontend\index.html')
