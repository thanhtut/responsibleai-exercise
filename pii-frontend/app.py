import gradio as gr
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")


def analyze_text(text):
    """Send text to API for PII analysis"""
    try:
        response = requests.post(
            f"{API_URL}/process",
            json={
                "text": text,
            },
        )
        result = response.json()

        return result["redacted_text"]
    except Exception as e:
        return f"Error: {str(e)}"


def view_recent_analyses():
    """Fetch recent PII analyses"""
    try:
        response = requests.get(f"{API_URL}/history?limit=10")
        analyses = response.json()

        # Create a list to store formatted data
        formatted_data = []

        for analysis in analyses:
            # Format detections as a string
            detections_str = "; ".join(
                [
                    f"{d['detected_class']}: {d['text']} ({d['confidence']:.2%})"
                    for d in analysis["detections"]
                ]
            )

            # Create flags string
            pii_flags = []
            if analysis["name"]:
                pii_flags.append("Name")
            if analysis["email"]:
                pii_flags.append("Email")
            if analysis["phone"]:
                pii_flags.append("Phone")
            if analysis["nric"]:
                pii_flags.append("NRIC")
            if analysis["address"]:
                pii_flags.append("Address")

            # Format datetime
            created_at = datetime.fromisoformat(analysis["created_at"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # Add row to formatted data
            formatted_data.append(
                {
                    "Timestamp": created_at,
                    "Original Text": analysis["text"],
                    "Redacted Text": analysis["redacted_text"],
                    "PII Types Found": ", ".join(pii_flags),
                    "Detections": detections_str,
                }
            )

        # Create DataFrame
        df = pd.DataFrame(formatted_data)
        return df

    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})


# Create the Gradio interface
with gr.Blocks(title="PII Removal and Detection Tool") as demo:
    gr.Markdown("# PII Detection Tool")

    with gr.Tab("Analyze Text"):
        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(
                    label="Enter text to redact", placeholder="Enter your text here...", lines=5
                )
                analyze_btn = gr.Button("Redact PII")

            output_text = gr.Textbox(
                label="Analysis Results(redacted_text)", lines=10, interactive=False
            )

        analyze_btn.click(fn=analyze_text, inputs=input_text, outputs=output_text)

    with gr.Tab("Recent History"):
        view_btn = gr.Button("View Recent Analyses")
        history_table = gr.DataFrame(
            headers=[
                "Timestamp",
                "Original Text",
                "Redacted Text",
                "PII Types Found",
                "Detections",
            ],
            wrap=True,
            row_count=10,
        )

        view_btn.click(fn=view_recent_analyses, inputs=None, outputs=history_table)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
    )
