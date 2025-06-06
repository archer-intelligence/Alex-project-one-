#!/usr/bin/env bash
# Prompts the user for their OpenAI API key and appends it to ~/.bashrc

read -p "Enter your OpenAI API key (sk-...): " key
if [[ -z "$key" ]]; then
    echo "No key entered. Aborting."
    exit 1
fi

touch ~/.bashrc
echo "" >> ~/.bashrc
echo "# OpenAI API Key exported by set_api_key.sh" >> ~/.bashrc
echo "export OPENAI_API_KEY=\"$key\"" >> ~/.bashrc

echo "✅ Your key has been added to ~/.bashrc."
echo "   Restart your shell or run: source ~/.bashrc"
