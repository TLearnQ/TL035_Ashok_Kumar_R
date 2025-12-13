import os
import glob
import yaml
import json
import logging
import requests
import datetime
from pythonjsonlogger import jsonlogger

class APIResponseError(Exception):
    def __init__(self, message, status_code, payload=None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload

def setup_logging():
    logger = logging.getLogger()
    
    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger.setLevel(logging.INFO)
    
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')

    file_handler = logging.FileHandler('project.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

logger = setup_logging()

class RobustClient:
    def fetch_spec(self, url):
        try:
            response = requests.get(url, timeout=10)
            if 400 <= response.status_code < 600:
                raise APIResponseError(
                    f"API Error {response.status_code}",
                    response.status_code,
                    payload=response.text
                )
            return response.text
        except requests.RequestException as e:
            logger.error(f"Network failed: {str(e)}")
            return None

def analyze_apis():
    files = glob.glob("specs/*.yaml")
    
    if not files:
        logger.error("No YAML files found in 'specs/' folder.")
        return

    stats = {
        "total_endpoints": 0,
        "methods": {},
        "auth_methods": set(),
        "codes": {},
        "missing_responses": 0,
        "files_processed": 0
    }

    logger.info("Starting analysis", extra={"file_count": len(files)})
    metadata = []

    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)

            stats["files_processed"] += 1
            global_security = data.get('security', [])
            
            paths = data.get('paths', {})
            for path, methods in paths.items():
                for method, details in methods.items():
                    if method.lower() not in ['get', 'post', 'put', 'delete', 'patch']:
                        continue

                    stats["total_endpoints"] += 1
                    stats["methods"][method.upper()] = stats["methods"].get(method.upper(), 0) + 1
                    
                    endpoint_security = details.get('security', global_security)
                    current_auth = []
                    if endpoint_security:
                        for sec_rule in endpoint_security:
                            for scheme_name in sec_rule.keys():
                                stats["auth_methods"].add(scheme_name)
                                current_auth.append(scheme_name)
                    else:
                        current_auth = ["None"]

                    responses = details.get('responses', {})
                    if not responses:
                        stats["missing_responses"] += 1
                    
                    for code in responses:
                        stats["codes"][code] = stats["codes"].get(code, 0) + 1

                    metadata.append({
                        "file": os.path.basename(file_path),
                        "endpoint": path,
                        "method": method.upper(),
                        "auth_methods": current_auth,
                        "response_codes": list(responses.keys())
                    })
            
            logger.info("Parsed file successfully", extra={"file": os.path.basename(file_path)})

        except Exception as e:
            logger.error("Failed to parse file", extra={"file": file_path, "error": str(e)})

    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    logger.info("Metadata saved to metadata.json")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"""
    
    ========================================
    RUN SUMMARY - {timestamp}
    ========================================
    Total Files Parsed: {stats['files_processed']}
    Total Endpoints: {stats['total_endpoints']}
    Methods Distribution: {json.dumps(stats['methods'], indent=2)}
    Response Codes Observed: {json.dumps(stats['codes'], indent=2)}
    Authentication Methods: {list(stats['auth_methods'])}
    Endpoints with No Response Definition: {stats['missing_responses']}
    ========================================
    """
    
    with open("README.txt", "a") as f:
        f.write(report)
    
    logger.info("Summary report appended to README.txt")
    print(report)

if __name__ == "__main__":
    analyze_apis()


def meta_data(url):
    yamlcheck = yaml.safe_load(url)
    if yamlcheck == 0 :
        return "check the yaml structure"
    else:
        return yamlcheck 
        metadata.append(yamlcheck)
