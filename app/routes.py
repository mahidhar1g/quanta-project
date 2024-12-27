from flask import Flask, request, render_template, jsonify, send_from_directory, current_app
import os
from app.services import process_breakout_analysis

def setup_routes(app: Flask):
    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            try:
                # Call service to process analysis
                response = process_breakout_analysis(request.form)

                # Extract only the file name to avoid exposing the full file path
                output_file = os.path.basename(response["output_file"])
                response["output_file"] = output_file

                return jsonify(response)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        return render_template("index.html")

    @app.route("/download/<filename>", methods=["GET"])
    def download_file(filename):
        try:
            # Define the secure exports directory
            exports_dir = os.path.join(current_app.root_path, "exports")

            # Ensure the file exists
            file_path = os.path.join(exports_dir, filename)
            if not os.path.exists(file_path):
                return jsonify({"error": f"File {filename} not found"}), 404

            # Serve the file for download
            return send_from_directory(exports_dir, filename, as_attachment=True)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
