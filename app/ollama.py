from flask import Flask, request, jsonify, render_template
import json
import subprocess

def listInstalledModels():
    curl_command = f'curl http://localhost:11434/api/tags'

    output = subprocess.check_output(curl_command, shell=True, encoding='utf-8')
    res = json.loads(output)

    return res

def listModels():
    res = listInstalledModels()
    return jsonify({'models':res})

print(listModels())

