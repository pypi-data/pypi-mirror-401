
import requests

class PeptideAPIClient:
    def __init__(self, base_url="http://127.0.0.1:5000/api"):
        """
        Initializes the client with the base URL of the API.
        """
        self.base_url = base_url

    def get_peptide_experiment_counts(self, peptides: list) -> dict:
        """
        Takes a list of peptide sequences and returns a dictionary with their
        associated experiment counts.
        """
        if not isinstance(peptides, list):
            raise TypeError("Input must be a list of peptide strings.")

        # The endpoint we want to call
        endpoint = f"{self.base_url}/peptides/experiment_counts"
        
        # The JSON data to send in the request body
        payload = {"peptides": peptides}
        
        try:
            # Make the POST request
            response = requests.post(endpoint, json=payload, timeout=10) # 10-second timeout

            # Raise an exception if the server returned an error (like 4xx or 5xx)
            response.raise_for_status()
            
            # Return the JSON data from the response
            return response.json()
        
        except requests.exceptions.RequestException as e:
            # Handle network errors, timeouts, etc.
            print(f"An error occurred while communicating with the API: {e}")
            return None
        
    def check_peptide_existence(self, peptides: list) -> dict:
        """
        Takes a list of peptide sequences and returns a dictionary with their
        associated experiment counts.
        """
        if not isinstance(peptides, list):
            raise TypeError("Input must be a list of peptide strings.")

        # The endpoint we want to call
        endpoint = f"{self.base_url}/peptides/check_existence"
        
        # The JSON data to send in the request body
        payload = {"peptides": peptides}
        
        try:
            # Make the POST request
            response = requests.post(endpoint, json=payload, timeout=10) # 10-second timeout

            # Raise an exception if the server returned an error (like 4xx or 5xx)
            response.raise_for_status()
            
            # Return the JSON data from the response
            return response.json()
        
        except requests.exceptions.RequestException as e:
            # Handle network errors, timeouts, etc.
            print(f"An error occurred while communicating with the API: {e}")
            return None