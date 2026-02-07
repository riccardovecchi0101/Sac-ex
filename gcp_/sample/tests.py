#!/usr/bin/env python3
import requests
import json

#BASE_URL = "http://localhost:8080/api/v1"
# Per App Engine:
BASE_URL = "https://secretsantaesame.oa.r.appspot.com//api/v1"

participants = [
    {
        "email": "alice@example.com",
        "name": "Alice",
        "surname": "Rossi"
    },
    {
        "email": "bob@example.com",
        "name": "Bob",
        "surname": "Bianchi"
    },
    {
        "email": "carol@example.com",
        "name": "Carol",
        "surname": "Verdi"
    }
]


def print_response(resp):
    print(f"STATUS: {resp.status_code}")
    try:
        print(json.dumps(resp.json(), indent=2))
    except Exception:
        print(resp.text)
    print("-" * 50)


def register_participant(p):
    print(f"➡️  Registering {p['email']}")
    url = f"{BASE_URL}/santa/{p['email']}"
    payload = {
        "name": p["name"],
        "surname": p["surname"]
    }
    r = requests.post(url, json=payload)

    print_response(r)

    # ASSERT ESAME
    assert r.status_code in (200, 201), \
        f"POST failed for {p['email']} (rc={r.status_code})"


def get_receiver(email):
    print(f"🎁 Getting receiver for {email}")
    url = f"{BASE_URL}/santa/{email}"
    r = requests.get(url)

    print_response(r)

    # ASSERT ESAME
    assert r.status_code == 200, \
        f"GET failed for {email} (rc={r.status_code})"

    body = r.json()
    assert "receiver" in body, \
        "Missing 'receiver' field in response"


def test_full_flow():
    url = f"{BASE_URL}/clean"
    
    r = requests.get(url)
    print_response(r)
    print("\n=== REGISTER PARTICIPANTS ===\n")
    for p in participants:
        register_participant(p)

    print("\n=== GET RECEIVERS ===\n")
    for p in participants:
        get_receiver(p["email"])


def test_error_cases():
    print("\n=== ERROR TESTS ===\n")

    # GET utente inesistente
    print("❌ GET non-existing user")
    r = requests.get(f"{BASE_URL}/santa/notfound@example.com")
    print_response(r)

    assert r.status_code == 404, \
        f"Expected 404, got {r.status_code}"
    assert "message" in r.json(), \
        "Error response missing 'message' field"

    # POST duplicato
    print("❌ POST duplicate user")
    p = participants[0]
    r = requests.post(
        f"{BASE_URL}/santa/{p['email']}",
        json={"name": p["name"], "surname": p["surname"]}
    )
    print_response(r)

    assert r.status_code in (400, 409), \
        f"Expected 400/409, got {r.status_code}"
    assert "message" in r.json(), \
        "Duplicate error missing 'message' field"


if __name__ == "__main__":
    test_full_flow()
    test_error_cases()
    print("\n✅ ALL TESTS PASSED")
