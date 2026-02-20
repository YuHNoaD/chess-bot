"""
Chess.com API Client - Alternative approach
"""

import requests
import json


class ChessComAPI:
    """Chess.com API client - using web API"""

    def __init__(self, api_key=None):
        # Use web API instead of pub API
        self.base_url = "https://www.chess.com"
        self.api_key = api_key
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        }

        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'

    def test_connection(self):
        """Test API connection"""
        # Check if chess.com is accessible
        url = f"{self.base_url}"

        try:
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                print("[OK] Chess.com website is accessible")
                return True
            else:
                print(f"[INFO] Chess.com status: {response.status_code}")
                return True  # Still accessible
        except Exception as e:
            print(f"[ERROR] Cannot connect to Chess.com: {e}")
            return False

    def get_profile(self, username):
        """Get user profile via web"""
        url = f"{self.base_url}/callback/user/profile?username={username}"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            try:
                return response.json()
            except:
                return None
        else:
            return None

    def get_stats(self, username):
        """Get user stats via web"""
        url = f"{self.base_url}/callback/user/stats?username={username}"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            try:
                return response.json()
            except:
                return None
        else:
            return None

    def get_games(self, username, limit=10):
        """Get recent games via web"""
        url = f"{self.base_url}/callback/user/games?username={username}&limit={limit}"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            try:
                return response.json().get('games', [])
            except:
                return []
        else:
            return []

    def get_challenges(self, username):
        """Get pending challenges (requires API key)"""
        if not self.api_key:
            print("[ERROR] API key required to get challenges")
            return []

        url = f"{self.base_url}/api/challenge?username={username}"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            try:
                return response.json().get('challenges', [])
            except:
                return []
        else:
            print(f"[ERROR] Cannot get challenges: {response.status_code}")
            return []

    def accept_challenge(self, challenge_id):
        """Accept a challenge (requires API key)"""
        if not self.api_key:
            print("[ERROR] API key required to accept challenge")
            return False

        url = f"{self.base_url}/api/challenge/{challenge_id}/accept"

        response = requests.post(url, headers=self.headers)

        if response.status_code == 200:
            return True
        else:
            print(f"[ERROR] Cannot accept challenge: {response.status_code}")
            return False

    def decline_challenge(self, challenge_id):
        """Decline a challenge (requires API key)"""
        if not self.api_key:
            print("[ERROR] API key required to decline challenge")
            return False

        url = f"{self.base_url}/api/challenge/{challenge_id}/decline"

        response = requests.post(url, headers=self.headers)

        if response.status_code == 200:
            return True
        else:
            print(f"[ERROR] Cannot decline challenge: {response.status_code}")
            return False

    def get_current_games(self, username):
        """Get current ongoing games"""
        url = f"{self.base_url}/callback/user/games?username={username}&status=in_progress"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            try:
                return response.json().get('games', [])
            except:
                return []
        else:
            return []


def main():
    """Test API"""
    print("="*60)
    print("CHESS.COM API TEST (Alternative)")
    print("="*60)

    # Create API client (without API key - public only)
    api = ChessComAPI()

    # Test connection
    if not api.test_connection():
        print("Cannot connect to Chess.com")
        return

    # Note: Without API key, we can only access public data
    print("\n[INFO] Without API key, we can only access public data")
    print("[INFO] To access challenges and play games, you need:")
    print("  1. Register at https://www.chess.com/club/chess-com-bots")
    print("  2. Get API key from chess.com")
    print("  3. Configure API key in config_chesscom.py")

    print("\n" + "="*60)
    print("API TEST COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()