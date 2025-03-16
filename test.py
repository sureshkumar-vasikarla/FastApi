import jwt
import pdb
def verify_token_manually(token: str, key: str):
    try:
        pdb.set_trace()
        # Debug: Print the token
        # Decode and verify the JWT
        payload = jwt.decode(
            token,
            key,
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        print("Token is valid. Payload:", payload)
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError as e:
        print("Token is invalid:", str(e))

# Example usage
verify_token_manually("eyJhbGciOiJIUzI1NiIsImtpZCI6IjBRWnk1UVhuK0lzRFdZOUQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2J4ZHZ1cnltcnB4anJoeXp4aXVnLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJmMTU5ZDNlYS1hZmNiLTRjZmItODQ4OS0zMzM0OTk1YWE1NDEiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzQyMDQyODgxLCJpYXQiOjE3NDIwMzkyODEsImVtYWlsIjoic3VyZXNodkBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoic3VyZXNodkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiZjE1OWQzZWEtYWZjYi00Y2ZiLTg0ODktMzMzNDk5NWFhNTQxIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NDIwMzkyODF9XSwic2Vzc2lvbl9pZCI6IjVkMThkY2Q5LWEzNmMtNGYwMS1hYzFiLTQ5NDM0OTY5NGExNSIsImlzX2Fub255bW91cyI6ZmFsc2V9.iMC482E_gv6Tsg0501t0D3CAgs62KrL5nAwIDeH7IHU", "SBS179XQJ5zOc6JVRxbd8tQonUlD3ORUt0H+k0uyRHfqvI6lhgdFjqhn41SKI+tD2xLaMuhenKuLF1pnPDkeVg==")