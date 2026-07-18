#!/usr/bin/env python3
import sys
import argparse
import json
from src.assistant import AxiomHiveAssistant

def main():
    parser = argparse.ArgumentParser(description="AxiomHive AI Assistant CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with the AxiomHive Assistant")
    chat_parser.add_argument("query", type=str, help="Your question or command")

    # Threat analysis command
    threat_parser = subparsers.add_parser("analyze", help="Analyze an intelligence payload")
    threat_parser.add_argument("file", type=str, help="Path to JSON payload file")

    # Image processing command
    image_parser = subparsers.add_parser("image", help="Process an image with AxiomHive branding")
    image_parser.add_argument("source", type=str, help="Source image path")
    image_parser.add_argument("output", type=str, help="Output image path")
    image_parser.add_argument("--text", type=str, default="AXIOMHIVE", help="Branding text")

    args = parser.parse_args()
    assistant = AxiomHiveAssistant()

    if args.command == "chat":
        print("\n--- AxiomHive Assistant ---")
        print(assistant.chat(args.query))
        print("---------------------------\n")

    elif args.command == "analyze":
        try:
            with open(args.file, 'r') as f:
                payload = json.load(f)
            print("\n--- Strategic Threat Analysis ---")
            print(assistant.analyze_threat(payload))
            print("---------------------------------\n")
        except Exception as e:
            print(f"Error: {e}")

    elif args.command == "image":
        try:
            result = assistant.process_image(args.source, args.output, args.text)
            print(f"\n{result}\n")
        except Exception as e:
            print(f"Error: {e}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
